import os
import pandas as pd
import re

# Define the directory containing the files
directory = '/home/grant/projects/batting/data/roster_data/'

# Create DataFrame to aggregate all individual roster files, then save them out to rosters.csv
rosters_df = pd.DataFrame()

for filename in os.listdir(directory):
    team = filename[0:3]
    year = filename[3:7]

    file_path = os.path.join(directory, filename)
    file_df = pd.read_csv(file_path, skiprows=1, header=None)

    
    file_df['team'] = team
    file_df['year'] = year

    rosters_df = pd.concat([rosters_df, file_df], ignore_index=True)

rosters_df = rosters_df.rename(columns = {
    0: 'Name',
    1: 'G',
    2: 'AB',
    3: 'R',
    4: 'H',
    5: '2B',
    6: '3B',
    7: 'HR',
    8: 'RBI',
    9: 'BB',
    10: 'IBB',
    11: 'SO',
    12: 'AVG',
    13: 'OBP',
    14: 'SLG'
})

rosters_df = rosters_df.sort_values(by='year')

rosters_df.to_csv('/home/grant/projects/batting/data/rosters.csv', index=False)

