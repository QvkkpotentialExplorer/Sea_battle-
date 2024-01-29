from flask import Blueprint, render_template, redirect, abort, url_for
from data.boards import Board
from data.db_session import db_sess
from flask_login import login_required, current_user
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
        return render_template('board_list.html', boards=boards)
    else:
        boards = db_sess.query(Board).filter(UserOnBoard.user_id== current_user.id).all()
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
        return redirect (f'game_room/{board.id}')
    return render_template('add_board.html', form=form)


@board.route('/game_room/<int:board_id>', methods=['GET', 'POST'])
@login_required
def edit_board(board_id: int):
    if not current_user.is_admin:
        return abort(401)
    add_ship_form = AddShipForm(board_id=board_id)
    delete_ship_form = DeleteShipForm(board_id=board_id)
    board = db_sess.get(Board, board_id)
    user_on_board = db_sess.query(UserOnBoard).filter(UserOnBoard.board_id == board_id).all()
    ship_coords = [(ship.x, ship.y) for ship in db_sess.query(Ship).filter(Ship.board_id == board_id).all()]
    users = db_sess.query(User).all()

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


        print(add_ship_form.y.data)
        board_render[add_ship_form.y.data][add_ship_form.x.data] = '#'
        print(board_render)

        return render_template('game_room.html',
                               add_ship_form=add_ship_form,
                               delete_ship_form=delete_ship_form,
                               board=db_sess.get(Board, board_id),
                               users = users,
                               user_on_board = user_on_board,
                               prizes = prizes,
                               board_render=[''.join(i) for i in board_render],
                               size = board.n)

    return render_template('game_room.html',
                           add_ship_form=add_ship_form,
                           delete_ship_form =delete_ship_form,
                           prizes = prizes,
                           users = users,
                           user_on_board=user_on_board,
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
    shoots = db_sess.query(UserOnBoard).filter(UserOnBoard.board_id == board_id,UserOnBoard.user_id == current_user.id).first()
    if shoots is None:
        shoots_data = UserOnBoard(
            user_id=current_user.id,
            board_id = board_id,
            count=board.default_shoots
        )
        db_sess.add(shoots_data)
    user_on_board = db_sess.query(UserOnBoard).filter(UserOnBoard.user_id == current_user.id,  UserOnBoard.board_id == board_id).first()
    db_sess.commit()
    if not user_on_board.can_join:
        return 'Вы забанены на этой доске!'
    return render_template('show_board.html')

@board.route('/add_user/<int:board_id>/<int:user_id>',methods=['GET', 'POST'])
@login_required
def add_user(board_id: int,user_id: int ):
    # if not current_user.is_admin:
    #     return abort(401)
    print(db_sess.query(Ship).filter(board_id == Ship.board_id).all())

    if db_sess.query(Ship).filter(board_id == Ship.board_id).all():
        count = db_sess.query(Board.default_shoots).filter(Board.id == board_id).first()
        print(count)
        user_on_board = UserOnBoard(user_id=user_id,
                                    board_id = board_id,
                                    can_join = True,
                                    count=count[0])

        db_sess.add(user_on_board)
        db_sess.commit()
        return redirect(url_for('board.edit_board', board_id =board_id))
    else:
        return False

@board.route('/delete_user/<int:board_id>/<int:user_id>')
@login_required
def delete_user(board_id: int,user_id: int):
    if not current_user.is_admin:
        return abort(401)
    user = db_sess.query(UserOnBoard).filter(UserOnBoard.user_id == user_id,UserOnBoard.board_id ==  board_id).first()
    db_sess.delete(user)
    db_sess.commit()

@board.route('/delete_board/<int:board_id>',methods=['GET', 'POST'])
@login_required
def delete_board(board_id:int):
    if not current_user.is_admin:
        return abort(401)
    print(board_id)
    board = db_sess.get(Board, board_id)
    print(board)
    users = db_sess.query(UserOnBoard).filter(UserOnBoard.board_id == board_id).all()
    ships = db_sess.query(Ship).filter(Ship.board_id == board_id).all()

    print(ships)
    if ships: #Проверяем , были ли на поле корабли
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

