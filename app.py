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
        an_obj['content'] = post[1]
        an_obj['created_at'] = post[2]
        an_obj['title'] = post[3]
        an_obj['user'] = post[4]
        resp.append(an_obj)
    return jsonify(resp), 200

@app.post('/api/posts')
def posts_post():
    data = request.json
    content = data.get('content')
    created_at = data.get('created_at')
    title = data.get('title')
    user = data.get('user')
    if not content:
        return jsonify("Missing required argument: content"), 422
    if not created_at:
        return jsonify("Missing required argument: created_at"), 422
    if not title:
        return jsonify("Missing required argument: title"), 422
    if not user:
        return jsonify("Missing required field: user"), 422
    run_query("INSERT INTO post (content, created_at, title, user) VALUES(?,?,?,?)", [content, created_at, title, user])
        
    return jsonify("Post created"), 201

@app.patch('/api/posts')
def posts_patch():
    data = request.json
    id = data.get('postId')
    content = data.get('content')
    title = data.get('title')
    run_query("UPDATE post SET content=?, title=? WHERE id=?", [content, title, id])
        
    return jsonify("Post created"), 201

@app.delete('/api/posts')
def posts_delete():
    data = request.json
    postid = data.get('postId')
    run_query("DELETE FROM post WHERE id=?", [postid])
        
    return jsonify("Post created"), 201



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