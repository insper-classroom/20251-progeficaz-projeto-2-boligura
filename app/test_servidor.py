import pytest
import mysql.connector
import os
from dotenv import load_dotenv
from servidor import app

load_dotenv()

@pytest.fixture
def client():
    app.testing = True
    return app.test_client()

def test_listagem_imoveis(client):
    response = client.get('/imoveis')
    assert response.status_code == 200
    assert isinstance(response.json, list)  # Verifica se o retorno é uma lista

    if response.json:
        assert "id" in response.json[0]  # Verifica se há a chave "id"

