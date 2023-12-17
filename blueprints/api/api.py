from flask import Blueprint, jsonify, request
from data.boards import Board
from data.ships import Ship
from data.users_shoots import UserShoot
from data import db_session

api = Blueprint('api', __name__, url_prefix='/api/')


@api.route('/get_board/<int:board_id>')
def get_board(board_id):
    db_sess = db_session.create_session()
    board = db_sess.query(Board).get(board_id)
    db_sess.close()
    return jsonify({
        'board_id': board.id,
        'board_n': board.n
    })


@api.route('/get_ships_on_board/<int:board_id>')
def get_ships_on_board(board_id):
    db_sess = db_session.create_session()
    ships = db_sess.query(Ship).filter(Ship.board_id == board_id).all()
    db_sess.close()
    return jsonify({
        [
            {
                'ship_x': ship.x,
                'ship_y': ship.y
            }
            for ship in ships
        ]
    })


@api.route('/get_user_shoot/')
def get_user_shoot():
    db_sess = db_session.create_session()
    shoots = db_sess.query(UserShoot).filter(UserShoot.user_id == request.args.get('user_id', default=0, type=int),
                                             UserShoot.board_id == request.args.get('board_id', default=0,
                                                                                    type=int)).first()
    db_sess.close()
    return str(shoots.count) if shoots is not None else '-1'
