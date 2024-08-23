from dash import Dash, html, dash_table, dcc, callback, Output, Input
import copy
from google.cloud import storage
from io import StringIO
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd

#if 'GOOGLE_APPLICATION_CREDENTIALS' not in os.environ:
#    raise EnvironmentError('GOOGLE_APPLICATION_CREDENTIALS environment variable not set.')

# client = storage.Client()
# 
# bucket_name = 'rosters-bucket'
# blob_name = 'https://storage.cloud.google.com/rosters-bucket/rosters.csv'
# 
# bucket = client.bucket(bucket_name)
# 
# blob = bucket.blob(blob_name)
# 
# csv_string = blob.download_as_text()
# 
# df = pd.read_csv(StringIO(csv_string))

df_path = '~/projects/batting/data/rosters.csv'

df = pd.read_csv(df_path)

app = Dash()

stat_list = ['G','AB','R','H','2B','3B','HR','RBI','BB','IBB','SO','AVG','OBP','SLG']

max_stat = {}

for i in stat_list:
    max_stat[i] = df[i].max()

# Define the layout
app.layout = html.Div([
    html.Label('Select Player:', style={'color': 'white'}),
    dcc.Dropdown(
        id='player-dropdown',
        options=[{'label': name, 'value': name} for name in df['Name'].unique()],
        value=df['Name'].unique()[0], # Default value
        style={'margin-bottom': '20px'}
    ),
    html.Label('Select Stat:', style={'color': 'white'}),
    dcc.Dropdown(
        id='stat-dropdown',
        options=[{'label': stat, 'value': stat} for stat in stat_list],
        value=stat_list[0]
    ),
    dcc.Graph(id='line-chart')
])

# Define the callback to update the graph
@app.callback(
    Output('line-chart', 'figure'),
    [Input('player-dropdown', 'value'),
    Input('stat-dropdown', 'value')]
)
def update_graph(selected_player, selected_stat):
    # Filter data for the selected player
    filtered_df = df[df['Name'] == selected_player]
    chosen_stat = selected_stat

    # Define different color segments
    colors = ['blue', 'green', 'red', 'purple']
    color_map = {
        'CHN': '#0E3386',
        'BOS': '#BD3039',
        'CHA': '#27251F',
        'SLN': '#C41E3A ',
        'CN5': '#C6011F',
        'ANG': '#BA0021',
        'MIA': '#00A3E0',
        'TEX': '#003278',
        'PIT': '#FDB827',
        'LAN': '#005A9C',
        'SDN': '#2F241D',
        'WS0': '#AB0003',
        'ARI': '#A71930',
        'TOR': '#134A8E',
        'TBR': '#092C5C',
        'SEA': '#005C5C',
        'BAL': '#DF4601',
        'ATL': '#CE1141',
        'HOA': '#EB6E1F',
        'KCA': '#004687',
        'PHI': '#E81828',
        'CLE': '#E50022',
        'MIN': '#002B5C',
        'NYN': '#FF5910',
        'ML4': '#12284B',
        'OAK': '#003831',
        'COL': '#333366',
        'DET': '#FA4616',
        'NYA': '#27251F',
        'SFN': '#FD5A1E',
        'CLG': '#E50022'
    }

    
    # Create the figure
    fig = go.Figure()

    # Add segments one by one based on teams
    for i, team in enumerate(filtered_df['team'].unique()):
        team_df = filtered_df[filtered_df['team'] == team].sort_values(by='year')
        color = color_map.get(team)
        fig.add_trace(go.Scatter(
            x=team_df['year'],
            y=team_df[chosen_stat],
            mode='lines+markers+text',
            line=dict(color=color, width=7),
            marker=dict(size=20),
            text=team_df[chosen_stat],
            textposition='top center',
            textfont=dict(size=16, family='Arial Black'),
            name=f'{team}'
        ))

    # Update layout
    fig.update_layout(
        height=800,
        paper_bgcolor='#626366',
        plot_bgcolor='#c5c7cd',
        title=dict(
            text=f'{selected_player}: {chosen_stat} per Year',
            font=dict(color='#FFFFFF', size=24),
            x=0.5,
            xanchor='center'
        ),
        xaxis=dict(
            range=[2014, 2024],
            title=dict(
                text='Year',
                font=dict(color='#FFFFFF', size=20)
            ),
            tickfont=dict(color='#FFFFFF', size=16)
        ),
        yaxis=dict(
            range=[0, max_stat[chosen_stat]],
            title=dict(
                text=chosen_stat,
                font=dict(color='#FFFFFF', size=20)
            ),
            tickfont=dict(color='#FFFFFF', size=16)
        ),
        legend=dict(
            font=dict(color='#FFFFFF')
        ),
        showlegend=True
    )

    return fig

if __name__ == '__main__':
    app.run(port=8051, debug=True)
