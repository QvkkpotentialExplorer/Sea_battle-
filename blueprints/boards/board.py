from flask import Blueprint, render_template, redirect, abort, url_for, flash
from data.boards import Board
from data.db_session import db_sess
from flask_login import login_required, current_user

from data.no_cells import DeathCell
from data.users import User
from data.prizes import Prize
from data.users_on_boards import UserOnBoard
from data.prize_data import PrizeData
from forms.add_board_form import AddBoardForm
from forms.add_ship_form import AddShipForm
from data.ships import Ship
from forms.delete_ship_form import DeleteShipForm

board = Blueprint('board', __name__, template_folder='../templates', static_folder='static', url_prefix='/board')


@board.route('/list')
def board_list():
    if current_user.is_admin:
        boards = db_sess.query(Board).all()
        return render_template('board_list.html', boards=boards, current_user=current_user)
    else:
        boards_id = db_sess.query(UserOnBoard.board_id).filter(UserOnBoard.user_id == current_user.id).all()
        print(boards_id)
        boards = []
        for board_id in boards_id:
            boards.append(db_sess.get(Board, board_id))
        return render_template('board_list.html', boards=boards, current_user=current_user)


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
        print(board)
        db_sess.add(board)
        db_sess.commit()
        return redirect(f'game_room/{board.id}')
    return render_template('add_board.html', form=form)


@board.route('/game_room/<int:board_id>', methods=['GET', 'POST'])
@login_required
def edit_board(board_id: int, errors=None):
    ship_coords = [(ship.x, ship.y) for ship in db_sess.query(Ship).filter(Ship.board_id == board_id).all()]
    shoots_coords = [(shoots.x, shoots.y) for shoots in
                     db_sess.query(DeathCell).filter(DeathCell.board_id == board_id).all()]
    board = db_sess.get(Board, board_id)
    board_render = [['.'] * board.n for _ in range(board.n)]

    for x, y in ship_coords:
        board_render[y][x] = '#'
    for x, y in shoots_coords:
        board_render[y][x] = 'x'

    if not current_user.is_admin:
        user = db_sess.query(UserOnBoard).filter(UserOnBoard.user_id == current_user.id,
                                                 UserOnBoard.board_id == board_id).first()
        return render_template('user_game_room.html', board_render=board_render,
                               user=user,
                               current_user=current_user,
                               size=len(board_render),
                               errors=errors)

    else:
        add_ship_form = AddShipForm(board_id=board_id)
        delete_ship_form = DeleteShipForm(board_id=board_id)

        board = db_sess.get(Board, board_id)
        user_on_board = db_sess.query(UserOnBoard).filter(UserOnBoard.board_id == board_id).all()

        users = db_sess.query(User).all()

        for x, y in ship_coords:
            board_render[y][x] = '#'
        prizes = db_sess.query(Prize.name, Prize.description, Prize.avatar).all()
        print(prizes)

        if add_ship_form.validate_on_submit():
            prize_data = PrizeData(
                is_win=False,
                owner_id=current_user.id,
                prize_id=add_ship_form.prize.data
            )
            db_sess.add(prize_data)
            db_sess.commit()

            ship = Ship(
                board_id=board_id,
                prize_id=prize_data.id,
                x=add_ship_form.x.data,
                y=add_ship_form.y.data
            )
            db_sess.add(ship)
            db_sess.commit()

            print(prize_data.id)
            board_render[add_ship_form.y.data][add_ship_form.x.data] = '#'
            print(board_render)
            add_ship_form = AddShipForm(board_id=board_id)

            return render_template('admin_game_room.html',
                                   add_ship_form=add_ship_form,
                                   delete_ship_form=delete_ship_form,
                                   board=db_sess.get(Board, board_id),
                                   users=users,
                                   errors=errors,
                                   user_on_board=user_on_board,
                                   prizes=prizes,
                                   board_render=[''.join(i) for i in board_render],
                                   size=board.n)

        # if delete_ship_form.validate_on_submit():
        #     ship = db_sess.query(Ship).filter(Ship.board_id == board_id, Ship.x == delete_ship_form.x.data,
        #                                       Ship.y == delete_ship_form.y.data).first()# Ищем корабли по данным переданной в форму.
        #     prize_data = db_sess.query(PrizeData).filter(PrizeData.id == ship.prize_data.id).first()#Находим приз , привязанный к нему
        #     print(prize_data)
        #     db_sess.delete(ship)
        #     db_sess.delete(prize_data)
        #     db_sess.commit()
        #
        #     board_render[delete_ship_form.y.data][delete_ship_form.x.data] = '.'
        #
        #     return render_template('admin_game_room.html',
        #                            add_ship_form=add_ship_form,
        #                            delete_ship_form=delete_ship_form,
        #                            board=db_sess.get(Board, board_id),
        #                            users=users,
        #                            errors=errors,
        #                            user_on_board=user_on_board,
        #                            prizes=prizes,
        #                            board_render=[''.join(i) for i in board_render],
        #                            size=board.n)

        return render_template('admin_game_room.html',
                               add_ship_form=add_ship_form,
                               delete_ship_form=delete_ship_form,
                               prizes=prizes,
                               users=users,
                               errors=errors,
                               user_on_board=user_on_board,
                               board=db_sess.get(Board, board_id),
                               board_render=[''.join(i) for i in board_render],
                               size=board.n)


