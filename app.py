from app_config import app, db
import models
from models import *

# from forms import CategoryForm, NewsForm

from flask import request, render_template, redirect, url_for, flash

from flask_login import LoginManager, login_required, login_user, logout_user, current_user
from datetime import datetime
from sqlalchemy import desc

# flask-login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"


# login page
@app.route("/login", methods=["GET", "POST"])
def login():
    feedback = ''
    if request.method == 'POST':
        if request.form['cmd'] == 'Вход':
            u = db.session.query(User).\
                filter(User.login == request.form['login']).\
                filter(User.password == request.form['password']).\
                one_or_none()
            if u is None:
                feedback = "Неверное имя пользователя или пароль"
            else:
                login_user(u)
                return redirect(request.args.get("next") or url_for('menu'))

    return render_template('login.html', feedback=feedback)



@app.route("/register", methods=["POST", "GET"])
def register():
    if request.method == "POST":
        if len(request.form['login']) > 6 and len(request.form['psw']) > 6 and request.form['psw'] == request.form['psw2']:
            if db.session.query(User).filter(User.login == request.form['login']).count() == 0:
                u = User(login=request.form['login'], password=request.form['psw'])
                db.session.add(u)
                db.session.commit()
                return redirect(url_for('login'))
            else:
                 flash("Логин уже существует", "error")
        else:
             flash("Неверно заполнены поля", "error")

    return render_template("register.html")


@login_manager.user_loader
def load_user(user_id):
    return db.session.query(User).filter(User.user_id == int(user_id)).one_or_none()


@app.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))




@app.route('/event/<int:id>', methods=["POST", "GET"])
def event(id):
    event = db.session.query(Event).filter(Event.event_id == id).one_or_none()
    if event is None:
        return 'Not Found', 404

    user = event.user
    types = event.type

    if request.method == "POST":
        if request.form['delete'] == 'Удалить запись':
            for type in types:
                event.type.remove(type)


            db.session.delete(event)
            db.session.commit()

            return redirect(url_for('user_note_search', page_num=1))

    return render_template(
        "event.html",
        event=event,
        user=user,
        types=types,
        id=str(id)
    )



@app.route('/user_note_search/<int:page_num>')
@login_required
def user_note_search(page_num):
    user_notes_search = db.session.query(Event).filter(current_user.user_id == Event.user_id).\
        paginate(per_page=5, page=page_num, error_out=True)
    return render_template('user_note_search.html', notes=user_notes_search)



@app.route('/create_event', methods=['GET', 'POST'])
@login_required
def create_event():
    types = db.session.query(Type).all()

    if request.method == "POST":
        user_id = current_user.user_id
        title = request.form['title']
        date = datetime.now()
        comment = request.form['text']

        event = Event(user_id=user_id, titlt=title, open=open, date=date, comment=comment)
        db.session.add(event)

        selected_types = request.form.getlist('types')
        for type_id in selected_types:
            type = db.session.query(Type).filter(Type.type_id == type_id).one_or_none()
            event.type.append(type)


        db.session.commit()
        flash("Успешно создана", "success")
        return redirect(url_for('event', id=event.note_id))

    return render_template("create_note.html", types=types,)


