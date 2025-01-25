import pandas as pd
from datetime import datetime
# PoliCheck
#['id', 'race_id', 'state_abbrev', 'state', 'office_id', 'office_name','office_seat_name', 'cycle', 'stage', 'special', 'party','politician_id', 'candidate_id', 'candidate_name', 'ballot_party','ranked_choice_round', 'votes', 'percent', 'unopposed', 'winner','alt_result_text', 'source'],type='object')


def get_data_results(csv): # function putting 538s .csv file into a python dictionary to be used for data
    df = pd.read_csv(csv)
    results = {}
    for index, row in df.iterrows():
        if type(row['state_abbrev']) == float:
            row['state_abbrev'] = "USA" # converts null values into USA keyword (use "USA" in state column to access national data)
        if row['percent'] >= 3 and row['stage'] == 'general':
            if row['cycle'] not in results:
                results[row['cycle']] = {}
            if row['state_abbrev'] not in results[row['cycle']]:
                results[row['cycle']][row['state_abbrev']] = []
            results[row['cycle']][row['state_abbrev']].append({'candidate': row['candidate_name'],'party': row['ballot_party'],'percentage': row['percent'],'votes': row['votes']})
    return results

def get_data_polls(csv):
    df = pd.read_csv(csv)
    print(df.columns)
    results = {2020:{},2024:{}}
    for index, row in df.iterrows():
        if type(row['state']) == float:
            row['state'] = "USA"
        print(row['end_date'])
        date = (datetime.strptime(row['end_date'],"%m/%d/%y"))
        if datetime(2024,11,5) > date > datetime(2024,10,1):
            if row['pollster'] not in list(results[2024].keys()):
                if row['candidate_name'] == "Donald Trump":
                    date[2024][row['pollster']] = [row['pct'],0,1] # first element in list will be republican percentage totals for polling company, second will be democrat, and third is number of polls the company has
                elif row['candidate_name'] == "Kamala Harris":
                    date[2024][row['pollster']] = [0, row['pct'], 0] # count is not initilaized to prevent double counting
            else:
                if row['candidate_name'] == "Donald Trump":
                    date[2024][row['pollster']] += [row['pct'], 0,1]
                elif row['candidate_name'] == "Kamala Harris":
                    date[2024][row['pollster']] += [0, row['pct'], 0]
        if datetime(2020,11,3) > date > datetime(2024,10,1):


get_data_polls("538-poll-data/president_polls_historical-2018+.csv")