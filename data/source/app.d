import std.stdio;
import std.string;
import std.algorithm;
import std.json: JSONException;
import std.conv: to;
import std.regex;
import std.range;

import asdf;


struct Move
{
    string eval;
    string move;
}


void main(string[] args)
{
    File pgnFile = File(args[1], "r");

    while (!pgnFile.eof()) {
        string line = strip(pgnFile.readln());

        if (isMoveText(line))
        {
            Move[] moves = parseMoveText(line);

            if (moves.length == 0)
                continue;

            else if (moves[0].eval)
            {
                writeln(moves.serializeToJson());
            }
        }
    }
}


bool isMoveText(string input_line)
{
    int line_start = to!int(input_line.indexOf("1"));
    return (line_start == 0);
}


/*
Find all the moves in the line. Parse out the evaluation and the clock time
*/
Move[] parseMoveText(string input_line)
{
    Move[] moveOutput;

    static r = ctRegex!(`((([a-z]|[A-Z])+[1-8])+(=[A-Z])?|(O-O)|(O-O-O))((\+)?|(\?)?|(\!)?)+\s\{(\s\[%eval\s((-?\d+\.\d{0,2})|(#-?\d+))\])?\s\[%clk\s\d+:\d{2}:\d{2}\]\s\}`);
    static move_reg = ctRegex!(`((([a-z]|[A-Z])+[1-8])+(=[A-Z])?|(O-O)|(O-O-O))((\+)?|(\?)?|(\!)?)+`);

    static has_eval = ctRegex!(`\[%eval\s((-?\d+\.\d{0,2})|(#-?\d+))\]`);
    static extract_eval = ctRegex!(`(-?\d+\.\d{0,2})|(#-?\d+)`);
    foreach (move; matchAll(input_line, r))
    {
        Move curMove;
        curMove.move = matchFirst(move.hit, move_reg).hit;

        // evaluation is an optional piece, so we need to make sure we have the eval here
        auto evaluation = move.hit.matchFirst(has_eval);
        if (!evaluation.empty)
            curMove.eval = evaluation.hit.matchFirst(extract_eval).hit;

        moveOutput ~= curMove;
    }

    return moveOutput;
}
