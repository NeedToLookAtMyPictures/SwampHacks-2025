import pandas as pd
from datetime import datetime
import altair as alt
# PoliCheck
#['id', 'race_id', 'state_abbrev', 'state', 'office_id', 'office_name','office_seat_name', 'cycle', 'stage', 'special', 'party','politician_id', 'candidate_id', 'candidate_name', 'ballot_party','ranked_choice_round', 'votes', 'percent', 'unopposed', 'winner','alt_result_text', 'source'],type='object')
import matplotlib.pyplot as plt

def get_data_results(csv): # function putting 538s .csv file into a python dictionary to be used for data
    # USES STATE ABBREVIATIONS
    df = pd.read_csv(csv)
    results = {}
    for index, row in df.iterrows():
        if type(row['state']) == float:
            row['state'] = "USA" # converts null values into USA keyword (use "USA" in state column to access national data)
        if row['percent'] >= 10 and row['stage'] == 'general' and (row['cycle'] == 2020 or row['cycle'] == 2024):
            if row['cycle'] not in results:
                results[row['cycle']] = {}
            if row['state'] not in results[row['cycle']]:
                results[row['cycle']][row['state']] = []
            results[row['cycle']][row['state']].append({'candidate': row['candidate_name'],'party': row['ballot_party'],'percentage': row['percent'],'votes': row['votes']})
    return results

def get_data_polls(csv,state="USA",month=10):
    # USES STATES FULL NAMES BESIDES NATIONAL WHICH IS USA
    df = pd.read_csv(csv,low_memory=False)
    results = {2020:{},2024:{}}
    for index, row in df.iterrows():
        if type(row['state']) == float:
            row['state'] = "USA"
        date = (datetime.strptime(row['end_date'],"%m/%d/%y"))
        if (datetime(2024,11,5) > date > datetime(2024,month,1)) and row['state'] == state:
            if row['pollster'] not in list(results[2024].keys()):
                if row['candidate_name'] == "Donald Trump":
                    results[2024][row['pollster']] = [row['pct'],0,1] # first element in list will be republican percentage totals for polling company, second will be democrat, and third is number of polls the company has
                elif row['candidate_name'] == "Kamala Harris":
                    results[2024][row['pollster']] = [0, row['pct'], 0] # count is not initilaized to prevent double counting
            else:
                if row['candidate_name'] == "Donald Trump":
                    results[2024][row['pollster']] = list(map(lambda x,y: x+y, [row['pct'], 0,1],results[2024][row['pollster']]))
                elif row['candidate_name'] == "Kamala Harris":
                    results[2024][row['pollster']] = list(map(lambda x,y: x+y, [0, row['pct'],0],results[2024][row['pollster']]))
        if datetime(2020,11,3) > date > datetime(2020,month,1) and row['state'] == state:
            if row['pollster'] not in list(results[2020].keys()):
                if row['candidate_name'] == "Donald Trump":
                    results[2020][row['pollster']] = [row['pct'],0,1]
                elif row['candidate_name'] == "Kamala Harris":
                    results[2020][row['pollster']] = [0, row['pct'], 0]
            else:
                if row['candidate_name'] == "Donald Trump":
                    results[2020][row['pollster']] = list(map(lambda x,y: x+y, [row['pct'], 0,1],results[2020][row['pollster']]))
                elif row['candidate_name'] == "Joe Biden":
                    results[2020][row['pollster']] = list(map(lambda x,y: x+y, [0, row['pct'],0],results[2020][row['pollster']]))
    for i in [2020,2024]:
        for key, value in results[i].items():
            value[0] = value[0] / value[2]
            value[1] = value[1] / value[2]
    return results


def calculate_errors(results):
    errors = {2020: {}, 2024: {}}
    for y in [2020, 2024]:
        polls = get_data_polls("538-poll-data/president_polls_historical-2018+.csv")
        for j in list(polls[y].keys()):
            result = [x for x in results[y]["USA"] if x['candidate'] == "Donald Trump"]
            if result:
                result = result[0]
                resid = polls[y][j][0] - result['percentage']
                errors[y][j] = [resid.__round__(4), polls[y][j][2]]

    return errors


def transform_errors_to_df(errors):
    data = []

    for year, polls in errors.items():
        for poll_name, (error, num_polls) in polls.items():
            data.append({
                'Year': year,
                'Poll': poll_name,
                'Error': error,
                'Num Polls': num_polls
            })
    df = pd.DataFrame(data)
    return df
def plot_errors(df):
    chart = alt.Chart(df).mark_point(fillOpacity=0.75,size=100).encode(
        x=alt.X('Poll:N',title="Pollster"),
        y=alt.Y('Error:Q', title='Trump Polling Error (Predicted - Actual)'),
        color='Year:N',  # Color by election year
        fill='Year:N',
        size=alt.Size('Num Polls:Q', scale=alt.Scale(range=[50, 400]), legend=None),
        tooltip=['Poll:N', 'Year:N', 'Error:Q', 'Num Polls:Q']
    ).properties(
        width=1200,
        height=400,
        title='Error Comparison for Pollsters (2020 and 2024 Elections)'
    )

    return chart
results = get_data_results("election_results/election_results_presidential.csv")
errors = calculate_errors(results)
df = transform_errors_to_df(errors)
chart = plot_errors(df)
chart.save("chart.html")

print(errors)
df = pd.DataFrame()



#under = 0
#total_under = 0
#total = 0
# for i in list(errors[2024].keys()):
#     for j in list(errors[2024][i].keys()):
#         if errors[2024][i][j][0] < 0:
#             under+=1
#             total_under+=errors[2024][i][j][0]
#         total+=1
# print(errors)
# print("The total percentage of pollsters average polls that underestimated trump in 2024 is  "+str(under/total))
# print("The average amount of underestimating was "+str(total_under/total))

# ---------------------------------------------------------------------------------------------------




#chart_2024 = alt.Chart(flattened_data_2024).mark_point().encode(
#        x = 'Polls',
#        y = 'Residual'
#    ).interactive()
#chart_2024.save('chart_2024.html')

#chart_2020 = alt.Chart(flattened_data_2020).mark_point().encode(
#        x = 'Polls',
#        y = 'Residual'
#    ).interactive()
#chart_2020.save('chart_2020.html')