@app.route('/edit_event/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_event(id):
    note = db.session.query(Event).filter(Event.note_id == id).one_or_none()
    if note is None:
        return 'Not Found', 404

    cur_types = note.type


    types = db.session.query(Type).all()


    add_types = [type for type in types if type not in cur_types]


    if request.method == "POST":
        event.user_id = current_user.user_id
        event.title = request.form['title']
        event.date = datetime.now()
        event.comment = request.form['text']

        del_types = request.form.getlist('del_types')
        for type_id in del_types:
            type = db.session.query(Type).filter(Type.type_id == type_id).one_or_none()
            note.type.remove(type)


        add_types = request.form.getlist('add_types')
        for type_id in add_types:
            type = db.session.query(Type).filter(Type.type_id == type_id).one_or_none()
            note.type.append(type)

        db.session.commit()
        flash("Успешно отредактирована", "success")
        return redirect(url_for('note', id=id))

    return render_template(
        "edit_note.html",
        event=event,
        del_types=cur_types,
        add_types=add_types,
        id=id
    )


@app.route('/event_search/<int:page_num>')
def event_search(page_num, sort_key='name'):

    events_search = db.session.query(Event).all()

    return render_template('event_search.html', events=events_search)










# @app.route('/')
# def index():
#     categories = db.session.query(Category).\
#         order_by(Category.category_id).\
#         all()
#     return render_template(
#         'mypage.html',
#         title='Моя первая страница на Flask',
#         categories=categories
#     )
#
#
# @app.route('/category/<int:id>')
# def category(id):
#     cat = db.session.query(Category).filter(Category.category_id == id).one_or_none()
#     if cat is None:
#         return 'Not Found', 404
#
#     n = db.session.query(News).\
#         filter(News.category_id == cat.category_id).\
#         order_by(desc(News.news_id)).\
#         all()
#
#     return render_template(
#         "category.html",
#         category=cat,
#         news=n
#     )
#
#
# @app.route('/edit_news/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_news(id):
#     # new
#     if id == 0:
#         n = News()
#     else:
#         n = db.session.query(News).filter(News.news_id == id).one_or_none()
#         if n is None:
#             return 'Not Found', 404
#
#     form = NewsForm(request.form)
#
#     if form.button_save.data:
#         if form.validate():
#             n.category = form.category.data
#             n.news_title = form.news_title.data
#             n.news_text = form.news_text.data
#             db.session.add(n)
#             db.session.commit()
#             if id == 0:
#                 db.session.flush()
#                 return redirect(url_for('edit_news', id=n.news_id))
#
#     elif form.button_delete.data:
#         db.session.delete(n)
#         db.session.commit()
#         return redirect(url_for('category', id=n.category_id))
#     else:
#         form.category.data = n.category
#         form.news_title.data = n.news_title
#         form.news_text.data = n.news_text
#         if form.button_add_keyword.data and form.keyword.data:
#             kw = NewsKeyword(news_id=n.news_id, keyword=form.keyword.data)
#             n.keywords.append(kw)
#             db.session.add(kw)
#             db.session.commit()
#
#     return render_template(
#         'edit_news.html',
#         news=n,
#         form=form
#     )
#
#
# @app.route('/remove_news_keyword/<int:news_id>/<keyword>', methods=['GET', 'POST'])
# @login_required
# def remove_news_keyword(news_id, keyword):
#     kw = db.session.query(NewsKeyword).\
#         filter(NewsKeyword.news_id == news_id).\
#         filter(NewsKeyword.keyword == keyword).\
#         one_or_none()
#     if kw is not None:
#         db.session.delete(kw)
#         db.session.commit()
#     return redirect(url_for('edit_news', id=news_id))
#
#
# @app.route('/edit_category/<int:id>', methods=['GET', 'POST'])
# @login_required
# def edit_category(id):
#     if id == 0:
#         cat = Category(category_name="")
#     else:
#         cat = db.session.query(Category).filter(Category.category_id == id).\
#             one_or_none()
#     if cat is None:
#         return 'Not Found', 404
#
#     form = CategoryForm(request.form)
#
#     if form.button_save.data:
#         if form.validate():
#             cat.category_name = form.category_name.data
#             db.session.add(cat)
#             db.session.commit()
#             flash("Данные успешно изменены")
#     else:
#         form.category_name.data = cat.category_name
#
#     return render_template(
#         'edit_category.html',
#         category=cat,
#         form=form
#     )



@app.route('/')
def menu():
    return render_template("menu.html")


@app.route('/mypage')
def mypage():
    return render_template("mypage.html")



if __name__ == '__main__':
    # Create scheme if not exists
    with app.app_context():
        db.create_all()
        if db.session.query(models.User).count() == 0:
            u = models.User(user_login='admin', user_password='admin')
            db.session.add(u)
            db.session.commit()

    app.run(debug=True)
