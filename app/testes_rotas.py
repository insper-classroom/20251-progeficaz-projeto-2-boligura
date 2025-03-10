import pytest
import os
from dotenv import load_dotenv
import mysql.connector
from servidor import listar_todos_imoveis

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


def test_listagem_imoveis(conexao):
    imoveis = listar_todos_imoveis(conexao)
    # Verifica se o retorno é uma lista
    assert isinstance(imoveis, list)

    # Se houver imóveis, verifica se o primeiro item é um dicionário
    if imoveis:
        assert isinstance(imoveis[0], dict)

    # Opcional: verificar se a chave "id" está presente nos dicionários retornados
    for imovel in imoveis:
        assert "id" in imovel
        assert "logradouro" in imovel
