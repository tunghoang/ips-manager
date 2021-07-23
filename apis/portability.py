def quote(sql, dialect):
  if dialect == 'mysql':
    return sql.replace("#", '`')
  elif dialect == 'postgresql':
    return sql.replace("#", '"')
  else:
    return sql.replace("#", "")
