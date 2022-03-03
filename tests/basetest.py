import unittest
import os
from app.app import app
from tests import (questions, get_all_questions, get_answers_for_one_question, get_one_question, post_answer, post_question,\
                empty_string_answer_post, empty_string_description_post, empty_string_question_post, empty_string_update_question,\
                wrong_input_answer, wrong_input_description, wrong_input_login, wrong_input_question, wrong_input_sign_up,\
                wrong_input_update_question, sign_up, login, missing_data_login, missing_data_sign_up)
import json
import config
from config import TestConfig
from app.dbconnect import DbConnect

app.config.from_object(TestConfig)

db = DbConnect()

class TestUser(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()
        db.create_questions_table()
        db.create_answers_table()
        db.create_user_details_table()

    def tearDown(self):
        clear_questions = "DROP TABLE qustions CASCADE"
        db.cur.execute(clear_questions)
        clear_answers = "DROP TABLE answers CASCADE"
        db.cur.execute(clear_answers)
        clear_user_details = "DROP TABLE user_details CASCADE"
        db.cur.execute(clear_user_details)

    def signup_user(self, sign_up):
        response = self.client.post("/register", data = json.dumps(sign_up), content_type = 'application/json')
        return response

    def signin_user(self, login):
        response = self.client.post("/login", data = json.dumps(login), content_type = 'application/json')
        response_data = json.loads(response.data.decode())
        return response_data["Token"]

    def user_token(self, login):
        response = self.client.post("/login", data = json.dumps(login), content_type = 'application/json')
        response_data = json.loads(response.data.decode())
        return response_data["Token"]

    def post_a_question(self, post_question):
        response = self.client.post("/api/v1/questions", headers={'Authorization': 'Bearer '+ self.user_token(login)}\
        ,data = json.dumps(post_question), content_type = 'application/json')
        return response

    def empty_string_question(self, empty_string_question_post):
        response = self.client.post("/api/v1/questions",headers={'Authorization': 'Bearer '+ self.user_token(login)}\
        ,data = json.dumps(empty_string_question_post), content_type = 'application/json')
        return response
