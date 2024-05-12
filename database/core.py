from sqlalchemy import create_engine, Engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base, DeclarativeMeta

from service.models import ErrorMessage

Base = declarative_base()


class Database:
    def __init__(
        self,
        base: DeclarativeMeta,
        engine: Engine,
        session_callable: sessionmaker,
    ):
        self.base = base
        self.engine = engine
        self.sessionmaker = session_callable

    def __call__(self, **kwargs) -> Session:
        return self.sessionmaker(**kwargs)


def init_db(
    user: str,
    password: str,
    host: str,
    port: int,
    database: str,
) -> Database:
    """
    Create sqlalchemy sessionmaker

    Args:
        user: database user
        password: user's password
        host: database host
        port: database port
        database: database name

    Returns:
        Callable sessionmaker object
    """
    db_url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{database}"
    engine = create_engine(db_url)
    session_callable = sessionmaker(autocommit=False, autoflush=False, bind=engine)

    database = Database(Base, engine, session_callable)

    database.base.metadata.create_all(bind=engine, checkfirst=True)

    return database


def handle_database_exception(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as e:
            return ErrorMessage(code=400, message=f"Bad Request: {e}")
        except Exception as e:
            return ErrorMessage(code=400, message=f"Bad Request: {e}")

    return wrapper
