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


# def test_obter_imovel_por_id(conexao, imovel_teste):
#     imovel = obter_imovel_por_id(conexao, imovel_teste)
#     assert imovel is not None
#     assert imovel["id"] == imovel_teste
#     assert imovel["logradouro"] == "Rua de Teste"

def test_adicionar_imovel(client):
    novo_imovel = {
        "logradouro": "Avenida Teste",
        "tipo_logradouro": "Avenida",
        "bairro": "Centro",
        "cidade": "Cidade Teste",
        "cep": "12345-678",
        "tipo": "Apartamento",
        "valor": 250000.00,
        "data_aquisicao": "2025-03-11"
    }
    
    response = client.post("/imoveis", json=novo_imovel)
    assert response.status_code == 201  # Código HTTP para criação bem-sucedida
    
    dados_resposta = response.json
    assert "id" in dados_resposta  # Verifica se um ID foi retornado
    assert dados_resposta["logradouro"] == novo_imovel["logradouro"]
    assert dados_resposta["tipo_logradouro"] == novo_imovel["tipo_logradouro"]
    assert dados_resposta["bairro"] == novo_imovel["bairro"]
    assert dados_resposta["cidade"] == novo_imovel["cidade"]
    assert dados_resposta["cep"] == novo_imovel["cep"]
    assert dados_resposta["tipo"] == novo_imovel["tipo"]
    assert dados_resposta["valor"] == novo_imovel["valor"]
    assert dados_resposta["data_aquisicao"] == novo_imovel["data_aquisicao"]

def test_remover_imovel(client):
    # Primeiro, adiciona um imóvel para garantir que ele existe
    novo_imovel = {
        "logradouro": "Rua Removível",
        "tipo_logradouro": "Rua",
        "bairro": "Bairro X",
        "cidade": "Cidade Y",
        "cep": "98765-432",
        "tipo": "Casa",
        "valor": 150000.00,
        "data_aquisicao": "2025-03-12"
    }
    
    response = client.post("/imoveis", json=novo_imovel)
    assert response.status_code == 201
    imovel_id = response.json["id"]

    response = client.delete(f"/imoveis/{imovel_id}")
    assert response.status_code == 200
    assert response.json["mensagem"] == "Imóvel removido com sucesso"

