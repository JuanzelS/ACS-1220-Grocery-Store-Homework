from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, Optional

from grocery_app.models import GroceryStore, GroceryItem

# TODO: Create a form class for new grocery stores
class GroceryStoreForm(FlaskForm):
    title = StringField('Store Title', validators=[DataRequired(), Length(min=3, max=80)])
    address = StringField('Store Address', validators=[DataRequired(), Length(min=3, max=200)])
    submit = SubmitField('Submit')

# TODO: Create a form class for new grocery items
class GroceryItemForm(FlaskForm):
    name = StringField('Item Name', validators=[DataRequired(), Length(min=3, max=80)])
    price = FloatField('Price', validators=[DataRequired()])
    category = SelectField('Category', choices=[
        ('PRODUCE', 'Produce'),
        ('DAIRY', 'Dairy'),
        ('MEAT', 'Meat'),
        ('BAKERY', 'Bakery'),
        ('PANTRY', 'Pantry'),
        ('FROZEN', 'Frozen')
    ])
    photo_url = StringField('Photo URL', validators=[URL(), Optional()])
    store = QuerySelectField('Store', query_factory=lambda: GroceryStore.query, get_label='title')
    submit = SubmitField('Submit')