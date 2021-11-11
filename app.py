import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc

from recommender import App, df
from homepage import Homepage

app = dash.Dash(__name__, external_stylesheets=[dbc.themes.UNITED])

app.title = "Music Recommendations"
server = app.server
app.config.suppress_callback_exceptions = True

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == '/app':
        return App()
    else:
        return Homepage()


def get_recommendation(row, col):
    song_cluster = df.iat[row, 5]
    song_rank = df.iat[row, 3]
    reco_song_1 = df[df['Cluster'] == song_cluster]['Track_Name']
    reco_song_1.drop(song_rank - 1, inplace=True)
    song_artist = df.iat[row, 4]
    song_rank = df.iat[row, 3]
    reco_song_df = df[df['Artist'] == song_artist]['Track_Name']
    reco_song_df.drop(song_rank - 1, inplace=True)
    return reco_song_1.head(), reco_song_df.head()


@app.callback([
    Output(component_id='track_name', component_property='children'),
    Output(component_id='artist', component_property='children'),
    Output(component_id='similar_songs', component_property='children'),
    Output(component_id='same_artist', component_property='children')],
    [Input('table', 'active_cell')]
)
def multi_output(active_cell):
    if active_cell:
        song_recommendation, artist_recommendation = get_recommendation(active_cell['row'], active_cell['column'])
        return (df.iloc[active_cell['row'], [2]], df.iloc[active_cell['row'], [4]], ', '.join(song_recommendation),
                ', '.join(artist_recommendation))
    else:
        return ('No selection', 'No selection', 'Make a selection, to get a recommendation here',
                'Make a selection, to get a recommendation here')


if __name__ == '__main__':
    app.run_server(debug=True)
