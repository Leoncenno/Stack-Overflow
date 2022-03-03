from config import TestConfig
from app.api import app

questions = {"question": "What is a test?"}

get_all_questions = {}

get_one_question = {}

get_answers_for_one_question = {}

post_question = {"question": "What is your name?",
                 "description": "A new description name"}

empty_string_question_post = {"question": "", "description": "A new description name"}

empty_string_description_post = {"question": "What is your name?", "description": ""}

wrong_input_question = {"question": "12345", "description": "A new description name"}

wrong_input_description = {"question": "What is your name?", "description": "12345"}

post_answer = {"answer": "A new answer for the question."}

empty_string_answer_post = {"answer": ""}

wrong_input_answer = {"answer": "12345"}

update_question = {"question": "A new update for the question"}

empty_string_update_question = {"question": ""}

wrong_input_update_question = {"question": "123456"}

sign_up = {"firstname": "Smith", "lastname": "Okello", "email": "smith@gmail.com",
                   "password1": "okeli", "password2": "okeli", "dateofbirth": "1994-04-20", "username": "smith"}

wrong_input_sign_up = {"firstname": "Smith", "lastname": "Okello", "email": "smith@gmail.com",
                   "password1": "okeli", "password2": "okeli", "dateofbirth": "1994-20-20", "username": "smith"}

missing_data_sign_up = {"firstname": "Smith", "lastname": "", "email": "smith@gmail.com",
                   "password1": "okeli", "password2": "okeli", "dateofbirth": "1994-04-20", "username": "smith"}

login = {"username": "smith", "password": "okeli"}

wrong_input_login = {"username": "123456", "password": "okeli"}

missing_data_login = {"username": "", "password": "okeli"}




