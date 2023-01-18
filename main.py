import datetime
import os

from dotenv import load_dotenv
from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy

MYSQL_URI = os.getenv("MYSQL_URI")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = MYSQL_URI
db = SQLAlchemy(app)


class Posts(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text)
    content = db.Column(db.Text)
    date_posted = db.Column(db.DateTime)


def test_connection():
    with app.app_context():
        db.create_all()


def get_posts():
    posts_data = Posts.query.all()
    posts = [{"id": post.id, "title": post.title, "content": post.content, "date_posted": post.date_posted} for post in
             posts_data]
    return posts


@app.route('/')
def index():
    return render_template("index.html", posts=get_posts())


@app.route('/api/posts', methods=["GET", "POST"])
def posts_api():
    if request.method == "GET":
        posts = get_posts()
        return {"success": True, "posts": posts}
    if request.method == "POST":
        try:
            request_data = request.json
            new_post = Posts(title=request_data["title"], content=request_data["content"], date_posted=datetime.datetime.now())
            db.session.add(new_post)
            db.session.commit()
            return {"success": True, "msg": "Successfully added new post."}, 200
        except KeyError:
            return {"success": False, "error": "Please include title and content in request body."}


if __name__ == "__main__":
    app.run(debug=True)