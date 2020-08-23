#!/bin/bash

# list.txt contains urls for the open source games on lichess.org
echo "downloading files"
wget - i list.txt

# you will need to have lbunzip installed
echo "uncompressing files"
lbunzip2 * .bz2

# parse out the games with mate in x evaluations for white (but not black)
echo "parsing games"
cat *.pgn | grep 'eval' | grep '#' | grep -v '#-' > lichess_mate_games.txt

# build the dlang chess parser
dub build

# use the faster d language to parse the games from the algebraic notation into json format, which will be faster for python to handle
# even so, this still took 15 minutes to run. Better than the process that estimated would take days in python, but still takes a while
./lichess_parser lichess_mate_games.txt > moves.jsonl

# run the python script for turning the output from the parser into a database
# this takes approximately 45 minutes to run on my machine
python3 process_games.py

# clean up the files used in processing
# if running for the first time, I would recommend commenting these lines out,
# so this bash script doesn't remove these files and you have to start over if something goes wrong
rm *.pgn
rm lichess_mate_games.txt
rm moves.jsonl
