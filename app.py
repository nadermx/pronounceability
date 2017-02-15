from flask import Flask, render_template, jsonify, request
from rq import Queue
from flask_cors import CORS
from utilities import check_pronounceability
import rq_dashboard
from redis import Redis

app = Flask(__name__)
app.config.from_object(rq_dashboard.default_settings)
app.register_blueprint(rq_dashboard.blueprint, url_prefix="/rq")
CORS(app)
conn = Redis()
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
        print(word)
        db_word = models.Word.get(word=word)
        if not db_word:
            job = q.enqueue(check_pronounceability, args=(word,))
            return jsonify(job=job.id)
        else:
            return jsonify(pronounceability=db_word.pronounceability)
    if request.method == "GET":
        job_id = request.args.get('job_id')
        job = q.fetch_job(job_id)
        if not job:
            return jsonify('no job id')
        if job.is_finished:
            return jsonify(pronounceability=job.result)
        if job.is_failed:
            return jsonify(pronounceability='Error')
        return jsonify(False)

if __name__ == '__main__':
    # app.run(host='0.0.0.0', port=5000, debug=True)
    app.run(debug = True)
    # app.run()

