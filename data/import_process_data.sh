#!/bin/bash

# list.txt contains urls for the open source games on lichess.org
echo "downloading files"
wget - i list.txt

# run the python script for parsing the pgn into the database
# this can take a very long time to run
echo "parsing games and loading to database"
zstdcat *.pgn.zst | grep 'eval' | grep '#' | grep -v '#-' | python process_games.py

# clean up the files used in processing
# if running for the first time, I would recommend commenting these lines out,
# so this bash script doesn't remove these files and you have to start over if something goes wrong
echo "cleaning up intermediate files"
rm *.pgn.szt
rm lichess_mate_games.txt
rm moves.jsonl
