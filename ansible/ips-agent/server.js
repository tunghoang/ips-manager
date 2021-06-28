const getopts = require('getopts')
const express = require('express')
const fs = require('fs');
const ini = require('ini');
const YAML = require('yaml');

const options = getopts(process.argv.slice(2), {
  alias: {
    config: "c",
    port: "p"
  }
});
const {forkChild, checkServices, isServiceInstalled, isModSecRulesInstalled} = require('./utils');

const bodyParser = require('body-parser');
const app = express();
app.use(bodyParser.json());
app.use(bodyParser.urlencoded({ extended: false }));

app.use(express.static('public'));

const helloMsg = "Wellcome to test Manager IPS"

app.get('/', (req, res) => {
    res.send(helloMsg)
});

//const services = ['filebeat', 'filebeat.modsec', 'metricbeat', 'realtime-protection'];
const serviceConfigFile = process.env.SERVICE_CONFIG || options.config || 'services.yaml';
let content = fs.readFileSync(serviceConfigFile).toString()
console.log(content);
const services = YAML.parse(content);
console.log(services);
app.get('/engine/status', function(req, res) {
    checkServices(services, function(error, responseData) {
        if (!error) 
            res.send(responseData);
        else
            res.status(500).send(responseData);
    });
});

app.get('/engine/start', function(req, res) {
    let jobs = [];
    for (let i = 0; i < services.length; i++) {
        jobs.push(forkChild(services[i].start));
    }
    Promise.all(jobs).then(function(results) {
        checkServices(services, function(error, responseData) {
            if (!error) 
                res.send(responseData);
            else 
                res.status(500).send(responseData);
        });
    });
});

app.get('/engine/stop', function(req, res) {
    let jobs = [];
    for (let i = 0; i < services.length; i++) {
        jobs.push(forkChild(services[i].stop));
    }
    Promise.all(jobs).then(function(results) {
        checkServices(services, function(error, responseData) {
            if (!error) 
                res.send(responseData);
            else res.status(500).send(responseData);
        });
    });
});

app.get('/engine/query/webservers', function(req, res) {
    Promise.all([isServiceInstalled('apache2'), isServiceInstalled('nginx')]).then(function(results) {
        console.log(results);
        res.send({
            data: {
                apache2: results[0],
                nginx: results[1]
            },
            status: {
                code: 200,
                description: ""
            }
        });
    }).catch(e => {
        console.error(e);
        res.status(500).send(e.message);
    });
})

const MODSEC_RULES = {
    'apache2': ['coreruleset-3.3.0', 'cwaf'],
    'nginx': []
}
app.post('/engine/query/modsec-rules', function(req, res) {
    let webservers = req.body.webservers;
    let jobs = [];
    for (let ws of webservers) {
        for (let rs of MODSEC_RULES[ws]) {
            jobs.push(isModSecRulesInstalled(ws,rs));
        }
    }
    
    Promise.all(jobs).then(function(results) {
        let responseData = {};
        for (let r of results) {
            if (!responseData[r.webserver]) {
                responseData[r.webserver] = new Array()
            }
            if (!r.ruleset) continue;
            responseData[r.webserver].push(r.ruleset);
        }
        res.send({
            data: responseData,
            status: {
                code: 200,
                description: ""
            }
        })
    }).catch(e => {
        res.status(500).send(e.message);
    });
});

const HOSTIPS_APPS = ['modsec'];
const NETIPS_APPS = ['idssystem', 'idsapi'];
app.post('/engine/query/rules', function(req, res) {
    let idEnginetype = req.body.idEnginetype;
    switch (idEnginetype) {
        case 1: // Net IPS
            Promise.all(
                NETIPS_APPS.map(app => isServiceInstalled(app))
            ).then(results => {
                let responseData = {};
                for (let i = 0; i < results.length; i++) {
                    if (results[i]) {
                        responseData[NETIPS_APPS[i]] = [];
                    }
                }
                res.send({
                    data: responseData,
                    status: {
                        code: 200,
                        description: ""
                    }
                });
            }).catch(e => {
                res.status(500).send(e.message);
            });
            break;
        case 2: // Host IPS
            Promise.all(
                HOSTIPS_APPS.map(app => isServiceInstalled(app))
            ).then(function(results) {
                let responseData = {};
                for (let i = 0; i < results.length; i++) {
                    if (results[i]) {
                        responseData[HOSTIPS_APPS[i]] = [];
                    }
                }
                res.send({
                    data: responseData,
                    status: {
                        code: 200,
                        description: ""
                    }
                });
            }).catch(e => {
                res.status(500).send(e.message);
            });
            break;
    }
});

const realtimeProtectionIni='/opt/realtime-protection/realtime-protection.ini';
app.get('/engine/watchList', function(req, res) {
    let iniText = fs.readFileSync(realtimeProtectionIni, 'utf-8');
    let conf = ini.parse(iniText);
    console.log(conf);
    let watchPaths = conf.CLAMAV.watch_path.split(',');
    res.send({
        data: watchPaths,
        status: {code: 200, description: ""}
    });
});

app.put('/engine/watchList', function(req, res) {
    let iniText = fs.readFileSync(realtimeProtectionIni, 'utf-8');
    let conf = ini.parse(iniText);
    let watchPaths = req.body;
    for (let path of watchPaths) {
        let stats;
        try {
            stats = fs.statSync(path);
        }
        catch(e) {
            fs.mkdirSync(path, {recursive: true});
            continue;
        }
        if (!stats.isDirectory()) {
            res.status(500).send({
                data: path + " is not a directory",
                status: {
                    code: 500,
                    description: path + " is not a directory"
                }
            });
            return;
        }
    }
    conf.CLAMAV.watch_path = watchPaths.join(',');
    console.log(conf);
    fs.writeFileSync(realtimeProtectionIni, ini.stringify(conf));
    res.send({
        data: watchPaths,	
        status: {code: 200, description:""}
    });
});
const port = process.env.PORT || options.port || 8000;
app.listen(port, () => {
  console.log(`ips-agent listenning on port ${port}!`)
});

