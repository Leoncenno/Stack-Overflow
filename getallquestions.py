from flask import Flask, request, jsonify, json
from model import questions

app = Flask(__name__)
app.config["DEBUG"] = True


@app.route('/api/v1/questions')
def all_questions():
    return jsonify(questions)

app.run()
