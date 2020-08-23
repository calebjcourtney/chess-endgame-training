# Creating the Data

## Why is this necessary
Because the decision tree for chess is so large, I opted to use a database of already existing games from [lichess.org](database.lichess.org) that people have actually played, and pull the data from that.

## How the import works
I've added a helpful `bash` file for automating the database creation process. You can run it from the command line with `./import_process_data.sh`. The data runs in three steps:

1. wget the data in the urls from `list.txt`. Please note that the larger files from [lichess.org](lichess.org) may take 30 minutes or more to download.
2. `bunzip` the data in the `bz2` files (please note that you will need `lbzip2` for this to work, since `lbunzip2` is faster than just `bunzip2`).
3. run the python script `process_games.py`.

The python script does the majority of the heavy lifting, parsing the data and loading it into an sqlite database. Please note that it assumes the `.pgn` files will be in the same directory as where execution is happening.
