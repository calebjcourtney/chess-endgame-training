import base64
import sqlite3

import pandas as pd
import flask

import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html

# local generation
from position.generator import create_position_file


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

server = flask.Flask(__name__)
app = dash.Dash(__name__, server=server, external_stylesheets = external_stylesheets)


app.layout = html.Div(
    children=[
        html.H1(children='Checkmate Generator', style = {"text-align": "center"}),
        dcc.Markdown("***"),
        html.Div(
            [
                html.Div(dcc.Markdown("###### Select checkmate in a number of moves:"), className = "six columns"),
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
        dcc.Markdown("***"),
        html.Div(
            [
                html.H3(id = "mate-in-x-text"),
                html.Img(id= 'chess-image', src='initial.svg', width = 550)
            ],
            style = {"text-align": "center"}
        ),

        html.Div(id = "fen-text", style = {'display': 'none'})
    ],
    className = "container"
)


@app.callback(
    Output(component_id='mate-in-x-text', component_property='children'),
    [Input(component_id='fen-text', component_property='children')]
)
def update_mate_image(fen):
    con = sqlite3.connect("data/db.sqlite3")
    sql = f"SELECT moves FROM data WHERE fen = '{fen}' LIMIT 1"
    df = pd.read_sql_query(sql, con)

    mate_in_x = df['moves'].tolist()[0]
    return f'White to move. Mate in {mate_in_x}.'


@app.callback(
    Output(component_id='chess-image', component_property='src'),
    [Input(component_id='fen-text', component_property='children')]
)
def update_mate_text(fen):
    svg_file = create_position_file(fen)

    encoded = base64.b64encode(open(svg_file, 'rb').read())
    svg = 'data:image/svg+xml;base64,{}'.format(encoded.decode())

    return svg


@app.callback(
    Output(component_id='fen-text', component_property='children'),
    [Input(component_id='mate-in-x', component_property='value')]
)
def update_fen_text(mate_in_x):
    con = sqlite3.connect("data/db.sqlite3")
    sql = "SELECT * FROM data WHERE moves {} ORDER BY RANDOM() LIMIT 1".format("> 0" if mate_in_x == 0 else f"= {mate_in_x}")
    df = pd.read_sql_query(sql, con)

    fen = df['fen'].tolist()[0]

    return fen


if __name__ == '__main__':
    app.run_server(debug=True)