@board.route('/show/<int:board_id>', methods=['GET', 'POST'])
@login_required
def show_board(board_id):
    if (current_user.is_admin):
        return render_template('show_admin_board.html')
    board = db_sess.query(Board).filter(Board.id == board_id).first()

    if board is None:
        return abort(404)
    shoots = db_sess.query(UserOnBoard).filter(UserOnBoard.board_id == board_id,
                                               UserOnBoard.user_id == current_user.id).first()
    if shoots is None:
        shoots_data = UserOnBoard(
            user_id=current_user.id,
            board_id=board_id,
            count=board.default_shoots
        )
        db_sess.add(shoots_data)
    user_on_board = db_sess.query(UserOnBoard).filter(UserOnBoard.user_id == current_user.id,
                                                      UserOnBoard.board_id == board_id).first()
    db_sess.commit()
    if not user_on_board.can_join:
        return 'Вы забанены на этой доске!'
    return render_template('show_board.html')


@board.route('/add_user/<int:board_id>/<int:user_id>', methods=['GET', 'POST'])
@login_required
def add_user(board_id: int, user_id: int):
    # if not current_user.is_admin:
    #     return abort(401)
    print(db_sess.query(Ship).filter(board_id == Ship.board_id).all())
    if not db_sess.query(UserOnBoard).filter(UserOnBoard.user_id == user_id, UserOnBoard.board_id == board_id).first():
        errors = "Еще "
        if db_sess.query(Ship).filter(board_id == Ship.board_id).all():

            count = db_sess.query(Board.default_shoots).filter(Board.id == board_id).first()
            print(count)
            user_on_board = UserOnBoard(user_id=user_id,
                                        board_id=board_id,
                                        can_join=True,
                                        count=count[0])
            print(user_on_board)
            db_sess.add(user_on_board)
            db_sess.commit()
            return redirect(url_for('board.edit_board', board_id=board_id))
        else:
            return redirect(url_for('board.edit_board', board_id=board_id, errors=errors))

    else:
        errors = "Пользователь уже добавлен на поле"
        return redirect(url_for('board.edit_board', board_id=board_id, errors=errors))


@board.route('/delete_user/<int:board_id>/<int:user_id>')
@login_required
def delete_user(board_id: int, user_id: int):
    if not current_user.is_admin:
        return abort(401)
    user = db_sess.query(UserOnBoard).filter(UserOnBoard.user_id == user_id, UserOnBoard.board_id == board_id).first()

    db_sess.delete(user)
    db_sess.commit()


@board.route('/delete_board/<int:board_id>', methods=['GET', 'POST'])
@login_required
def delete_board(board_id: int):
    if not current_user.is_admin:
        return abort(401)
    print(board_id)
    board = db_sess.get(Board, board_id)
    print(board)
    users = db_sess.query(UserOnBoard).filter(UserOnBoard.board_id == board_id).all()
    ships = db_sess.query(Ship).filter(Ship.board_id == board_id).all()

    print(ships)
    if ships:  # Проверяем , были ли на поле корабли
        for ship in ships:
            print(ship)
            db_sess.delete(ship)
            db_sess.commit()
    if not users:

        db_sess.delete(board)
        db_sess.commit()
    else:
        for user in users:
            db_sess.delete(user)
        db_sess.delete(board)
        db_sess.commit()
    return redirect(url_for('board.board_list'))


@board.route('/delete_ship/<int:board_id>/<int:x>/<int:y>', methods=['GET', 'POST'])
@login_required
def delete_ship(board_id : int ,x :int,y: int):
    if not current_user.is_admin:
        return abort(401)
    ship = db_sess.query(Ship).filter(Ship.board_id == board_id, Ship.x == x, Ship.y == y).first()
    if not ship :
        errors = "На этих координатах нет корабля "
        return redirect(url_for('board.edit_board', board_id=board_id, errors=errors))
    prize_data = db_sess.query(PrizeData).filter(PrizeData.id == ship.prize_id).first()
    db_sess.delete(ship)
    db_sess.delete(prize_data)
    db_sess.commit()
    return redirect(url_for('board.edit_board',board_id = board_id))



