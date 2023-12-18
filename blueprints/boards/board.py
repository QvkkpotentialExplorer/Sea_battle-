from flask import Blueprint, render_template, redirect, abort
from data.boards import Board
from data.db_session import db_sess
from flask_login import login_required, current_user
from forms.add_board_form import AddBoardForm

board = Blueprint('board', __name__, template_folder='templates', static_folder='static', url_prefix='/board')


@board.route('/list')
def board_list():
    boards = db_sess.query(Board).all()
    return render_template('board_list.html', boards=boards)


@board.route('/add', methods=['GET', 'POST'])
@login_required
def add_board():
    if not current_user.is_admin:
        return abort(401)
    form = AddBoardForm()
    if form.validate_on_submit():
        board = Board(
            admin_id=current_user.id,
            n=form.n.data,
            default_shoots=form.default_shoots.data
        )
        db_sess.add(board)
        db_sess.commit()
        return 'Доска создана'
    return render_template('add_board.html', form=form)