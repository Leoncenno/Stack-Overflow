from enum import unique
import psycopg2.extras
import psycopg2
import config
from decouple import config


dbhost = config('HOST')
dbdatabase = config('DATABASE')
dbuser = config('USER')
dbpassword = config('PASSWORD')


class DbConnect():  # connect to the StackOverflow database
    def __init__(self):
        """Connect to the StackOverflow Database Server"""

        try:
            self.conn = None
            params = config  # read connection parameters

            # connect to StackOverflow server
            print('connecting to StackOverflow Database...')
            self.conn = psycopg2.connect(
                host=dbhost,
                database=dbdatabase,
                user=dbuser,
                password=dbpassword)

            self.cur = self.conn.cursor(
                cursor_factory=psycopg2.extras.RealDictCursor)  # create a cursor
            self.conn.autocommit = True

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)

    def get_all_questions(self):
        self.cur.execute('SELECT * FROM questions')
        all_questions = self.cur.fetchall()
        return all_questions

    def post_a_question(self, question, description):
        self.cur.execute(
            'INSERT INTO questions (question, description) VALUES (%s, %s)', (question, description))
        return {'question': question, 'description': description}

    def update_a_question(self, question_id, question):
        self.cur.execute(
            'SELECT * FROM questions WHERE question_id = %s', question_id)
        chk = self.cur.fetchone()
        if chk != None:
            self.cur.execute(
                'UPDATE questions SET question = %s WHERE question_id = %s', (question, question_id))
            return {'question': question}
        else:
            return 'Question doesnt exist!'

    def get_one_question(self, question_id):
        self.cur.execute(
            'SELECT * FROM questions WHERE question_id = %s', question_id)
        one_question = self.cur.fetchone()
        if one_question != None:
            return one_question
        else:
            return 'Question doesnt exist!'

    def get_all_answers(self, question_id):
        self.cur.execute(
            'SELECT * FROM answers WHERE question_id = %s', question_id)
        answers = self.cur.fetchall()
        if answers != None:
            return answers
        else:
            return 'No answers for this question!'

    def post_an_answer(self, question_id, answer):
        self.cur.execute(
            'SELECT * FROM questions WHERE question_id = %s', question_id)
        chk = self.cur.fetchone()
        if chk != None:
            self.cur.execute(
                'INSERT INTO answers (question_id, answer) VALUES (%s, %s)', (question_id, answer))
            return answer

    def sign_up(self, firstname, lastname, email, password1, password2, dateofbirth, username):
        self.cur.execute('INSERT INTO user_details (first_name, last_name, email, password, confirm_password, date_of_birth, user_name) VALUES (%s, %s, %s, %s, %s, %s, %s)',
                         (firstname, lastname, email, password1, password2, dateofbirth, username))
    
    def check_for_user(self, username):
        self.cur.execute("SELECT * FROM user_details WHERE user_name = '{}'".format(username))
        chk = self.cur.fetchone()
        return chk