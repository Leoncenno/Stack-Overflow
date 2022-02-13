from flask import Flask, request, jsonify, json
from dbconnect import DbConnect

app = Flask(__name__)
app.config["DEBUG"] = True

db = DbConnect()

@app.route('/api/v1/questions')
def all_questions():
    questions = db.get_all_questions()
    return jsonify(questions)

app.run()
