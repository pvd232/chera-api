def get_db_connection_string(
    username: str, password: str, env: str, name: str, host: str, port: str
) -> str:
    # Helpful starting point for database URI 101 https://stackoverflow.com/questions/58331055/how-do-you-specify-db-uri-postgres-db-connection-string-to-instance-running-in-g
    # Postgres connection URI info https://www.postgresql.org/docs/9.3/libpq-connect.html, 31.1.1.2. Connection URIs
    # SQLAlchemy database connection URI https://flask-sqlalchemy.palletsprojects.com/en/2.x/config/
    if env == "production":  # UNIX socket for host in cloud run
        return f"postgresql:///{name}?host={host}&port={port}&user={username}&password={password}"
    else:
        return f"postgresql://{username}:{password}@{host}:{port}/{name}"
