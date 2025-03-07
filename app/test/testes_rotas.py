import pytest
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

service_URI = os.getenv("SERVICE_URI")
database_name = os.getenv("DATABASE_NAME")
host = os.getenv("HOST")
port = os.getenv("PORT")
user = os.getenv("USER")
password = os.getenv("PASSWORD")


@pytest.fixture
def conexao():
    return mysql.connector.connect(
        host=host, user=user, password=password, database=database_name
    )
