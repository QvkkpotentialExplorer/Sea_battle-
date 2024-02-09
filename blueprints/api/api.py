from datetime import datetime
from flask import Blueprint, jsonify, request, redirect, url_for, flash
from flask_login import current_user, login_required
from data.boards import Board
from data.ships import Ship
from data.users_on_boards import UserOnBoard
from data.prize_data import PrizeData
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
    print(x, y)
    print(board_id)
    user = db_sess.query(UserOnBoard).filter(UserOnBoard.user_id == current_user.id,
                                             UserOnBoard.board_id == request.args.get('board_id', default=0,
                                                                                    type=int)).first()
    print(user.count)
    cells = db_sess.query(DeathCell).filter(DeathCell.board_id == board_id, DeathCell.x == x, DeathCell.y == y).first()

    if int(user.count) > 0:
        ship = db_sess.query(Ship).filter(Ship.board_id == board_id, Ship.x == x, Ship.y == y).first()
        user.count -= 1
        if cells is not None:
            return redirect(url_for('board.edit_board', board_id=board_id,errors = "На эту координату уже стреляли"))
        cell = DeathCell(
            board_id=board_id,
            x=x,
            y=y,
        )
        if ship is None:
            cell.status_ship = False
            db_sess.add(cell)
            db_sess.commit()
            return redirect(url_for('board.edit_board',board_id = board_id))
        cell.status_ship = True
        prize_data = db_sess.get(PrizeData,ship.prize_id)
        prize_data.is_win = True
        prize_data.owner_id = current_user.id
        prize_data.date_win = datetime.now()
        db_sess.add(cell)
        db_sess.delete(ship)
        db_sess.commit()
        flash('Вы попали')
        return redirect(url_for('board.edit_board', board_id=board_id, msg = "Вы попали"))
    else :
        return redirect(url_for('board.edit_board',board_id = board_id,errors ="У тебя недостаточно выстрелов"))