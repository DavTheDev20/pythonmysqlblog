import datetime
import traceback

from flask import Flask, render_template, request
from flask_cors import CORS
from database import db_session, init_db
from models import Posts

app = Flask(__name__)
CORS(app)

init_db()


def get_posts():
    posts_data = Posts.query.all()
    posts = [
        {
            "id": post.id,
            "title": post.title,
            "content": post.content,
            "date_posted": post.date_posted,
        }
        for post in posts_data
    ]
    return posts


@app.route("/")
def index():
    return render_template("index.html", posts=get_posts())


@app.route("/api/posts", methods=["GET", "POST"])
def posts_api():
    if request.method == "GET":
        posts = get_posts()
        return {"success": True, "posts": posts}
    if request.method == "POST":
        try:
            request_data = request.json
            new_post = Posts(
                title=request_data["title"],
                content=request_data["content"],
                date_posted=datetime.datetime.now(),
            )
            db_session.add(new_post)
            db_session.commit()
            return {"success": True, "msg": "Successfully added new post."}, 200
        except KeyError:
            return {
                "success": False,
                "error": "Please include title and content in request body.",
            }


@app.route('/api/posts/<post_id>', methods=["GET", "PUT", "DELETE"])
def manipulate_post(post_id):
    if request.method == "GET":
        post_data = db_session.query(Posts).get(post_id)
        post = {"id": post_data.id, "title": post_data.title, "content": post_data.content, "date_posted": post_data.date_posted}
        return {"success": True, "post": post}
    elif request.method == "DELETE":
        try:
            post = db_session.query(Posts).get(post_id)
            db_session.delete(post)
            db_session.commit()
            return {"success": True}
        except Exception:
            return {"success": False, "error": traceback.format_exc()}


@app.teardown_appcontext
def shutdown_session(exception=None):
    db_session.remove()


if __name__ == "__main__":
    app.run(debug=True)
