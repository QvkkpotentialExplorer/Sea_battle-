from flask import Blueprint, render_template, url_for, abort
from flask_login import login_required, current_user
from werkzeug.utils import redirect

from data.db_session import db_sess
from data.prize_data import PrizeData
from data.prizes import Prize
from data.boards import Board
from data.users import User
from data.users_on_boards import UserOnBoard
from datetime import datetime
from crypto.gost import *

profile = Blueprint('profile', __name__, template_folder='../templates', static_folder='static', url_prefix='/profile')


@profile.route('/profile_page')
@login_required
def user():
    user = db_sess.query(User).filter(User.login == current_user.login).first()
    prizes = [db_sess.query(PrizeData).filter(PrizeData.owner_id == current_user.id).all()]

    if current_user.is_admin:
        return render_template('admin.html')
    else:
        return render_template('user.html', user=user)


@profile.route('/prizes', methods=['GET', 'POST'])
@login_required
def prize():
    if current_user.is_admin:
        prizes = db_sess.query(Prize.name,Prize.description,Prize.avatar).all()
        print(prizes)
        return render_template('prizes.html',prizes = prizes,current_user=current_user)

    else:
        prizes = db_sess.query(PrizeData.prize_id,PrizeData.data_win).filter(PrizeData.owner_id == current_user.id).all()
        print(prizes)
        return render_template('prizes.html', prizes=prizes,template = 'base_user.html',current_user=current_user)

@profile.route('/client')
@login_required
def client():
    user =  db_sess.query(User).filter(User.login == current_user.login).first()
    return render_template('clients.html',user = user)


@profile.route('/invite/<string:invite>')
@login_required
def invites(invite):
    invite_str = b32decrypt(invite)
    uname = invite_str.split(';')

    try:
        user_id = int(uname[2])
        board_id = int(uname[1])
        creation_date = datetime.strptime(uname[0], '%Y-%m-%d %H:%M:%S.%f')
        print(user_id, board_id, creation_date)
    except Exception as i:
        print(i)
        return abort(404)

    if (user_id != current_user.id or
            (datetime.now() - creation_date).seconds > 3600 or
            db_sess.get(Board, board_id) is None):
        return abort(404)

    user_on_board = UserOnBoard(
        user_id=current_user.id,
        board_id=board_id
    )
    db_sess.add(user_on_board)
    db_sess.commit()
    return redirect(url_for('board.show_board', board_id=board_id))
