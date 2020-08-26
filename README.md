# Chess Endgame Training

This app was created as part of the Tech with Tim August `Timathon` challenge. The goal of the project is to create a lightweight application that can generate chess positions for finding checkmate in a certain number of moves.

***
## Data Creation
For more complete explanation on this, see the [data](https://github.com/calebjcourtney/chess-endgame-training/tree/master/data) folder. The majority of the work that went into this project was based on having to take chess games and parse out positions that were mate in a certain number of moves. Because of the large decision tree in chess, I could not find a fast way to generate this data ad hoc. Instead I used the [open database from lichess.org](database.lichess.org) and used games from actual players as the basis for the database.

To save on disk space, only 10k positions for each move option was kept. This results in a database of 100k checkmating patterns, which should be sufficient for most people to not see a duplicate position for a long time.

***
## How the App Works
Since the majority of the work was pre-processing the chess positions, the generation portion is a simple query to an sqlite database:
```python
con = sqlite3.connect("data/db.sqlite3")
# gets a random chess position from the database
sql = """
	SELECT *
	FROM data
	WHERE moves {}
	ORDER BY RANDOM()
	LIMIT 1""".format("> 0" if mate_in_x == 0 else f"= {mate_in_x}")

# pandas is just so convenient for these queries, even if it is overkill
df = pd.read_sql_query(sql, con)
```

***
The visualization portion of the application uses the [Dash library](https://dash.plotly.com/) from Plotly. I like this because it allows me to keep the entire application (even the components based on `React.JS`) in python, where I'm most comfortable. The application is broken down into three pieces:
1. The FEN (chess position) text - this component is hidden, but used as a reference by the next two components.
2. The selection of number of white moves to checkmate - this component is a dropdown option for any number of different positions.
3. The resulting image, based on the selection, with randomness.

***
## Ideas for improvement
The first thought that comes to mind is simply expanding to a larger database of positions. Currently, there are only 100k possible positions to generate, and there should be many, many (incalculably many) more.

A second idea for improvement is to actually allow the user to play the position. This would require a much greater understanding of JavaScript than I have and goes beyond the scope of this project anyways.

Lastly, and somewhat tied to the second improvement, is the ability to give a hint for the first move to make to follow through on the checkmating pattern.
