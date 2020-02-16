from flask import render_template, request, Blueprint
from web_app.models import User, Quiz, Result, Category

main = Blueprint('main', __name__)


@main.route("/")
@main.route("/home")
def home():
    categories = Category.query.all()
    results = Result.query.all()
    return render_template('home.html', categories=categories, results=results)


@main.route("/category")
def category():
    categories = Category.query.all()
    return render_template('all_category.html', title='Categories', categories=categories)
