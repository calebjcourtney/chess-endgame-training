import std.stdio;
import std.string;
import std.conv: to;
import std.regex;

import asdf;

// the basic components of a chess move - the move itself and the evaluation of the move
struct Move
{
    string eval;
    string move;
}

// given a filename as input, parse the data
void main(string[] args)
{
    File pgnFile = File(args[1], "r");

    // iterate through the input file
    while (!pgnFile.eof()) {
        string line = strip(pgnFile.readln());

        if (isMoveText(line))
        {
            // parse all the moves from the text file
            Move[] moves = parseMoveText(line);

            if (moves.length == 0)
                continue;

            // output the data to json
            else if (moves[0].eval)
            {
                writeln(moves.serializeToJson());
            }
        }
    }
}

// check that the file is, in fact, a move - it should be, since that's what we've already parsed
bool isMoveText(string input_line)
{
    int line_start = to!int(input_line.indexOf("1"));
    return (line_start == 0);
}


// Find all the moves in the line. Parse out the evaluation and the clock time
Move[] parseMoveText(string input_line)
{
    Move[] moveOutput;

    // this is where the major improvement over python was - the compile-time regex was able to run at 10-15x the speed of the python regex
    static r = ctRegex!(`((([a-z]|[A-Z])+[1-8])+(=[A-Z])?|(O-O)|(O-O-O))((\+)?|(\?)?|(\!)?)+\s\{(\s\[%eval\s((-?\d+\.\d{0,2})|(#-?\d+))\])?\s\[%clk\s\d+:\d{2}:\d{2}\]\s\}`);
    static move_reg = ctRegex!(`((([a-z]|[A-Z])+[1-8])+(=[A-Z])?|(O-O)|(O-O-O))((\+)?|(\?)?|(\!)?)+`);

    static has_eval = ctRegex!(`\[%eval\s((-?\d+\.\d{0,2})|(#-?\d+))\]`);
    static extract_eval = ctRegex!(`(-?\d+\.\d{0,2})|(#-?\d+)`);

    // for each match in the line
    foreach (move; matchAll(input_line, r))
    {
        // parse the move from the text
        Move curMove;
        curMove.move = matchFirst(move.hit, move_reg).hit;

        // parse the evaluation from the text
        auto evaluation = move.hit.matchFirst(has_eval);
        curMove.eval = evaluation.hit.matchFirst(extract_eval).hit;

        moveOutput ~= curMove;
    }

    return moveOutput;
}
