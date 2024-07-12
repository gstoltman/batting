import pandas as pd
import unicodedata
import re

battingstats_path = '../data/battingstats.csv'
rosters_path = '../data/rosters.csv'

battingstats_df = pd.read_csv(battingstats_path)
rosters_df = pd.read_csv(rosters_path)

#normalize letters from battingstats
def normalize_text(name):
    name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('utf-8')
    return name

battingstats_df['NORMALIZED_NAME'] = battingstats_df['last_name, first_name'].apply(normalize_text)

# Split 'last_name, first_name' column in battingstats
battingstats_df[['last_name', 'first_name']] = battingstats_df['NORMALIZED_NAME'].str.split(', ', expand=True)
print(battingstats_df.head())

# Merge to new DF and drop unnecessary columns
merged_df = pd.merge(battingstats_df, rosters_df, left_on=['last_name', 'first_name', 'year'], right_on=['LAST', 'FIRST', 'YEAR'], how='inner')
merged_df = merged_df.drop(columns=['last_name', 'first_name', 'LAST', 'FIRST', 'YEAR'])

# Reorder columns to place PLAYERID at the start
columns = ['PLAYERID'] + [col for col in merged_df.columns if col != 'PLAYERID']
merged_df = merged_df[columns]

merged_df.to_csv('../data/battingfacts.csv', index=False)
