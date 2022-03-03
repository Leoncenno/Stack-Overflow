from crypt import methods
from enum import unique
from xml.etree.ElementTree import QName
from flask import Flask, request, jsonify, json
from app.dbconnect import DbConnect
from flasgger import Swagger
from flasgger.utils import swag_from
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, JWTManager, jwt_required
from decouple import config
from app.validations import Validators


app = Flask(__name__)
app.config["DEBUG"] = True
swagger = Swagger(app)
app.config["JWT_SECRET_KEY"] = config('SECRET_KEY')
jwt = JWTManager(app)

db = DbConnect()
val = Validators()


@app.route('/api/v1/questions', methods=['GET'])
@swag_from('api_docs/getallquestion.yml')
@jwt_required()
def all_questions():
    questions = db.get_all_questions()
    return jsonify(questions), 200


@app.route('/api/v1/questions', methods=['POST'])
@swag_from('api_docs/post_question.yml')
@jwt_required()
def post_question():
    new_question = request.json
    is_question_empty = val.validate_missing_post(new_question['question'])
    is_description_empty = val.validate_missing_post(
        new_question['description'])
    is_question_empty_string = val.validate_empty_post(
        new_question['question'])
    is_description_empty_string = val.validate_empty_post(
        new_question['description'])
    is_question_string = val.validate_nonstring_input(new_question['question'])
    is_description_string = val.validate_nonstring_input(
        new_question['description'])
    if is_question_empty:
        return jsonify('Txt area cannot be empty! Enter the question.'), 406
    if is_description_empty:
        return jsonify('Txt area cannot be empty! Enter the question description.'), 406
    if is_question_empty_string:
        return jsonify('Txt area cannot be empty! Enter the question'), 406
    if is_description_empty_string:
        return jsonify('Txt area cannot be empty! Enter the question description.'), 406
    if is_question_string:
        return jsonify('Question cannot be numbers only!'), 406
    if is_description_string:
        return jsonify('Description cannot be numbers only!'), 406
    else:
        qn = db.post_a_question(
            val.remove_spaces(new_question['question']), val.remove_spaces(new_question['description']))
        return jsonify(qn), 201


@app.route('/api/v1/questions/<id>', methods=['PUT'])
@swag_from('api_docs/update_question.yml')
@jwt_required()
def update_question(id):
    new_question = request.json
    is_question_empty = val.validate_missing_post(new_question['question'])
    is_question_empty_string = val.validate_empty_post(
        new_question['question'])
    is_question_string = val.validate_nonstring_input(new_question['question'])
    is_id_string = val.validate_nonstring_input(id)
    if is_id_string is False:
        return jsonify('Question ID can only be an interger!')
    if is_question_empty:
        return jsonify('Txt area cannot be empty! Please type in question'), 406
    if is_question_empty_string:
        return jsonify('Txt area cannot be empty! Please type in question'), 406
    if is_question_string:
        return jsonify('Question cannot be numbers only!'), 406
    else:
        updated_question = db.update_a_question(
            id, val.remove_spaces(new_question['question']))
        return jsonify(updated_question), 201


@app.route('/api/v1/questions/<id>', methods=['GET'])
@swag_from('api_docs/one_question.yml')
@jwt_required()
def one_question(id):
    is_id_string = val.validate_nonstring_input(id)
    if is_id_string is False:
        return jsonify('Question ID can only be an interger!')
    else:
        question = db.get_one_question(id)
        return jsonify(question), 200


@app.route('/api/v1/questions/<id>/answers', methods=['GET'])
@swag_from('api_docs/allanswers.yml')
@jwt_required()
def answers(id):
    is_id_string = val.validate_nonstring_input(id)
    if is_id_string is False:
        return jsonify('Question ID can only be an interger!')
    else:
        answers = db.get_all_answers(id)
        return jsonify(answers), 200


@app.route('/api/v1/questions/<id>/answers', methods=['POST'])
@swag_from('api_docs/post_answer.yml')
@jwt_required()
def post_answer(id):
    new_answer = request.json
    is_id_string = val.validate_nonstring_input(id)
    is_answer_empty = val.validate_missing_post(new_answer['answer'])
    is_answer_empty_string = val.validate_empty_post(new_answer['answer'])
    is_answer_string = val.validate_nonstring_input(new_answer['answer'])
    if is_id_string is False:
        return jsonify('Question ID can only be an interger!')
    if is_answer_empty:
        return jsonify('Txt area cannot be empty! Please type in answer'), 406
    if is_answer_empty_string:
        return jsonify('Txt area cannot be empty! Please typ in answer'), 406
    if is_answer_string:
        return jsonify('Question cannot be numbers only!'), 406
    else:
        answer = db.post_an_answer(id, val.remove_spaces(new_answer['answer']))
        return jsonify(answer), 201


