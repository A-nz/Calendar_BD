from flask import Flask
from flask import request, render_template, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy


class Config:
    SQLALCHEMY_DATABASE_URI = "postgresql://postgres:AND111000@localhost/Calendar"
    #SQLALCHEMY_DATABASE_URI = 'sqlite:///app.db'
    SQLALCHEMY_COMMIT_ON_TEARDOWN = False # Autocommit
    SQLALCHEMY_TRACK_MODIFICATIONS = False # ??? Если не прописать, то будет Warning
    SECRET_KEY = 'we4fh%gC_za:*8G5v=fbv'


app = Flask(__name__)
app.config.from_object(Config())
db = SQLAlchemy(app=app, session_options={'autoflush': False})


# @app.route('/')
# def index():
#     return render_template("menu.html")
#
#
# @app.route('/index')
# def about():
#     return render_template("mypage.html")
#
#
# @app.route('/create-article')
# def create_article():
#     return render_template("create-event.html")


# if __name__ == '__main__':
#     app.run(debug=True)

