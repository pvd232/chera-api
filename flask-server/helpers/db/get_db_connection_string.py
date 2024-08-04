def get_db_connection_string(
    username: str, password: str, db_name: str, db_server
) -> str:
    c_string_beginning = "postgresql://"
    c_string_end = f"@{db_server}/{db_name}"
    c_string = f"{c_string_beginning}{username}:{password}{c_string_end}"
    return c_string
