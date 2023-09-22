"""Database Connection"""
import os
import struct

import sqlalchemy
from azure import identity
from dotenv import load_dotenv
from sqlalchemy import create_engine, event
from sqlalchemy.ext.declarative import as_declarative, declared_attr
from sqlalchemy.orm import sessionmaker
from sqlmodel import Session

load_dotenv()


def get_engine():
    """Get Engine method"""
    if eval(os.getenv("IS_AZURE_BASED_TOKEN")):
        server = os.getenv("db_host")
        database = os.getenv("db_name")

        SQL_COPT_SS_ACCESS_TOKEN = (
            1256  # Connection option for access tokens, as defined in msodbcsql.h
        )
        TOKEN_URL = (
            "https://database.windows.net/"  # The token URL for any Azure SQL database
        )

        connection_string = (
            f"mssql+pyodbc://{server}/{database}?driver=ODBC+Driver+17+for+SQL+Server"
        )
        # connection_url = sqlalchemy.engine.url.URL('mssql+pyodbc', query={'odbc_connect': odbc_str})

        engine = create_engine(
            connection_string, isolation_level="AUTOCOMMIT", fast_executemany=True
        )

        azure_credentials = identity.DefaultAzureCredential()

        @event.listens_for(engine, "do_connect")
        def provide_token(cargs, cparams):
            print("provide token start")
            # remove the "Trusted_Connection" parameter that SQLAlchemy adds
            cargs[0] = cargs[0].replace(";Trusted_Connection=Yes", "")

            # create token credential
            raw_token = azure_credentials.get_token(TOKEN_URL).token.encode("utf-16-le")
            token_struct = struct.pack(
                f"<I{len(raw_token)}s", len(raw_token), raw_token
            )

            # apply it to keyword arguments
            cparams["attrs_before"] = {SQL_COPT_SS_ACCESS_TOKEN: token_struct}

    else:
        connection_url = sqlalchemy.engine.URL.create(
            "mssql+pyodbc",
            username=os.getenv("db_username"),
            password=os.getenv("db_password"),
            host=os.getenv("db_host"),
            database=os.getenv("db_name"),
            query={
                "driver": "ODBC Driver 17 for SQL Server",
                "autocommit": "True",
            },
        )
        engine = sqlalchemy.create_engine(connection_url).execution_options(
            isolation_level="AUTOCOMMIT"
        )
    return engine


engine = get_engine()
engine.dialect.identifier_preparer.initial_quote = ""
engine.dialect.identifier_preparer.final_quote = ""
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


@as_declarative()
class Base:
    """Base class"""

    @declared_attr
    def __tablename__(self, cls) -> str:
        return cls.__name__.lower()


def get_session():
    """Get session method"""
    with Session(engine) as session:
        yield session
