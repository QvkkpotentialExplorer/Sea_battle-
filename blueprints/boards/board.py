from flask import Blueprint, render_template, redirect, abort
from data.boards import Board
from data.db_session import db_sess
from flask_login import login_required, current_user

from data.prizes import Prize
from data.users_on_boards import UserOnBoard
from data.prize_data import PrizeData
from forms.add_board_form import AddBoardForm
from forms.add_ship_form import AddShipForm
from data.ships import Ship
from data.users_shoots import UserShoot

board = Blueprint('board', __name__, template_folder='../templates', static_folder='static', url_prefix='/board')


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
        return redirect (f'edit/{board.id}')
    return render_template('add_board.html', form=form)


@board.route('/edit/<int:board_id>', methods=['GET', 'POST'])
@login_required
def edit_board(board_id: int):
    if not current_user.is_admin:
        return abort(401)
    add_ship_form = AddShipForm(board_id=board_id)
    board = db_sess.get(Board, board_id)
    ship_coords = [(ship.x, ship.y) for ship in db_sess.query(Ship).filter(Ship.board_id == board_id).all()]
    print(ship_coords)
    board_render = [['.'] * board.n for _ in range(board.n)]
    for x, y in ship_coords:
        board_render[y][x] = '#'
    prizes = db_sess.query(Prize.name, Prize.description, Prize.avatar).all()
    if add_ship_form.validate_on_submit():
        prize_data = PrizeData(
            is_win=False,
            owner_id=current_user.id,
            prize_id=add_ship_form.prize.data
        )
        ship = Ship(
            board_id=board_id,
            prize_id=add_ship_form.prize.data,
            x=add_ship_form.x.data,
            y=add_ship_form.y.data
        )
        db_sess.add(prize_data)
        db_sess.add(ship)
        db_sess.commit()
        board_render[add_ship_form.y.data][add_ship_form.x.data] = '#'

        return render_template('edit_board.html',
                               ship_form=add_ship_form,
                               board=db_sess.get(Board, board_id),
                               prizes = prizes,
                               board_render=[''.join(i) for i in board_render],
                               size = board.n)

    return render_template('edit_board.html',
                           ship_form=add_ship_form,
                           prizes = prizes,
                           board=db_sess.get(Board, board_id),
                           board_render=[''.join(i) for i in board_render],
                           size = board.n)


@board.route('/show/<int:board_id>', methods=['GET', 'POST'])
@login_required
def show_board(board_id):
    if (current_user.is_admin):
        return render_template('show_admin_board.html')
    board = db_sess.query(Board).filter(Board.id == board_id).first()
    if board is None:
        return abort(404)
    shoots = db_sess.query(UserShoot).filter(UserShoot.board_id == board_id,
                                             UserShoot.user_id == current_user.id).first()
    if shoots is None:
        shoots_data = UserShoot(
            user_id=current_user.id,
            board_id=board_id,
            count=board.default_shoots
        )
        db_sess.add(shoots_data)
    user_on_board = db_sess.query(UserOnBoard).filter(UserOnBoard.user_id == current_user.id,
                                                      UserOnBoard.board_id == board_id)
    if user_on_board is None:
        user_on_board = UserOnBoard(
            user_id=current_user.id,
            board_id=board_id
        )
        db_sess.add(user_on_board)
    db_sess.commit()
    if not user_on_board.can_join:
        return 'Вы забанены на этой доске!'
    return render_template('show_board.html')
