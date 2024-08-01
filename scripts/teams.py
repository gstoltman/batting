import pandas as pd

df = pd.read_csv('/home/grant/projects/batting/data/rosters.csv')

unique = df['team'].unique()

teams_dict = {
    'CHN': 'Cubs',
    'BOS': 'Red Sox',
    'CHA': 'White Sox',
    'SLN': 'Cardinals',
    'CN5': 'Reds',
    'ANG': 'Unknown',
    'MIA': 'Marlins',
    'TEX': 'Rangers',
    'PIT': 'Pirates',
    'LAN': 'Dodgers',
    'SDN': 'Padres',
    'WS0': 'Nationals',
    'ARI': 'Diamondbacks',
    'TOR': 'Blue Jays',
    'TBR': 'Rays',
    'SEA': 'Mariners',
    'BAL': 'Orioles',
    'ATL': 'Braves',
    'HOA': 'Astros',
    'KCA': 'Royals',
    'PHI': 'Phillies',
    'CLE': 'Indians',
    'MIN': 'Twins',
    'NYN': 'Mets',
    'ML4': 'Brewers',
    'OAK': 'Athletics',
    'COL': 'Rockies',
    'DET': 'Tigers',
    'NYA': 'Yankees',
    'SFN': 'Giants',
    'CLG': 'Guardians'
    }

print(unique)

