"""
This file contains tools to facilitate the use of the system.
"""


def generate_connection_string(type_database: str = "", user: str = "", password: str = "", host: str = "localhost",
                               port: str = "", database: str = "") -> str:
    """
    Returns the configuration string for SQLAlchmey to connect to the database.

    :param type_database: Type database to connect. PS.: sqlite, postgre, mariadb, mysql, oracle...
    :param user: User to connect into database.
    :param password: Password to connect into database, but if not have user, this field will be ignored.
    :param host: Host to connect database, by defaul is localhost, but if using sqlite, this field will be ignored.
    :param port: Port to database's host, if not have host parameter, this field will be ignored.
    :param database: Database's Name, if using SQLite, this need absolute path to SQLite file and filename.
    :return: str: String with contains config to use in SQLAlchemy
    """
    # Example of a full configuration string for SQLAlchemy.
    # '<type_database>://<user>:<password>@<host>:<port>/<database>'

    # security to avoid broken system
    if isinstance(type_database, str) and isinstance(user, str) and isinstance(password, str) and \
            isinstance(host, str) and isinstance(port, str) and isinstance(database, str):

        string_connection = type_database + "://"
        # if the user string is not empty, it will store the username in the string.
        if not user == "":
            string_connection = string_connection + user
        # If the user has a password and user, it will store the password in the string.
        if not password == "" and not user == "":
            string_connection = string_connection + ":" + password
        # If the connection has an address, it will store the address in the string.
        if not host == "" and not type_database.lower() == "sqlite":
            if not user == "":
                string_connection = string_connection + "@" + host
            else:
                string_connection = string_connection + host
        # If the connection requires a custom port and has a host
        # insert the port into the string
        if not port == "" and not host == "":
            string_connection = string_connection + ":" + port
        # Insert the server database into the string
        string_connection = string_connection + "/" + database
        return string_connection
    return ""
