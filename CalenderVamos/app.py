from flask import Flask, request, jsonify, render_template
import mysql.connector
from mysql.connector import Error
import os

app = Flask(__name__)

# Configurações do banco de dados
db_config = {
    'host': 'localhost',
    'database': 'calendario',
    'user': 'root',
    'password': '1nfr4@v4m05'
}

# Função para conectar ao banco de dados
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(**db_config)
        print("Conexão com o MySQL bem-sucedida")
    except Error as e:
        print(f"Erro: '{e}'")
    return connection

# Rota inicial para renderizar a página index.html
@app.route('/')
def index():
    return render_template('index.html')

# Rota para agendar uma reunião (POST)
@app.route('/api/meetings', methods=['POST'])
def schedule():
    if not request.json:
        return jsonify(success=False, error="Formato JSON inválido"), 400

    data = request.json
    title = data.get('title')
    start = data.get('start')
    end = data.get('end')
    email = data.get('email')

    connection = create_connection()
    if connection:
        try:
            cursor = connection.cursor()
            query = """
            INSERT INTO meetings (title, start, end, email) 
            VALUES (%s, %s, %s, %s)
            """
            cursor.execute(query, (title, start, end, email))
            connection.commit()
            cursor.close()
        except Error as e:
            return jsonify(success=False, error=str(e)), 500
        finally:
            connection.close()

    return jsonify(success=True)

# Rota para obter todas as reuniões (GET)
@app.route('/api/meetings', methods=['GET'])
def get_meetings():
    connection = create_connection()
    meetings = []

    if connection:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT * FROM meetings")
        meetings = cursor.fetchall()
        cursor.close()
        connection.close()

    return jsonify(meetings)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
