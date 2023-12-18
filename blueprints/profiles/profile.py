from flask import Blueprint, render_template
from flask_login import login_required, current_user

from data.db_session import db_sess
from data.prize_data import PrizeData
from data.users import User

profile = Blueprint('profile', __name__, template_folder='templates', static_folder='static', url_prefix='/profile')


@profile.route('/profile_page')
def user():
    user = db_sess.query(User).filter(User.login == current_user.login).first()
    prizes = [db_sess.query(PrizeData).filter(PrizeData.owner_id == current_user.id).all()]

    if current_user.is_admin:
        return render_template('admin_html')
    else:
        return render_template('user.html',user = user,prizes= prizes)
