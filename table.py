import pandas as pd
from helper2 import get_data_results, transform_errors_to_df, calculate_errors

# Assuming you have results and errors calculated
results = get_data_results("election_results/election_results_presidential.csv")
errors = calculate_errors(results)

state_data = {}

for j in [2020, 2024]:
    for i in list(errors[j].keys()):
        error = abs(errors[j][i][0])
        amount = errors[j][i][1]
        if i not in state_data:
            state_data[i] = {"Error": 0, "Amount": 0,"Score":0}
        state_data[i]["Error"] += abs(error)
        state_data[i]["Amount"] += amount
    s_max = max([state_data[x]["Amount"] for x in list(state_data.keys())])
    for i in list(state_data.keys()):
        state_data[i]["Score"] = ((1/state_data[i]["Error"]))*0.75 + (state_data[i]["Amount"]/s_max)*0.25
        # score formula is calculated using 75% error and 25% sample size.
        # Full formula is (1/ER)+(S/max(S_N))
        # 1 divided by the error rate squares times 0.75 plus the sample size divided by the max sample size


df = pd.DataFrame.from_dict(state_data, orient='index').reset_index()
df.columns = ["Polling Company", "Aggregated Error", "Aggregated Amount","Score"]
df_sorted = df.sort_values(by="Score", ascending=False)

html_table = df_sorted.to_html(index=False)
