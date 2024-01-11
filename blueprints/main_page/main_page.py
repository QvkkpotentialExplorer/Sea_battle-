from flask import Blueprint, render_template

main_page = Blueprint('main_page', __name__, template_folder='../templates')


@main_page.route('/')
def index():
    return render_template('index.html')