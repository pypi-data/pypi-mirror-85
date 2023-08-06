from sqlalchemy import create_engine
from sqlalchemy.pool import SingletonThreadPool
from sqlalchemy.orm import sessionmaker, scoped_session
from SQLAlchemyEasyConnection import Utilities


class EasyConnection:
    def __init__(self):
        self.engine = None
        self.session = None

    def connect_to_database(self, type_database: str = "", user: str = "", password: str = "", host: str = "localhost",
                            port: str = "", database: str = "", sqlite_check_same_thread: bool = False,
                            pool_size: int = 600, max_overflow: int = 0, pool_recycle: int = 1) -> bool:
        """
        Create Engine and session to Database using SQLAlchemy engines.

        :param type_database: str: Type database to connect. PS.: sqlite, postgre, mariadb, mysql, oracle...
        :param user: str: User to connect into database.
        :param password: str: Password to connect into database, but if not have user, this field will be ignored.
        :param host: str: Host to connect database, by defaul is localhost, but if using sqlite, this field will be ignored.
        :param port: str: Port to database's host, if not have host parameter, this field will be ignored.
        :param database: str: Database's Name, if using SQLite, this need absolute path to SQLite file and filename.
        :param sqlite_check_same_thread: bool: Don't check if SQLite file already is in use.
        :param pool_size: int: This is the largest number of connections that will be kept persistently in the pool.
        :param max_overflow: int: When the number of checked-out connections reaches the size, additional connections will be returned up to this limit.
        :param pool_recycle: int: Number of seconds after which a connection is automatically recycled.
        :return:
        """
        if isinstance(type_database, str) and isinstance(user, str) and isinstance(password, str) \
                and isinstance(host, str) and isinstance(port, str) and isinstance(database, str) \
                and isinstance(sqlite_check_same_thread, bool) and isinstance(pool_size, int) \
                and isinstance(max_overflow, int) and isinstance(pool_size, int):
            connection_string = Utilities.generate_connection_string(type_database=type_database, user=user,
                                                                     password=password, host=host, port=port,
                                                                     database=database)
            if not connection_string == "":
                if type_database.lower() == "sqlite":
                    if sqlite_check_same_thread:
                        connection_string = connection_string + '?check_same_thread=False'
                    self.engine = create_engine(connection_string, poolclass=SingletonThreadPool)
                    print("Using SQLite on file: " + connection_string.upper())
                    session = sessionmaker(bind=self.engine)
                    self.session = scoped_session(session)
                    return True
                else:
                    self.engine = create_engine(connection_string, pool_size=pool_size, max_overflow=max_overflow,
                                                pool_recycle=pool_recycle)
                    print("Connected to :" + type_database.upper())
                    session = sessionmaker(bind=self.engine)
                    self.session = session()
                    return True
        return False

    def session_commit(self) -> None:
        """
        Commit changes into database.

        :return:
        """
        self.session.commit()

    def session_rollback(self):
        """
        Rollback last not committed changes.

        :return:
        """
        self.session.rollback()

    def insert_item(self, element):
        """
        Add new item.

        :param element: ORM instance.
        :return:
        """
        self.session.add(element)

    def insert_items(self, elements):
        """
        Add many items.

        :param elements: list: List of ORM instances.
        :return:
        """
        if isinstance(elements, list):
            self.session.add_all(elements)

    def delete_item(self, element):
        """
        Delete a item.

        :param element: ORM instance.
        :return:
        """
        self.session.delete(element)

    @property
    def get_engine(self):
        return self.engine

    @property
    def get_session(self):
        return self.session
