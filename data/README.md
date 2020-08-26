# Creating the Data

## Why is this necessary
Because the decision tree for chess is so large, I opted to use a database of already existing games from [lichess.org](database.lichess.org) that people have actually played, and pull the data from that. This means that the overall project turned into more of a data engineering project than a clever generation project.

## How the import works
I've added a helpful `bash` file for automating the database creation process. You can run it from the command line with `./import_process_data.sh`. The data runs in three steps:

1. `wget` the data in the urls from `list.txt`. Please note that the larger files from [lichess.org](lichess.org) may take 30 minutes or more to download.
2. `bunzip` the data in the `bz2` files (please note that you will need `lbzip2` for this to work, since `lbunzip2` is faster than just `bunzip2`).
3. Extract the lines of the data that have the moves and evaluations for the games.
4. build the `dub` process
5. run the `./lichess_parser`, which goes through the `lichess_mate_games.txt` file and parses each game of moves into a json object, primarily using `regex`. The reason I chose to use D in this case is that it ran much faster than my initial tests in python for parsing the games. Even parsing the data into `json`, then using python to parse the `json` was faster than using python to parse the `pgn` text.
6. run the python script `process_games.py`. This uploads the data into an sqlite file for the app to reference the data.

Please note that this entire process can take *many* hours to run, especially if you're downloading more than a single database file from [Lichess](database.lichess.org)
