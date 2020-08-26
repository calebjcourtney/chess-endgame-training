"""
Reads through the chess JSON to parse the moves with comments that indicate a mate can be found from the given position.
"""

import json
import sqlite3

import chess
import chess.pgn
from tqdm import tqdm
import pandas as pd

mate_positions = {}
games_scanned = 0

moves_file = open("moves.jsonl")
for line in moves_file:
    moves = json.loads(line)
    games_scanned += 1

    board = chess.Board()

    for move in moves:
        move_text = move['move'].replace("?", "").replace("!", "")
        try:
            board.push(board.parse_san(move_text))
        except ValueError:
            continue

        if move["eval"] is not None and "#" in move["eval"] and board.turn:
            mate_positions[board.fen()] = int(move["eval"].replace("#", ""))

    board = chess.Board()

    print(f"Games: {games_scanned} \t Mate Positions: {len(mate_positions)}", end = "\r")

print(f"Games: {games_scanned} \t Mate Positions: {len(mate_positions)}")


print("loading into sqlite")

con = sqlite3.connect("db.sqlite3")
cur = con.cursor()

cur.execute("""
    CREATE TABLE IF NOT EXISTS positions (
        fen TEXT,
        moves INT
    )
""")


# insert the positions into the database 10k at a time
inserts = []
for fen, moves in tqdm(mate_positions.items()):
    inserts.append([
        fen,
        moves
    ])

    if len(inserts) == 10000:
        cur.executemany(f"INSERT INTO positions (fen, moves) VALUES ({', '.join('?' for _ in inserts[0])})", inserts)
        inserts = []

if len(inserts) > 0:
    cur.executemany(f"INSERT INTO positions (fen, moves) VALUES ({', '.join('?' for _ in inserts[0])})", inserts)


con.commit()

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
    temp_df.to_sql(
        con = con,
        name = "data",
        index = False,
        if_exists = "append"
    )


cur.execute("DROP TABLE IF EXISTS positions")

con.close()
