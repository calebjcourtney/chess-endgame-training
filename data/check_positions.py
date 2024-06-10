import chess
import chess.engine

import sqlite3
from tqdm import tqdm

con = sqlite3.connect("db.sqlite3")
cur = con.cursor()

cur.execute("SELECT fen, moves FROM data ORDER BY moves DESC")
positions = cur.fetchall()

remove_positions = set()

engine = chess.engine.SimpleEngine.popen_uci("stockfish")

for fen, moves in tqdm(positions):
    board = chess.Board(fen)
    info = engine.analyse(board, chess.engine.Limit(depth=moves * 2 + 5))
    if not info["score"].is_mate():
        remove_positions.add(fen)

engine.quit()


print(list(remove_positions)[:10])

print(len(remove_positions), "positions to remove")
# remove the positions from the data table
for fen in tqdm(remove_positions):
    cur.execute(f"DELETE FROM data WHERE fen = ?", (fen,))
