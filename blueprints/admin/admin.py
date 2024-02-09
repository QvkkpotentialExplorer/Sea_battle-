import click
from flask import Blueprint, render_template, redirect, url_for, abort, request
from data.db_session import db_sess
from data import db_session
from data.users import User
from data.prizes import Prize
from data.users_on_boards import UserOnBoard

from forms.add_prize import AddPrizeForm
from uuid import uuid1
from flask_login import current_user, login_required

admin = Blueprint('admin', __name__, url_prefix='/admin/', template_folder='../templates')


@admin.cli.command("addadmin")
@click.argument("name")
@click.argument("password")
def create_admin(name, password):
    if db_sess is None:
        db_session.global_init('db/sea_battel.db')
    user = User(
        login=name,
        is_admin=True
    )
    user.set_password(password)
    db_sess.add(user)
    db_sess.commit()
    db_sess.close()
    return 'Вы зареганы'


@admin.route('/add_prize', methods=['GET', 'POST'])
@login_required
def add_prize():
    if not current_user.is_admin:
        return abort(401)
    form = AddPrizeForm()
    if form.validate_on_submit():
        file_name = f'{str(uuid1())}.{form.avatar.data.filename.split(".")[-1]}'
        prize = Prize(
            avatar=f'{file_name}',
            name=form.name.data,
            description=form.description.data,
        )
        db_sess.add(prize)
        db_sess.commit()
        form.avatar.data.save(f'blueprints/profiles/static/avatars/{file_name}')
        return redirect(url_for('profile.user'))

    return render_template('add_prize.html', form=form)


@admin.route('/add_shots')
@login_required
def add_shoot():
    if not current_user.is_admin:
        return abort(401)
    board_id = request.args.get('board_id')
    shoots = db_sess.query(UserOnBoard).filter(UserOnBoard.user_id == request.args.get('user_id'),
                                             UserOnBoard.board_id == board_id).first()
    print(shoots)
    shoots.count += request.args.get('shoots_count')
    db_sess.commit()

    return redirect(url_for("board.edit_board", board_id = board_id))
