from dash import Dash, html, dash_table, dcc, callback, Output, Input
import copy
import plotly.express as px
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import pandas as pd

df = pd.read_csv('/home/grant/projects/batting/data/rosters.csv')

app = Dash()

# Define the layout
app.layout = html.Div([
    dcc.Dropdown(
        id='player-dropdown',
        options=[{'label': name, 'value': name} for name in df['Name'].unique()],
        value=df['Name'].unique()[0]  # Default value
    ),
    dcc.Graph(id='line-chart')
])

# Define the callback to update the graph
@app.callback(
    Output('line-chart', 'figure'),
    Input('player-dropdown', 'value')
)
def update_graph(selected_player):
    # Filter data for the selected player
    filtered_df = df[df['Name'] == selected_player]

    # Define different color segments
    colors = ['blue', 'green', 'red', 'purple']
    color_map = {
        'CHN': 'blue', 'BOS': 'red', 'CHA': 'black', 'SLN': 'red', 'CN5': 'red', 'ANG': 'grey', 'MIA': 'orange', 'TEX': 'red', 'PIT': 'yellow', 'LAN': 'blue', 'SDN': 'yellow', 'WS0': 'red', 'ARI': 'maroon', 'TOR': 'blue', 'TBR': 'darkblue', 'SEA': 'darkblue', 'BAL': 'orange', 'ATL': 'red', 'HOA': 'orange', 'KCA': 'blue', 'PHI': 'red', 'CLE': 'red', 'MIN': 'red', 'NYN': 'orange', 'ML4': 'darkblue', 'OAK': 'green', 'COL': 'purple', 'DET': 'orange', 'NYA': 'black', 'SFN': 'orange', 'CLG': 'red'
    }

    
    # Create the figure
    fig = go.Figure()

    # Add segments one by one based on teams
    for i, team in enumerate(filtered_df['team'].unique()):
        team_df = filtered_df[filtered_df['team'] == team].sort_values(by='year')
        color = color_map.get(team)
        fig.add_trace(go.Scatter(
            x=team_df['year'],
            y=team_df['AVG'],
            mode='lines+markers',
            line=dict(color=color, width=7),
            marker=dict(size=20),
            name=f'{team}'
        ))

    # Update layout
    fig.update_layout(
        paper_bgcolor='darkgrey',
        plot_bgcolor='darkgrey',
        title=f'Batting Average (AVG) Over Years for {selected_player}',
        xaxis_title='Year',
        yaxis_title='Batting Average',
        xaxis=dict(range=[2014, 2024], tickmode='linear'),
        yaxis=dict(range=[.15, .35], tickformat='.3f'),
        showlegend=True
    )

    return fig

if __name__ == '__main__':
    app.run(port=8051, debug=True)
