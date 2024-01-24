from crypto.gost import *
from datetime import datetime


def gen_url(user_id: int, board_id: int):
    url = [str(datetime.now()), str(user_id), str(board_id)]
    return b32encrypt(';'.join(url))