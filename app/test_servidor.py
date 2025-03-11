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
    response = client.get("/imoveis")
    assert response.status_code == 200
    assert isinstance(response.json, list)  # Verifica se o retorno é uma lista

    if response.json:
        assert "id" in response.json[0]  # Verifica se há a chave "id"


def test_obter_imovel_por_id(conexao, imovel_teste):
    imovel = obter_imovel_por_id(conexao, imovel_teste)
    assert imovel is not None
    assert imovel["id"] == imovel_teste
    assert imovel["logradouro"] == "Rua de Teste"

def test_adicionar_imovel(client):
    novo_imovel = {
        "logradouro": "Avenida Teste",
        "numero": 123,
        "cidade": "Cidade Teste",
        "estado": "TS",
        "preco": 250000.00,
        "tipo": "Apartamento"
    }
    
    response = client.post("/imoveis", json=novo_imovel)
    assert response.status_code == 201  # Código HTTP para criação bem-sucedida
    
    dados_resposta = response.json
    assert "id" in dados_resposta  # Verifica se um ID foi retornado
    assert dados_resposta["logradouro"] == novo_imovel["logradouro"]
    assert dados_resposta["numero"] == novo_imovel["numero"]
    assert dados_resposta["cidade"] == novo_imovel["cidade"]
    assert dados_resposta["estado"] == novo_imovel["estado"]
    assert dados_resposta["preco"] == novo_imovel["preco"]
    assert dados_resposta["tipo"] == novo_imovel["tipo"]

