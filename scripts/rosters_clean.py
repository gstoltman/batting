import os
import pandas as pd
import re

# Define the directory containing the files
directory = '../data/roster_exports/'

# Define the regex pattern to match files with years 2015 to 2024
years_pattern = re.compile(r'.*(201[5-9]|202[0-4]).*')

# Iterate over the files in the directory
for filename in os.listdir(directory):
    # Check if the filename does not match the pattern
    if not years_pattern.match(filename):
        # Construct the full file path
        file_path = os.path.join(directory, filename)
        # Delete the file
        os.remove(file_path)
        print(f'Deleted: {filename}')

# Create DataFrame to aggregate all individual roster files, then save them out to rosters.csv
teams_df = pd.DataFrame()

for filename in os.listdir(directory):
    year = filename[3:7]

    file_path = os.path.join(directory, filename)
    file_df = pd.read_csv(file_path, header=None)
    
    file_df = file_df.rename(columns={0: 'PLAYERID', 1: 'LAST', 2: 'FIRST', 3: 'BATHAND', 4: 'THROWHAND', 5:'TEAM_CODE', 6:'POSITION'})
    file_df['YEAR'] = year

    teams_df = pd.concat([teams_df, file_df], ignore_index=True)

    teams_df.to_csv('../data/rosters.csv', index=False)

roster_pattern = re.compile(r'.*\.ROS$')

# Clean up and delete redundant roster files
# for filename in os.listdir(directory):
#     # Check if the filename does not match the pattern
#     if roster_pattern.match(filename):
#         # Construct the full file path
#         file_path = os.path.join(directory, filename)
#         # Delete the file
#         os.remove(file_path)
#         print(f'Deleted: {filename}')

