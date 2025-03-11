from flask import Flask, jsonify
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

# Rota para listar todos os imóveis
@app.route('/imoveis', methods=['GET'])
def listagem_imoveis():
    conn = mysql.connector.connect(**db_config)
    cursor = conn.cursor(dictionary=True)

    cursor.execute("SELECT * FROM imoveis")
    imoveis = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(imoveis)  # Agora retorna JSON corretamente

if __name__ == '__main__':
    app.run(debug=True)
