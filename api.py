from crypt import methods
from xml.etree.ElementTree import QName
from flask import Flask, request, jsonify, json
from dbconnect import DbConnect
from flasgger import Swagger
from flasgger.utils import swag_from


app = Flask(__name__)
app.config["DEBUG"] = True
swagger = Swagger(app)

db = DbConnect()

@app.route('/api/v1/questions', methods=['GET'])
@swag_from('api_docs/getallquestion.yml')
def all_questions():
    questions = db.get_all_questions()
    return jsonify(questions)


@app.route('/api/v1/questions', methods=['POST'])
@swag_from('api_docs/post_question.yml')
def post_question():
    new_question = request.json
    qn = db.post_a_question(new_question['question'], new_question['description'])
    return jsonify(qn)


@app.route('/api/v1/questions/<id>', methods=['PUT'])
@swag_from('api_docs/update_question.yml')
def update_question(id):
    new_question = request.json
    updated_question = db.update_a_question(id, new_question['question'],)
    return jsonify(updated_question)


@app.route('/api/v1/questions/<id>', methods=['GET'])
@swag_from('api_docs/one_question.yml')
def one_question(id):
    question = db.get_one_question(id)
    return jsonify(question)


@app.route('/api/v1/questions/<id>/answers', methods=['GET'])
@swag_from('api_docs/allanswers.yml')
def answers(id):
    answers = db.get_all_answers(id)
    return jsonify(answers)


@app.route('/api/v1/questions/<id>/answers', methods=['POST'])
@swag_from('api_docs/post_answer.yml')
def post_answer(id):
    new_answer = request.json
    answer = db.post_an_answer(id, new_answer['answer'])
    return jsonify(answer)


app.run()
