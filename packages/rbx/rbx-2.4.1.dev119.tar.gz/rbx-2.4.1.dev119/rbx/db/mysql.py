import warnings

from sqlalchemy import create_engine, text


class Singleton(type):
    _instance = None

    def __call__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__call__(*args, **kwargs)
        return cls._instance


class Connection(metaclass=Singleton):
    """Wraps a connection to a MySQL instance."""
    def __init__(self, db_engine_url):
        """Create a connection engine with default connection pooling.

        As a Singleton, the connection engine will only be created once for the entire process.
        SqlAlchemy will then chekout a new connection from the pool as needed.
        """
        self.engine = create_engine(
            db_engine_url,
            max_overflow=2,
            pool_pre_ping=True,
            pool_recycle=1800,  # 30 minutes
            pool_size=5,
            pool_timeout=30
        )

    def execute(self, *args, **kwargs):
        connection = self.engine.connect()
        connection.execute('SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci')
        connection.execute(*args, **kwargs)
        connection.close()

    def has_table(self, table_name):
        return self.engine.dialect.has_table(self.engine, table_name)

    def query(self, statement, scalar=False, total=None):
        """Run a SQL statement and return the results.

        When a 'total' SQL statement is provided, the total scalar is also returned, and the
        return object is then a tuple.

        When 'scalar' is True, a scalar type is returned.
        """
        connection = self.engine.connect()
        connection.execute('SET NAMES utf8mb4 COLLATE utf8mb4_unicode_ci')

        with warnings.catch_warnings():
            warnings.filterwarnings('ignore', '.*Division by 0.*', category=Warning)
            result = connection.execute(text(statement))

        if total:
            totals = connection.execute(total).scalar()

        if scalar:
            data = result.scalar()
        else:
            data = result.fetchall()

        result.close()
        connection.close()

        if total:
            return data, totals

        return data
