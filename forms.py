from wtforms import Form, StringField, SubmitField, TextAreaField, SelectField
from wtforms import validators
from wtforms_alchemy import QuerySelectField

#from models import Category


# class CategoryForm(Form):
#     category_name = StringField("Название категории", validators=[
#         validators.DataRequired(message="Поле обязательно для заполнения"),
#         validators.Length(min=3, max=50, message="Длина должна быть от 3 до 50 символов")])
#
#     button_save = SubmitField("Сохранить")
#
#
# class NewsForm(Form):
#     news_title = StringField("Заголовок новости", validators=[
#         validators.DataRequired(message="Заголовок не может быть пустым"),
#         validators.Length(min=3, max=100, message="Длина заголовка должна быть от 3 до 100 символов")])
#     news_text = TextAreaField("Текст новости", validators=[validators.DataRequired()])
#     category = QuerySelectField("Категория",
#                                 validators=[validators.DataRequired()],
#                                 query_factory=lambda: Category.query.order_by(Category.category_id).all(),
#                                 get_pk=lambda c: c.category_id,
#                                 get_label=lambda c: c.category_name)
#
#     button_save = SubmitField("Сохранить")
#     button_delete = SubmitField("Удалить")
#     keyword = StringField("Заголовок новости", validators=[validators.Optional()])
#     button_add_keyword = SubmitField("Добавить ключевое слово")
