from flask import Flask, render_template, request, jsonify
from question import answer

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    question_text = request.form['question']
    chat_response = answer(question_text)
    return jsonify(answer=chat_response)  

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/ask', methods=['POST'])
def ask():
    question_text = request.form['question']
    response = answer(question_text)
    return jsonify(answer=response)