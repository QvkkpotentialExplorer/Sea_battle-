from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from data.boards import Board
from data.ships import Ship
from data.users_on_boards import UserOnBoard
from data.users_shoots import UserShoot
from data.db_session import db_sess
from data.no_cells import DeathCell

api = Blueprint('api', __name__, url_prefix='/api')


@api.route('/get_board/<int:board_id>')
def get_board(board_id):
    board = db_sess.query(Board).get(board_id)
    return jsonify({
        'board_id': board.id,
        'board_n': board.n
    })


# @api.route('/get_user_shoot')
# @login_required
# def get_user_shoot():
#     shoots = db_sess.query(UserShoot).filter(UserShoot.user_id == current_user.id,
#                                              UserShoot.board_id == request.args.get('board_id', default=0,
#                                                                                     type=int)).first()
#     return str(shoots.count) if shoots is not None else '-1'


@api.route('/shoot_user')
@login_required
def shoot():
    board_id = request.args.get('board_id', default=0, type=int)
    x = request.args.get('x', default=0, type=int)
    y = request.args.get('y', default=0, type=int)

    shoots = db_sess.query(UserOnBoard).filter(UserOnBoard.user_id == current_user.id,
                                             UserOnBoard.board_id == request.args.get('board_id', default=0,
                                                                                    type=int)).first()
    cells = db_sess.query(DeathCell).filter(DeathCell.board_id == board_id, DeathCell.x == x, DeathCell.y == y).first()
    if shoots is not None and cells is not None:
        return 'False'
    if UserOnBoard.count > 0:
        ship = db_sess.query(Ship).filter(Ship.board_id == board_id, Ship.x == x, Ship.y == y).first()
        UserOnBoard.count -= 1
        cell = DeathCell(
            board_id=board_id,
            x=x,
            y=y
        )
        if ship is None:
            db_sess.add(cell)
            return 'MIMO'
        ship.prize_data.is_win = True
        ship.prize_data.owner_id = current_user.id
        db_sess.add(cell)
        db_sess.delete(ship)
        db_sess.commit()
        return str(ship is not None)
    return 'no_shoots'