@app.route('/register', methods=['POST'])
@swag_from('api_docs/create_new_user.yml')
def create_new_user():
    details = request.json
    password_1 = details['password1']
    password_2 = details['password2']
    user_name = val.remove_spaces(details['username'])
    email = val.remove_spaces(details['email'])
    date_of_birth = details['dateofbirth']
    first_name = val.remove_spaces(details['firstname'])
    last_name = val.remove_spaces(details['lastname'])

    is_lastname_empty = val.validate_missing_post(last_name)
    is_lastname_empty_string = val.validate_empty_post(last_name)
    is_lastname_string = val.validate_nonstring_input(last_name)

    is_firsttname_empty = val.validate_missing_post(first_name)
    is_firsttname_empty_string = val.validate_empty_post(first_name)
    is_firsttname_string = val.validate_nonstring_input(first_name)

    is_dateofbirth_empty = val.validate_missing_post(date_of_birth)
    is_dateofbirth_empty_string = val.validate_empty_post(date_of_birth)
    is_dateofbirth_correct_format = val.validate_date_of_birth_format(
        date_of_birth)

    is_email_empty = val.validate_missing_post(email)
    is_email_empty_string = val.validate_empty_post(email)
    is_email_string = val.validate_nonstring_input(email)

    is_username_empty = val.validate_missing_post(user_name)
    is_username_empty_string = val.validate_empty_post(user_name)
    is_username_string = val.validate_nonstring_input(user_name)

    if is_lastname_empty:
        return jsonify('Please enter your last name'), 406
    if is_lastname_empty_string:
        return jsonify('Please enter your last name'), 406
    if is_lastname_string:
        return jsonify('Your Last name cannot be numbers!'), 406
    if is_firsttname_empty:
        return jsonify('Please enter your first name'), 406
    if is_firsttname_empty_string:
        return jsonify('Please enter your first name'), 406
    if is_firsttname_string:
        return jsonify('Your first name cannot be numbers!'), 406
    if is_dateofbirth_empty:
        return jsonify('Please enter your date of birth'), 406
    if is_dateofbirth_empty_string:
        return jsonify('Please enter your date of birth'), 406
    if is_dateofbirth_correct_format is False:
        return jsonify('Incorrect date format, enter date as YYYY-MM-DD'), 406
    if is_email_empty:
        return jsonify('Please enter your email'), 406
    if is_email_empty_string:
        return jsonify('Please enter your email'), 406
    if is_email_string:
        return jsonify('Email cannot be numbers!'), 406
    if is_username_empty:
        return jsonify('Please enter a username'), 406
    if is_username_empty_string:
        return jsonify('Please enter a username'), 406
    if is_username_string:
        return jsonify('Please enter a valid username!'), 406
    if password_1 != password_2:
        return jsonify('Different passwords, please enter and confirm the same password!'), 409
    else:
        password = generate_password_hash(password_1)
        db.sign_up(first_name, last_name, email,
                   password, password, date_of_birth, user_name)
        return jsonify('Account registered succesfully'), 201


@app.route('/login', methods=['POST'])
def log_in():
    username = request.json["username"]

    is_username_empty = val.validate_missing_post(username)
    is_username_empty_string = val.validate_empty_post(username)
    is_username_string = val.validate_nonstring_input(username)
    if is_username_empty:
        return jsonify('Please enter a username'), 406
    if is_username_empty_string:
        return jsonify('Please enter a username'), 406
    if is_username_string:
        return jsonify('Please enter a valid username!'), 406
    else:
        user = db.check_for_user(username)
        is_correct_password = check_password_hash(
            user['password'], request.json["password"])
        if is_correct_password:
            access_token = create_access_token(identity=username)
            return jsonify({'Token': access_token}), 200
        else:
            return jsonify('Wrong username or password'), 401

if __name__ == '__main__':
    app.run()
