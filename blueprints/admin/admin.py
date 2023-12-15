import click
from flask import Blueprint
from data import db_session
from data.users import User

admin = Blueprint('admin', __name__, url_prefix='/admin/')


@admin.cli.command("create-admin")
@click.argument("name")
@click.argument("password")
def create_admin(name, password):
    db_sess = db_session.create_session()
    if db_sess is None:
        db_session.global_init('db/sea_battel.db')
        db_sess = db_session.create_session()
    user = User(
        login=name,
        is_admin=True
    )
    user.set_password(password)
    db_sess.add(user)
    db_sess.commit()
    db_sess.close()
    return 'Вы зареганы'