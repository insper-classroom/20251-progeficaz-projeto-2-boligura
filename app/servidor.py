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
    INSERT INTO imoveis (logradouro, numero, cidade, estado, preco, tipo)
    VALUES (%s, %s, %s, %s, %s, %s)
    """
    valores = (
        dados["logradouro"],
        dados["numero"],
        dados["cidade"],
        dados["estado"],
        dados["preco"],
        dados["tipo"]
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
