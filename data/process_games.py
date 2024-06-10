"""
Reads through the chess PGN file and extracts all the locations where the eval is mate in x moves.
"""

import json
import re
import sqlite3
import sys
from io import StringIO

import chess
import chess.pgn
from tqdm import tqdm
import pandas as pd

mate_positions = set()
games_scanned = 0

mate_pattern = re.compile(r"#(\d+)")

con = sqlite3.connect("test_db.sqlite3")
cur = con.cursor()

cur.execute(
    """
    CREATE TABLE IF NOT EXISTS positions (
        fen TEXT,
        moves INT
    )
"""
)

cur.execute("DELETE FROM positions")

positions_to_insert = []

for line in sys.stdin:
    game = chess.pgn.read_game(StringIO(line))

    games_scanned += 1

    temp = game.board()

    for node in game.mainline():
        temp.push(node.move)
        if (
            "#" in node.comment
            and "#-" not in node.comment
            and temp.turn == chess.WHITE
        ):
            mate_in_x = int(mate_pattern.search(node.comment).group(1))
            fen = temp.fen()
            if mate_in_x <= 10 and fen not in mate_positions:
                positions_to_insert.append((fen, mate_in_x))
                mate_positions.add(fen)

    if len(positions_to_insert) >= 10000:
        cur.executemany(
            f"INSERT INTO positions (fen, moves) VALUES ({', '.join('?' for _ in positions_to_insert[0])})",
            positions_to_insert,
        )
        con.commit()
        positions_to_insert = []

    print(f"Games: {games_scanned} \t Mate Positions: {len(mate_positions)}", end="\r")

print(f"Games: {games_scanned} \t Mate Positions: {len(mate_positions)}")

# get 10k random positions up to 10 moves to calculate mate, and put those in their own table
cur.execute("DROP TABLE IF EXISTS data")

for moves in range(1, 11):
    sql = f"""
        SELECT fen, moves
        FROM positions
        WHERE moves = {moves}
        ORDER BY RANDOM()
        LIMIT 10000
    """

    temp_df = pd.read_sql_query(sql, con)
    temp_df.to_sql(con=con, name="data", index=False, if_exists="append")

cur.execute("DROP TABLE IF EXISTS positions")

con.close()
