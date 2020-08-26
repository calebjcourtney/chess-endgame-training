"""Summary

Attributes:
    app (TYPE): Description
    external_stylesheets (list): Description
    server (TYPE): Description
"""

# native python libraries
import base64
import sqlite3

# chess libraries
import chess
import chess.svg

# plotly libraries for creating the app
import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

# other 3rd party libraries
import pandas as pd
import flask

# thanks to chris from plotly for the following css:
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets = external_stylesheets)

app.title = 'Chess with UnaSalusVictis'

app.layout = html.Div(
    children=[
        # free favicon obtained from here:
        # https://www.flaticon.com/free-icon/knight_2910867?term=chess&page=1&position=9
        html.Link(rel="shortcut icon", href="https://image.flaticon.com/icons/svg/2910/2910867.svg"),
        html.H1(children='Checkmate Generator', style = {"text-align": "center"}),
        # horizontal line
        dcc.Markdown("***"),
        # inputs for if you want to solve in x number of moves (or keep it as randomly selected)
        html.Div(
            [
                html.Div(html.H6("Select checkmate in a number of moves:"), className = "six columns"),
                html.Div(
                    dcc.Dropdown(
                        id='mate-in-x',
                        options=[{'label': x if x > 0 else "Random", 'value': x} for x in range(11)],
                        value=0
                    ),
                    className = "six columns"
                )
            ],
            className = "row"
        ),
        # another horizontal line
        dcc.Markdown("***"),
        # link to the local svg for displaying the image
        html.Div(
            [
                html.H3(id = "mate-in-x-text"),
                html.Img(id= 'chess-image', src='initial.svg', width = 550)
            ],
            style = {"text-align": "center"}
        ),
        # hidden div of the chess fen for use in creating the svg and "mate in x" text
        html.Div(id = "fen-text", style = {'display': 'none'})
    ],
    className = "container"
)


@app.callback(
    Output(component_id='mate-in-x-text', component_property='children'),
    [Input(component_id='fen-text', component_property='children')]
)
def update_mate_image(fen: str) -> str:
    """Use the fen to query from the database the number of moves it will take for white to give checkmate.

    Args:
        fen (str): the FEN representation of the chess board setup

    Returns:
        str: A string representation of the number of moves it will take for white to give checkmate
    """
    # get the number of moves from the database
    con = sqlite3.connect("data/db.sqlite3")
    sql = f"SELECT moves FROM data WHERE fen = '{fen}' LIMIT 1"
    df = pd.read_sql_query(sql, con)

    mate_in_x = df['moves'].tolist()[0]
    return f'White to move. Mate in {mate_in_x}.'


@app.callback(
    Output(component_id='chess-image', component_property='src'),
    [Input(component_id='fen-text', component_property='children')]
)
def update_mate_text(fen: str) -> str:
    """Use the fen to generate the SVG in chess and return it as an image to the app

    Args:
        fen (str): the FEN representation of the chess board setup

    Returns:
        str: the encoded image data for rendering the chess position
    """
    board = chess.Board(fen)
    out_string = chess.svg.board(board)

    fen_position = bytes(out_string, 'utf-8')

    encoded = base64.b64encode(fen_position)
    svg = 'data:image/svg+xml;base64,{}'.format(encoded.decode())

    return svg


@app.callback(
    Output(component_id='fen-text', component_property='children'),
    [Input(component_id='mate-in-x', component_property='value')]
)
def update_fen_text(mate_in_x: int) -> str:
    """Randomly generates a new chess position, based on the mate in x input

    Args:
        mate_in_x (int): the number of moves for white to mate

    Returns:
        str: the FEN representation of the chess board setup
    """
    con = sqlite3.connect("data/db.sqlite3")
    sql = "SELECT * FROM data WHERE moves {} ORDER BY RANDOM() LIMIT 1".format("> 0" if mate_in_x == 0 else f"= {mate_in_x}")
    df = pd.read_sql_query(sql, con)

    fen = df['fen'].tolist()[0]

    return fen


if __name__ == '__main__':
    app.run_server(debug=True)
