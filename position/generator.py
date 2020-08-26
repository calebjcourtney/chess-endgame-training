import os
import time

import chess
import chess.svg


def create_position_file(fen: str):
    path = "tmp/"
    now = time.time()

    # if the file is older than 6 hours, then remove the file
    for f in os.listdir(path):
        if f.endswith(".svg") and os.stat(os.path.join(path, f)).st_mtime < now - 6 * 3600.0:
            os.remove(os.path.join(path, f))

    board = chess.Board(fen)
    out_string = chess.svg.board(board)
    out_fen = fen.replace("/", "_")
    with open(f"tmp/{out_fen}.svg", "w+") as out:
        out.write(out_string)

    return f"tmp/{out_fen}.svg"
