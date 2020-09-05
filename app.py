#importing libraries

import pandas as pd
import numpy as np
import os


import plotly.express as px
import plotly.graph_objects as go
# import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_table
import dash_bootstrap_components as dbc

external_stylesheets = [dbc.themes.LUX]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server=app.server

# server=app.server
df=pd.read_csv('new_data/merged_global_ranks.csv')
ranks_df=df.drop(['Region','Cluster','Unnamed: 0'], axis=1)
ranks_df.drop(ranks_df[ranks_df['Rank']>50]. index,axis=0, inplace=True)
def get_reco(row,col):
    # if col <2:
        # print(df.iat[row,2])
    song_cluster=df.iat[row,5]
    song_rank=df.iat[row,3]
    reco_song_1=df[df['Cluster']==song_cluster]['Track_Name']
    reco_song_1.drop(song_rank-1, inplace=True)
    # print(type(reco_song_df))
        # reco_song_df.drop(song_rank-1, inplace=True)
        # reco_song_df.drop('index', axis=1, inplace=True)
    # else:
    song_artist=df.iat[row,4]
    print(song_artist)
    song_rank=df.iat[row,3]
    reco_song_df=df[df['Artist']==song_artist]['Track_Name']
    reco_song_df.drop(song_rank-1, inplace=True)
    #    print(type(reco_song_df))
    return (reco_song_1.head(),reco_song_df.head())


app.title = 'Song Recommender'

app.layout = html.Div(children=[
    dbc.Container
    ([
        dbc.Row
        ([
            dbc.Col(html.H1("Music Recommendation System"), className="mb-2 text-center", style = {'paddingTop':'20px'})
        ]),
        dbc.Row
        ([
            dbc.Col(html.H6(children='Item-based & User-Based Collaborative Filtering'), className="mb-4 text-center")
        ]),

    ]),
    dbc.Row
    ([
        dbc.Col(html.H5(children='Top Ranked Songs - Global'), className="mb-4 text-center"),
        dbc.Col(html.H5(children='Recommendations'), className="mb-4 text-center")
    ]),
    dbc.Row
    ([
        dbc.Col
        (
        
            dash_table.DataTable
            (
                id='table',
                columns=[{"name": i, "id": i} for i in ranks_df.columns],
                data=ranks_df.to_dict('records'),style_cell=
                {
                    'height': 'auto',
                    # all three widths are needed
                    'minWidth': '180px', 'width': '180px', 'maxWidth': '180px',
                    'whiteSpace': 'normal'
                },
                style_data=
                {
                    'width': '100px',
                    'maxWidth': '100px',
                    'minWidth': '100px',
                },
                style_cell_conditional=
                [
                         {'if': {'column_id': 'Artist'},
                         'width': '40%'},
                         {'if': {'column_id': 'Track_Name'},
                         'width': '40%'}
                ],
                page_action='none',
                style_table={'height': '360px', 'overflowY': 'auto'}
            ),
        ),
        dbc.Col
        ([
            html.Div(html.H6(children='Click on a track or artist from the table on the left, and we\'ll give you a recommendation!'), className="mb-4", style = {'padding-left':'20px','padding-right':'20px'}),
            html.Div(html.H6(children='Song Info'), className="mb-4 text-center"),
            dbc.Row
            ([
                dbc.Col(html.H6(children='Track Name:'), className="mb-4"),
                dbc.Col(html.Div(id='track_name',className="mb-4"),style = {'padding-left':'20px'})
            ]),
            dbc.Row
            ([
                dbc.Col(html.H6(children='Artist'), className="mb-4"),
                dbc.Col(html.Div(id='artist',className="mb-4"),style = {'padding-left':'20px'})
            ]),
            html.Div(html.H6(children='Recommendations'), className="mb-4 text-center"),
            dbc.Row
            ([
                dbc.Col(html.H6(children='Check out these songs that are similar to your choice:'), className="mb-4"),
                dbc.Col(html.Div(id='similar_songs',className="mb-4"),style = {'padding-left':'20px'})
            ]),
            dbc.Row
            ([
                dbc.Col(html.H6(children='Here are some songs by the same artist:'), className="mb-4",style = {'padding-left':'20px'}),
                dbc.Col(html.Div(id='same_artist',className="mb-4"))
            ])
                       
        ])
    ])   
])    

@app.callback([
    Output(component_id='track_name', component_property='children'),
    Output(component_id='artist', component_property='children'),
    Output(component_id='similar_songs', component_property='children'),
    Output(component_id='same_artist', component_property='children')],
     [Input('table', 'active_cell')]
            #    Input('table', 'data')]
)
def multi_output(active_cell):
    if active_cell:
        song_reco,artist_reco=get_reco(active_cell['row'], active_cell['column'])
        return (df.iloc[active_cell['row'],[2]],df.iloc[active_cell['row'],[4]],', '.join(song_reco),', '.join(artist_reco))
    else:
        return ('No selection','No selection','Make a selection, to get a recommendation here','Make a selection, to get a recommendation here')
        # return 'You\'ve entered "{}"'.format(active_cell)
        
        # return ranks_df.iat[active_cell['row'], active_cell['column']]
        # pd.DataFrame(data).iat[location['row'], location['column']]

# @app.callback(Output('selected-letter', 'children'),
#               [Input('table-one', 'active_cell'),
#                Input('table-one', 'data')])
# def get_active_letter(active_cell, data):
#     if active_cell:
#         return str(data[active_cell[0]]['Letter'])

if __name__ == '__main__':
    app.run_server(debug=True)

