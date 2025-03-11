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
    "port": os.getenv('PORT'),
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
        port = os.getenv('PORT'),
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
        dados.get("data_aquisicao")
    )
    
    cursor.execute(query, valores)
    conexao.commit()
    novo_id = cursor.lastrowid
    cursor.close()
    conexao.close()
    
    dados["id"] = novo_id
    return jsonify(dados), 201
if __name__ == '__main__':
    app.run(debug=True)

@app.route("/imoveis/<int:id>", methods=["DELETE"])
def remover_imovel(id):
    conexao = get_db_connection()
    cursor = conexao.cursor()
    
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