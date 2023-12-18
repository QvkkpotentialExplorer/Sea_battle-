from flask import Blueprint, jsonify, request
from flask_login import current_user, login_required
from data.boards import Board
from data.ships import Ship
from data.users_shoots import UserShoot
from data.db_session import db_sess
from data.prize_data import PrizeData

api = Blueprint('api', __name__, url_prefix='/api/')


@api.route('/get_board/<int:board_id>')
def get_board(board_id):
    board = db_sess.query(Board).get(board_id)
    return jsonify({
        'board_id': board.id,
        'board_n': board.n
    })


@api.route('/get_user_shoot/')
def get_user_shoot():
    shoots = db_sess.query(UserShoot).filter(UserShoot.user_id == request.args.get('user_id', default=0, type=int),
                                             UserShoot.board_id == request.args.get('board_id', default=0,
                                                                                    type=int)).first()
    return str(shoots.count) if shoots is not None else '-1'


@api.route('/shoot_user/')
@login_required
def shoot():
    shoots = db_sess.query(UserShoot).filter(UserShoot.user_id == current_user.id,
                                             UserShoot.board_id == request.args.get('board_id', default=0,
                                                                                    type=int)).first()
    if shoots.count > 0:
        board_id = request.args.get('board_id', default=0, type=int)
        x = request.args.get('x', default=0, type=int)
        y = request.args.get('y', default=0, type=int)
        ship = db_sess.query(Ship).filter(Ship.board_id == board_id, Ship.x == x, Ship.y == y).first()
        shoots.count -= 1
        ship.prize_data.is_win = True
        ship.prize_data.owner_id = current_user.id
        db_sess.delete(ship)
        db_sess.commit()
        return str(ship is not None)
    return 'no_shoots'