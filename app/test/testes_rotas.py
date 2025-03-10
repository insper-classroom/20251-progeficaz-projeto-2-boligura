import pytest
import os
from dotenv import load_dotenv
import mysql.connector

load_dotenv()

SERVICE_URI = os.getenv("SERVICE_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME")
HOST = os.getenv("HOST")
PORT = os.getenv("PORT")
USER = os.getenv("USER")
PASSWORD = os.getenv("PASSWORD")


@pytest.fixture
def conexao():
    return mysql.connector.connect(
        host=HOST, user=USER, password=PASSWORD, database=DATABASE_NAME
    )
