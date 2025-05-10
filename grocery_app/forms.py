from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, SelectField, SubmitField, PasswordField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.validators import DataRequired, Length, URL, Optional, ValidationError
from grocery_app.models import GroceryStore, GroceryItem, User
from grocery_app import bcrypt

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

class SignUpForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('That username is taken. Please choose a different one.')

class LoginForm(FlaskForm):
    username = StringField('User Name',
        validators=[DataRequired(), Length(min=3, max=50)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Log In')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if not user:
            raise ValidationError('No user with that username. Please try again.')

    def validate_password(self, password):
        user = User.query.filter_by(username=self.username.data).first()
        if user and not bcrypt.check_password_hash(
                user.password, password.data):
            raise ValidationError('Password doesn\'t match. Please try again.')