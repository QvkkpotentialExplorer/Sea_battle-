from flask import Blueprint, render_template, url_for
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from data.db_session import db_sess
from data.prize_data import PrizeData
from data.prizes import Prize
from data.users import User

profile = Blueprint('profile', __name__, template_folder='../templates', static_folder='static', url_prefix='/profile')


@profile.route('/profile_page')
@login_required
def user():
    user = db_sess.query(User).filter(User.login == current_user.login).first()
    prizes = [db_sess.query(PrizeData).filter(PrizeData.owner_id == current_user.id).all()]

    if current_user.is_admin:
        return render_template('admin.html')
    else:
        return render_template('user.html', user=user, prizes=prizes)

@profile.route('/prizes', methods=['GET', 'POST'])
@login_required
def prize():
    if current_user.is_admin:
        prizes = db_sess.query(Prize.name,Prize.description,Prize.avatar).all()
        print(prizes)
        return render_template('prizes.html',prizes = prizes)

    else:
        prizes = db_sess.query(Prize.name,Prize.description,Prize.avatar).filter(PrizeData.owner_id == current_user.id).all()
        return render_template('prizes.html', prizes=prizes)