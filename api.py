from crypt import methods
from enum import unique
from xml.etree.ElementTree import QName
from flask import Flask, request, jsonify, json
from dbconnect import DbConnect
from flasgger import Swagger
from flasgger.utils import swag_from
from validations import Validation
from werkzeug.security import generate_password_hash


app = Flask(__name__)
app.config["DEBUG"] = True
swagger = Swagger(app)

db = DbConnect()
val = Validation()


@app.route('/api/v1/questions', methods=['GET'])
@swag_from('api_docs/getallquestion.yml')
def all_questions():
    questions = db.get_all_questions()
    return jsonify(questions), 200


@app.route('/api/v1/questions', methods=['POST'])
@swag_from('api_docs/post_question.yml')
def post_question():
    new_q = request.json
    new_question = val.validate(new_q)
    qn = db.post_a_question(
        new_question['question'], new_question['description'])
    return jsonify(qn), 201


@app.route('/api/v1/questions/<id>', methods=['PUT'])
@swag_from('api_docs/update_question.yml')
def update_question(id):
    new_question = request.json
    updated_question = db.update_a_question(id, new_question['question'],)
    return jsonify(updated_question), 201


@app.route('/api/v1/questions/<id>', methods=['GET'])
@swag_from('api_docs/one_question.yml')
def one_question(id):
    question = db.get_one_question(id)
    return jsonify(question), 200


@app.route('/api/v1/questions/<id>/answers', methods=['GET'])
@swag_from('api_docs/allanswers.yml')
def answers(id):
    answers = db.get_all_answers(id)
    return jsonify(answers), 200


@app.route('/api/v1/questions/<id>/answers', methods=['POST'])
@swag_from('api_docs/post_answer.yml')
def post_answer(id):
    new_answer = request.json
    answer = db.post_an_answer(id, new_answer['answer'])
    return jsonify(answer), 201


@app.route('/register', methods=['POST'])
@swag_from('api_docs/create_new_user.yml')
def create_new_user():
    details = request.json
    password_1 = details['password1']
    password_2 = details['password2']
    user_name = details['username']
    Email = details['email']
    if password_1 == password_2:
        password_1 = generate_password_hash(details['password1'])
        db.sign_up(details['firstname'], details['lastname'], Email,
                            password_1, password_2, details['dateofbirth'], user_name)
        return jsonify('Account registered succesfully'), 201
    else:
        return jsonify('Conflicting passwords, please enter and confirm the same password!'), 409


app.run()
