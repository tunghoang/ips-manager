const { spawn } = require('child_process');
module.exports = {
  forkChild, isServiceRunning, isServiceInstalled, checkServices, isModSecRulesInstalled,
}
function forkChild(cmd) {
    return new Promise(function(resolve, reject) {
        const child = spawn('bash', ['-c', cmd]);
        child.stdout.pipe(process.stdout);
        child.stderr.pipe(process.stderr);
        child.on("exit", function(code) {
            console.log('code:' + code);
            resolve(code === 0);
        });
    });
}
function isServiceRunning(service) {
    return forkChild(service.status)
}
function isServiceInstalled(service) {
    switch(service) {
    case 'idssystem':
      return forkChild('test -x /usr/local/bin/idssystem');
    case 'modsec':
      return new Promise(resolve => {
        resolve(true);
      });
    default:
      return forkChild('systemctl cat ' + service);
    }
}
function checkServices(services, cb) {
    let jobs = [];
    for (let i = 0; i < services.length; i++) {
        jobs.push(isServiceRunning(services[i]));
    }
    Promise.all(jobs).then(function(results) {
        let finalResult = results.reduce(function(total, item) {
            return total + (item?1:0);
        }, 0);
        let details = [];
        results.forEach(function(item, idx) {
            details.push({
                service: services[idx].name,
                running: item
            });
        });
        cb(null, {
            data: {
                engine_status: finalResult === results.length ? "Running\n":"Stopped\n",
                details: details
            },
            status: {
                code: 200,
                description: ""
            }
        });
    });
}

function isModSecRulesInstalled(webserver, ruleset) {
    switch(webserver) {
    case 'apache2':
        return forkChild(`grep -e "IncludeOptional /opt/modsecurity/${ruleset}/main.load" /etc/apache2/mods-enabled/security2.conf`).then(
            function(success) {
                if (success) {
                    return {
                        webserver: webserver,
                        ruleset: ruleset
                    }
                }
                return {
                    webserver: webserver
                }
            }
        );
    default:
        return new Promise(function(resolve, reject){
            resolve({webserver: webserver});
        })
    }
}
