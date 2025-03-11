import pytest
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


def test_obter_imovel_por_id(client):
    # Primeiro, vamos adicionar um imóvel para ter certeza que existe um ID
    novo_imovel = {
        "logradouro": "Rua Teste ID",
        "tipo_logradouro": "Rua",
        "bairro": "Bairro Teste",
        "cidade": "Cidade Teste",
        "cep": "12345-678",
        "tipo": "Casa",
        "valor": 300000.00,
        "data_aquisicao": "2025-03-11",
    }

    response = client.post("/imoveis", json=novo_imovel)
    id_imovel = response.json["id"]

    # Agora testamos obter esse imóvel
    imovel = client.get(f"/imoveis/{id_imovel}")
    assert imovel.status_code == 200
    assert imovel.json is not None
    assert imovel.json["id"] == id_imovel


def test_adicionar_imovel(client):
    novo_imovel = {
        "logradouro": "Avenida Teste",
        "tipo_logradouro": "Avenida",
        "bairro": "Centro",
        "cidade": "Cidade Teste",
        "cep": "12345-678",
        "tipo": "Apartamento",
        "valor": 250000.00,
        "data_aquisicao": "2025-03-11",
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


def test_atualizar_imovel(client):
    # Primeiro adiciona um imóvel
    novo_imovel = {
        "logradouro": "Avenida Teste",
        "tipo_logradouro": "Avenida",
        "bairro": "Centro",
        "cidade": "Cidade Teste",
        "cep": "12345-678",
        "tipo": "Apartamento",
        "valor": 250000.00,
        "data_aquisicao": "2025-03-11",
    }
    response = client.post("/imoveis", json=novo_imovel)
    id_imovel = response.json["id"]

    # Depois atualiza esse imóvel
    imovel_atualizado = novo_imovel.copy()
    imovel_atualizado["logradouro"] = "Rua Atualizada"
    imovel_atualizado["valor"] = 280000.00

    response = client.put(f"/imoveis/{id_imovel}", json=imovel_atualizado)
    assert response.status_code == 200
    assert response.json["logradouro"] == "Rua Atualizada"
    assert response.json["valor"] == 280000.00
    assert response.json["id"] == id_imovel


def test_listar_imoveis_por_tipo(client):
    # Adiciona um imóvel
    novo_imovel = {
        "logradouro": "Avenida Teste",
        "tipo_logradouro": "Avenida",
        "bairro": "Centro",
        "cidade": "Cidade Teste",
        "cep": "12345-678",
        "tipo": "apartamento",
        "valor": 250000.00,
        "data_aquisicao": "2025-03-11",
    }
    response = client.post("/imoveis", json=novo_imovel)
    tipo = novo_imovel["tipo"]

    # Busca imóveis por tipo
    response = client.get(f"/imoveis/tipo/{tipo}")
    assert response.status_code == 200
    assert isinstance(response.json, list)

    if response.json:
        assert response.json[0]["tipo"] == tipo


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
        "data_aquisicao": "2025-03-12",
    }

    response = client.post("/imoveis", json=novo_imovel)
    assert response.status_code == 201
    imovel_id = response.json["id"]

    response = client.delete(f"/imoveis/{imovel_id}")
    assert response.status_code == 200
    assert response.json["mensagem"] == "Imóvel removido com sucesso"


def test_listar_imoveis_por_cidade(client):
    cidade_teste = "Cidade Teste"
    response = client.get(f"/imoveis/cidade/{cidade_teste}")
    assert response.status_code == 200

    imoveis = response.json
    assert isinstance(imoveis, list)
    print(imoveis)
    if imoveis:
        assert "id" in imoveis[0]
        assert "logradouro" in imoveis[0]
        assert "tipo_logradouro" in imoveis[0]
        assert "bairro" in imoveis[0]
        assert "cidade" in imoveis[0]
        assert "cep" in imoveis[0]
        assert "tipo" in imoveis[0]
        assert "valor" in imoveis[0]
        assert "data_aquisicao" in imoveis[0]
