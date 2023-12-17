from flask import Blueprint, render_template, redirect, abort
from data.boards import Board
from data import db_session
from flask_login import login_required, current_user
from forms.add_board_form import AddBoardForm

board = Blueprint('board', __name__, template_folder='templates', static_folder='static', url_prefix='/board')


@board.route('/list')
def board_list():
    db_sess = db_session.create_session()
    boards = db_sess.query(Board).all()
    db_sess.close()
    return render_template('board_list.html', boards=boards)


@board.route('/add', methods=['GET', 'POST'])
@login_required
def add_board():
    if not current_user.is_admin:
        return abort(401)
    form = AddBoardForm()
    if form.validate_on_submit():
        db_sess = db_session.create_session()
        board = Board(
            admin_id=current_user.id,
            n=form.n.data,
            default_shoots=form.default_shoots.data
        )
        db_sess.add(board)
        db_sess.commit()
        db_sess.close()
        return 'Доска создана'
    return render_template('add_board.html', form=form)