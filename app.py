from flask import Flask, render_template, jsonify, request
from rq import Queue
from redis import Redis
from worker import check_pronounceability
import models

app = Flask(__name__)
redis_conn = Redis()
q = Queue(connection=redis_conn)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/word', methods=['POST', 'GET'])
@models.db_session
def check():
    if request.method == "POST":
        word = request.form['word']
        db_word = models.Word.get(word=word)
        if not db_word:
            job = q.enqueue(check_pronounceability, word)
            return jsonify(job_id =job.id)
        else:
            return jsonify(pronounceability=db_word.pronounceability)
    if request.method == "GET":
        job_id = request.args.get('job_id')
        job = q.fetch_job(job_id)
        if not job.result:
            return jsonify(False)
        return jsonify(pronounceability=job.result)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug = True)
    # app.run()

