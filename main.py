from dash import Dash, html, dash_table, dcc, callback, Output, Input
import copy
import plotly.express as px
import pandas as pd

df = pd.read_csv('./data/battingfacts.csv')

app = Dash()

app.layout = [
    html.H1(children='Batting Averages', style={'textAlign':'center'}),
    dcc.Dropdown(id='team', options=df.TEAM_CODE.unique()),
    dcc.Dropdown(id='player', options=df.NORMALIZED_NAME.unique()),
    dcc.Graph(id='line'),
    dash_table.DataTable(id='table', data=df.to_dict('records'), page_size=10)
]

@callback(
    Output('player', 'options'),
    Input('team', 'value')
)

def chained_callback_player(team):
    dff = copy.deepcopy(df)
    if team is not None:
        dff = dff.query('TEAM_CODE == @team')
    return sorted(dff['NORMALIZED_NAME'].unique())

@callback(
    Output('team', 'options'),
    Input('player', 'value')
)

def chained_callback_team(player):
    dff = copy.deepcopy(df)
    if player is not None:
        dff = dff.query('NORMALIZED_NAME == @player')
    return dff['TEAM_CODE'].unique()

@callback(
    Output("table", "table"),
    Input("player", "value"),
    Input("team", "value"),
)

@callback(
    Output("line", "figure"),
    Input("player", "value"),
    Input("team", "value"),
)

def line_chart(player, team):
    dff = copy.deepcopy(df)
    if player is not None:
        dff = dff.query('NORMALIZED_NAME == @player')
    if team is not None:
        dff = dff.query('TEAM_CODE == @team')
    
    fig = px.line(dff, x='year', y='batting_avg')

    fig.update_xaxes(range=[2015, 2023])
    fig.update_yaxes(range=[0, .400])

    return fig

if __name__ == '__main__':
    app.run(port=8051, debug=True)

