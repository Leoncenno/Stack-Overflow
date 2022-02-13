from http.client import OK
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
        

        except (Exception, psycopg2.DatabaseError) as error:
            print(error)


    def get_all_questions(self):
        self.cur.execute('SELECT * FROM questions')
        all_questions = self.cur.fetchall()
        return all_questions

    def post_a_question(self, question, description):
        self.cur.execute('INSERT INTO questions (question, description) VALUES (%s, %s)', (question, description))
        self.conn.commit()
        return {'question': question, 'description': description}

