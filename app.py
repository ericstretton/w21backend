from helpers.db_helpers import run_query
from flask import Flask, jsonify, request 
from flask_cors import CORS
import sys

app = Flask(__name__)

@app.get('/api/posts')
def posts_get():
    post_list = run_query("SELECT * FROM post")
    resp = []
    for post in post_list:
        an_obj = {}
        an_obj['postId'] = post[0]
        resp.append(an_obj)
    return jsonify(resp), 200

@app.post('/api/posts')
def posts_post():
    return True

@app.patch('/api/posts')
def posts_patch():
    return True

@app.delete('/api/posts')
def posts_delete():
    return True



if len(sys.argv) > 1:
    mode = sys.argv[1]
else:
    print("Missing required mode argument")
    exit()
if mode == 'testing':
    CORS(app)
    app.run(debug=True)
elif mode == 'production':
    import bjoern
    bjoern.run(app, "0.0.0.0", 5010)
else:
    print("Mode must be in testing|production")
    exit()