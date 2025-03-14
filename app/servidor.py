from flask import Flask, jsonify, request, abort
import mysql.connector
import os
from dotenv import load_dotenv
import re 
from datetime import datetime

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
    validar_dados_imovel(dados)  # Chama a validação antes de inserir no banco

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

    cursor.execute("SELECT * FROM imoveis WHERE LOWER(tipo) = LOWER(%s)", (tipo,))
    imoveis = cursor.fetchall()

    cursor.close()
    conexao.close()

    return jsonify(imoveis)


if __name__ == "__main__":
    app.run(debug=True)

@app.route("/imoveis/<int:id>", methods=["DELETE"])
def remover_imovel(id):
    conexao = get_db_connection()
    cursor = conexao.cursor()

    # Verifica se o imóvel existe
    cursor.execute("SELECT id FROM imoveis WHERE id = %s", (id,))
    if not cursor.fetchone():
        cursor.close()
        conexao.close()
        return jsonify({"mensagem": "Imóvel não encontrado"}), 404  # Corrigido para retornar 404

    # Remove o imóvel
    cursor.execute("DELETE FROM imoveis WHERE id = %s", (id,))
    conexao.commit()

    cursor.close()
    conexao.close()

    return jsonify({"mensagem": "Imóvel removido com sucesso"}), 200


@app.route("/imoveis/cidade/<string:cidade>", methods=["GET"])
def listar_imoveis_por_cidade(cidade):
    conexao = get_db_connection()
    cursor = conexao.cursor(dictionary=True)
    
    cursor.execute("SELECT * FROM imoveis WHERE cidade = %s", (cidade,))
    imoveis = cursor.fetchall()
    
    cursor.close()
    conexao.close()
    
    return jsonify(imoveis)

def validar_dados_imovel(dados):
    """Valida os dados antes de adicionar ou atualizar um imóvel."""
    
    # Campos obrigatórios
    campos_obrigatorios = ["logradouro", "tipo_logradouro", "bairro", "cidade", "cep", "tipo", "valor", "data_aquisicao"]
    
    for campo in campos_obrigatorios:
        if campo not in dados or not dados[campo]:
            abort(400, description=f"O campo '{campo}' é obrigatório.")

    # Validação do CEP (deve ter o formato XXXXX-XXX)
    if not re.match(r"^\d{5}-\d{3}$", dados["cep"]):
        abort(400, description="O CEP deve estar no formato 00000-000.")

    # Validação do tipo (opcional, mas útil)
    tipos_permitidos = {"Apartamento", "Casa", "Terreno"}
    if dados["tipo"] not in tipos_permitidos:
        abort(400, description=f"Tipo inválido. Tipos permitidos: {', '.join(tipos_permitidos)}.")

    # Validação do valor (não pode ser negativo)
    if dados["valor"] < 0:
        abort(400, description="O valor do imóvel não pode ser negativo.")

    # Validação da data de aquisição (não pode estar no futuro)
    data_atual = datetime.today().date()
    try:
        data_aquisicao = datetime.strptime(dados["data_aquisicao"], "%Y-%m-%d").date()
        if data_aquisicao > data_atual:
            abort(400, description="A data de aquisição não pode estar no futuro.")
    except ValueError:
        abort(400, description="Formato de data inválido. Use 'YYYY-MM-DD'.")
