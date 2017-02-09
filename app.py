from flask import Flask, render_template, jsonify, request
from rq import Queue
from rq.job import Job
from worker import conn
from flask_cors import CORS
from utilities import check_pronounceability

app = Flask(__name__)
CORS(app)
q = Queue(connection=conn)

import models

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/word', methods=['POST', 'GET'])
@models.db_session
def check():
    if request.method == "POST":
        word = request.form['word']
        if not word:
            return render_template('index.html')
        db_word = models.Word.get(word=word)
        if not db_word:
            job = q.enqueue_call(check_pronounceability, args=(word,))
            return jsonify(job=job.id)
        else:
            return jsonify(pronounceability=db_word.pronounceability)
    if request.method == "GET":
        job_id = request.args.get('job_id')
        job = Job.fetch(job_id, connection=conn)
        if job.is_finished:
            return jsonify(pronounceability= job.result)
        else:
            return jsonify(False)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug = True)
    # app.run()

