from flask import Flask, render_template, jsonify, request
from rq import Queue
from worker import conn
from redis import Redis
import models
from flask_cors import CORS
from utilities import check_pronounceability

app = Flask(__name__)
redis_conn = Redis()
CORS(app)
q = Queue(connection=conn)


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
        print(job_id)
        job = q.fetch_job(job_id)
        if not job.result:
            return jsonify(False)
        return jsonify(pronounceability=job.result)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    # app.run(debug = True)
    app.run()

