import pandas as pd
# PoliCheck
#['id', 'race_id', 'state_abbrev', 'state', 'office_id', 'office_name','office_seat_name', 'cycle', 'stage', 'special', 'party','politician_id', 'candidate_id', 'candidate_name', 'ballot_party','ranked_choice_round', 'votes', 'percent', 'unopposed', 'winner','alt_result_text', 'source'],type='object')


def get_data(csv):
    df = pd.read_csv(csv)
    results = {}
    for index, row in df.iterrows():
        if type(row['state_abbrev']) == float:
            row['state_abbrev'] = "USA"
        if row['percent'] >= 3 and row['stage'] == 'general':
            if row['cycle'] not in results:
                results[row['cycle']] = {}
            if row['state_abbrev'] not in results[row['cycle']]:
                results[row['cycle']][row['state_abbrev']] = []
            results[row['cycle']][row['state_abbrev']].append({'candidate': row['candidate_name'],'party': row['ballot_party'],'percentage': row['percent'],'votes': row['votes']})
    return results


df = pd.read_csv("pres_pollaverages_1968-2016.csv")
years = []
print(df.columns)
print(df.columns)
