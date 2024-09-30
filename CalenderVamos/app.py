from flask import Flask, request, jsonify, render_template

app = Flask(__name__)

# Lista para armazenar reuniões
meetings = []

@app.route('/')
def index():
    return render_template('index.html')  # Substitua pelo seu HTML principal

@app.route('/schedule', methods=['POST'])
def schedule():
    data = request.json
    meetings.append(data)
    return jsonify(success=True)

@app.route('/api/meetings', methods=['GET'])
def get_meetings():
    return jsonify(meetings)

if __name__ == '__main__':
    app.run(debug=True)
