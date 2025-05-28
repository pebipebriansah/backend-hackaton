import os
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

load_dotenv()

driver = os.getenv("AZURE_SQL_DRIVER", "ODBC Driver 18 for SQL Server").replace(" ", "+")
server = os.getenv("AZURE_SQL_SERVER")
database = os.getenv("AZURE_SQL_DATABASE")
username = os.getenv("AZURE_SQL_USERNAME")
password = quote_plus(os.getenv("AZURE_SQL_PASSWORD"))

DATABASE_URL = (
    f"mssql+pyodbc://{username}:{password}@{server}:1433/{database}"
    f"?driver={driver}&Encrypt=yes&TrustServerCertificate=no"
)

engine = create_engine(
    DATABASE_URL,
    connect_args={"timeout": 30},
    pool_pre_ping=True,
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
