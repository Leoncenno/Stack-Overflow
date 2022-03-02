from flask import jsonify
from werkzeug.security import generate_password_hash
from datetime import datetime

class Validators():
    def validate_missing_post(self, post):
        if post.isspace():
            return True
        else:
            return False

    def validate_empty_post(self, post):
        if post == '':
            return True
        else:
            return False

    def remove_spaces(self, input_string):
        input_string = input_string.strip()
        return input_string

    def validate_nonstring_input(self, post):
        if post.isdigit():
            return True
        else:
            return False

    def validate_date_of_birth_format(self, date_string):
        try:
            bool(datetime.strptime(date_string, "%Y-%m-%d"))
            return True
        except ValueError:
            return False
       