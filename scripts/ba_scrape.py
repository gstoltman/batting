import os
import requests
from bs4 import BeautifulSoup
import pandas as pd

team_list = ["BAL", "PHI", "NYA", "ATL", "BOS", "NYN", "TBR", "WS0", "TOR", "MIA", "CLE", "ML4", "MIN", "SLN", "KCA", "PIT", "DET", "CHN", "CHA", "CN5", "SEA", "LAN", "HOA", "SDN", "TEX", "ARI", "ANG", "SFN", "OAK", "COL"]

team = input('Enter team code (3 digits): ')
min_year = int(input('Enter min year: '))
max_year = int(input('Enter max year: '))

def scrape(team, year):
    base_url = 'https://www.baseball-almanac.com/teamstats/hitting.php?y='
    team_url_part = f'{team}'

    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    year_url_part = f'{year}'
    full_url = base_url + year_url_part + '&t=' + team_url_part

    response = requests.get(full_url, headers=headers)

    if response.status_code != 200:
        print(f"Failed to retrieve the webpage for year {year}. Status code: {response.status_code}")
        exit()
    
    soup = BeautifulSoup(response.content, 'html.parser')
    table = soup.find('table', {'id': 'hitting-stats'})
    headers = []
    seen = set()

    for header in table.find_all('th', class_='banner'):
        header_text = header.text.strip()
        if header_text not in seen:
            headers.append(header_text)
            seen.add(header_text)

    rows = []
    for row in table.find_all('tr')[2:]:  # Skip the first two header rows
        cols = row.find_all('td')
        if cols:
            row_data = [col.text.strip() for col in cols]
            if len(row_data) == len(headers):  # Ensure row data matches the number of headers
                rows.append(row_data)

    df = pd.DataFrame(rows, columns=headers)
    df['Name'] = df['Name'].apply(lambda x: x.split('\r\n')[-1].strip())
    
    # Save to csv
    directory = '/home/grant/projects/batting/data/roster_data/'
    file_name = f'{team}{year}roster'
    file_path = os.path.join(directory, file_name)
    df.to_csv(file_path, index=False)

for year in range(min_year, max_year+1):
    scrape(team, year)