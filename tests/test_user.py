from basetest import TestUser
from tests.basetest import (questions, get_all_questions, get_answers_for_one_question, get_one_question, post_answer, post_question,\
                 empty_string_answer_post, empty_string_description_post, empty_string_question_post, empty_string_update_question,\
                    wrong_input_answer, wrong_input_description, wrong_input_login, wrong_input_question, wrong_input_sign_up,\
                     wrong_input_update_question, sign_up, login, missing_data_login, missing_data_sign_up)

class Test_User(TestUser):
    def test_user_signup(self):
        response = self.signup_user(sign_up)
        self.assertEqual(response.status_code, 201)