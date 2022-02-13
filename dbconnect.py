import psycopg2
import config

class DbConnect(): #connect to the StackOverflow database
    def __init__(self):
        """Connect to the StackOverflow Database Server"""
        
        try:
            self.conn = None
            params = config #read connection parameters

            print('connecting to StackOverflow Database...') #connect to StackOverflow server
            self.conn = psycopg2.connect(
                host="localhost",
                database="StackOverflow",
                user="postgres",
                password="root")

            self.cur = self.conn.cursor() #create a cursor
            self.conn.autocommit = True
        

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


    def get_all_questions(self):
        self.cur.execute('SELECT * FROM questions')
        all_questions = self.cur.fetchall()
        return all_questions

    def post_a_question(self, question, description):
        self.cur.execute('INSERT INTO questions (question, description) VALUES (%s, %s)', (question, description))
        return {'question': question, 'description': description}

    def update_a_question(self, question_id, question):
        self.cur.execute('SELECT * FROM questions WHERE question_id = %s', question_id)
        chk = self.cur.fetchone()
        if chk != None:
            self.cur.execute('UPDATE questions SET question = %s WHERE question_id = %s', (question, question_id))
            return {'question': question}
        else:
            return 'Question doesnt exist!'

    def get_one_question(self, question_id):
        self.cur.execute('SELECT * FROM questions WHERE question_id = %s', question_id)
        one_question = self.cur.fetchone()
        if one_question != None:
            return {'id': question_id, 'question': one_question[1], 'description': one_question[2]}
        else:
            return 'Question doesnt exist!'


