from flask import Flask, jsonify, request
import mysql.connector
import os
from dotenv import load_dotenv

# Carregar variáveis de ambiente do arquivo .env
load_dotenv()

app = Flask(__name__)

# Configuração do banco de dados
db_config = {
    "host": os.getenv("HOST"),
    "port": os.getenv("PORT"),
    "user": os.getenv("USER"),
    "password": os.getenv("PASSWORD"),
    "database": os.getenv("DATABASE_NAME"),
}


def get_db_connection():
    return mysql.connector.connect(
        host=os.getenv("HOST"),
        user=os.getenv("USER"),
        password=os.getenv("PASSWORD"),
        database=os.getenv("DATABASE_NAME"),
        port=os.getenv("PORT"),
    )


@app.route("/imoveis", methods=["GET"])
def listagem_imoveis():
    conexao = get_db_connection()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM imoveis")
    imoveis = cursor.fetchall()

    cursor.close()
    conexao.close()

    return jsonify(imoveis)


@app.route("/imoveis/<int:id_imovel>", methods=["GET"])
def obter_imovel_por_id(id_imovel):
    """Retorna um imóvel específico pelo seu ID."""
    conexao = get_db_connection()
    cursor = conexao.cursor(dictionary=True)
    cursor.execute("SELECT * FROM imoveis WHERE id = %s", (id_imovel,))
    imovel = cursor.fetchone()
    cursor.close()
    conexao.close()

    if imovel is None:
        return jsonify({"erro": "Imóvel não encontrado"}), 404

    return jsonify(imovel)


@app.route("/imoveis", methods=["POST"])
def adicionar_imovel():
    dados = request.get_json()
    conexao = get_db_connection()
    cursor = conexao.cursor(dictionary=True)

    query = """
    INSERT INTO imoveis (logradouro, tipo_logradouro, bairro, cidade, cep, tipo, valor, data_aquisicao)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    valores = (
        dados["logradouro"],
        dados.get("tipo_logradouro"),
        dados.get("bairro"),
        dados["cidade"],
        dados.get("cep"),
        dados.get("tipo"),
        dados.get("valor"),
        dados.get("data_aquisicao"),
    )

    cursor.execute(query, valores)
    conexao.commit()
    novo_id = cursor.lastrowid
    cursor.close()
    conexao.close()

    dados["id"] = novo_id
    return jsonify(dados), 201


@app.route("/imoveis/<int:id_imovel>", methods=["PUT"])
def atualizar_imovel(id_imovel):
    """Atualiza um imóvel existente pelo seu ID."""
    dados = request.get_json()
    conexao = get_db_connection()
    cursor = conexao.cursor(dictionary=True)

    # Verificar se o imóvel existe
    cursor.execute("SELECT * FROM imoveis WHERE id = %s", (id_imovel,))
    if not cursor.fetchone():
        cursor.close()
        conexao.close()
        return jsonify({"erro": "Imóvel não encontrado"}), 404

    query = """
    UPDATE imoveis SET
    logradouro = %s,
    tipo_logradouro = %s,
    bairro = %s,
    cidade = %s,
    cep = %s,
    tipo = %s,
    valor = %s,
    data_aquisicao = %s
    WHERE id = %s
    """
    valores = (
        dados["logradouro"],
        dados["tipo_logradouro"],
        dados["bairro"],
        dados["cidade"],
        dados["cep"],
        dados["tipo"],
        dados["valor"],
        dados["data_aquisicao"],
        id_imovel,
    )

    cursor.execute(query, valores)
    conexao.commit()
    cursor.close()
    conexao.close()

    dados["id"] = id_imovel
    return jsonify(dados)


@app.route("/imoveis/tipo/<tipo>", methods=["GET"])
def listar_imoveis_por_tipo(tipo):
    """Lista todos os imóveis de um determinado tipo."""
    conexao = get_db_connection()
    cursor = conexao.cursor(dictionary=True)

    cursor.execute("SELECT * FROM imoveis WHERE tipo = %s", (tipo,))
    imoveis = cursor.fetchall()

    cursor.close()
    conexao.close()

    return jsonify(imoveis)


if __name__ == "__main__":
    app.run(debug=True)
