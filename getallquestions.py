from xml.etree.ElementTree import QName
from flask import Flask, request, jsonify, json
from dbconnect import DbConnect

app = Flask(__name__)
app.config["DEBUG"] = True

db = DbConnect()

@app.route('/api/v1/questions')
def all_questions():
    questions = db.get_all_questions()
    return jsonify(questions)


@app.route('/api/v1/questions', methods=['POST'])
def post_question():
    new_question = request.json
    qn = db.post_a_question(new_question['question'], new_question['description'])
    return jsonify(qn)


@app.route('/api/v1/questions/<id>', methods=['PUT'])
def update_question(id):
    new_question = request.json
    updated_question = db.update_a_question(id, new_question['question'])
    return jsonify(updated_question)


app.run()
