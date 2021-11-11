import pandas as pd

import dash
import dash_html_components as html
import dash_table
import dash_bootstrap_components as dbc

from navbar import Navbar

df = pd.read_csv('new_data/merged_global_ranks.csv')
ranks_df = df.drop(['Region', 'Cluster', 'Unnamed: 0'], axis=1)
ranks_df.drop(ranks_df[ranks_df['Rank'] > 50].index, axis=0, inplace=True)

nav = Navbar()

title = dbc.Container([
    dbc.Row([
        dbc.Col(html.H5(children='Top Ranked Songs - Global'), className="mb-4 text-center"),
        dbc.Col(html.H5(children='Recommendations'), className="mb-4 text-center")
    ],
        style={'padding-top': '30px'}
    ),
])

card_song_info = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Song Info", className="card-title text-center"),
            dbc.Row([
                dbc.Col(html.H6(children='Track Name:'), className="mb-4", style={'padding-top': "10px"}),
                dbc.Col(html.H6(id='track_name', className="mb-4", style={'padding-top': "10px"})),
                dbc.Col(html.H6(children='Artist:'), className="mb-4", style={'padding-top': "10px"}),
                dbc.Col(html.H6(id='artist', className="mb-4", style={'padding-top': "10px"}))
            ]),
        ],

    ),
    style={"height": "200px"}
)

songs = dbc.Card(
    dbc.CardBody(
        [
            # dbc.CardHeader("Similar Songs", className= "text-center",),
            html.H4("Similar Songs", className="card-title text-center"),
            dbc.Row
            ([dbc.Col(html.Div(id='similar_songs', className="mb-4 text-center", style={'padding-top': "10px"}))]),
        ],
        style={"height": "220px", }, ),
)
artist = dbc.Card(
    dbc.CardBody(
        [
            html.H4("Same Artist", className="card-title text-center"),
            dbc.Row
                ([
                dbc.Col(html.Div(id='same_artist', className="mb-4 text-center", style={'padding-top': "10px"})),

            ], justify="around"),
        ],
        style={"height": "220px"}),
)

body = dbc.Container([
    dbc.Row([
        dbc.Col
        (dash_table.DataTable
         (id='table', columns=[{"name": i, "id": i} for i in ranks_df.columns],
          data=ranks_df.to_dict('records'), style_cell=
          {
              'height': 'auto',
              'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
              'whiteSpace': 'normal'
          },
          style_data=
          {
              'width': '100px',
              'maxWidth': '100px',
              'minWidth': '100px',
              'border': '1px solid black'
          },
          style_cell_conditional=
          [
              {'if': {'column_id': 'Artist'},
               'textAlign': 'left'},
              {'if': {'column_id': 'Track_Name'},
               'textAlign': 'left'}
          ], page_action='none', style_table={'height': '360px', 'overflowY': 'auto'},
          style_header={'border': '1px solid black'},
          ), className="table-bordered "
         ),
        dbc.Col([html.Div(html.H6(
            children='Click on your favourtie track or artist from the table on the left, and we\'ll give you a '
                     'recommendation!'),
            className="mb-4", style={'padding-left': '40px'}),
            dbc.Row([dbc.Col(songs, width=6), dbc.Col(artist, width=6)], style={'padding-bottom': '15px'}),
            dbc.Row([dbc.Col(card_song_info, width=12)], style={'padding-bottom': '15px', 'padding-left': '50px', })
        ],
            style={"margin-left": "20px", "margin-right": "20px"})
    ],
        style={"margin-bottom": "30px"})
])


def App():
    layout = html.Div([
        nav,
        title,
        body

    ])

    return layout


app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])
app.layout = App()
