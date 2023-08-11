import pandas as pd
import plotly.express as px

def update_elo(home_elo, away_elo, home_score, away_score):
    K = 30
    expected_home = 1 / (1 + 10 ** ((away_elo - home_elo) / 400))
    expected_away = 1 - expected_home
    if home_score > away_score:
        actual_home = 1
        actual_away = 0
    elif home_score < away_score:
        actual_home = 0
        actual_away = 1
    else:
        actual_home = 0.5
        actual_away = 0.5
    return home_elo + K * (actual_home - expected_home), away_elo + K * (actual_away - expected_away)

data = pd.read_csv('results.csv')
INITIAL_ELO = 1500
elo_ratings = {team: INITIAL_ELO for team in pd.concat([data['home_team'], data['away_team']]).unique()}
elo_history = {team: [] for team in elo_ratings.keys()}
dates_history = []

for idx, row in data.iterrows():
    home_team, away_team, home_score, away_score = row['home_team'], row['away_team'], row['home_score'], row['away_score']
    date, home_elo, away_elo = row['date'], elo_ratings[home_team], elo_ratings[away_team]
    new_home_elo, new_away_elo = update_elo(home_elo, away_elo, home_score, away_score)
    elo_ratings[home_team], elo_ratings[away_team] = new_home_elo, new_away_elo
    for team, rating in elo_ratings.items():
        elo_history[team].append(rating)
    dates_history.append(date)

top_10_teams = sorted(elo_ratings, key=elo_ratings.get, reverse=True)[:10]
plot_data = []
for team in top_10_teams:
    ratings = elo_history[team]
    plot_data.extend([{'Date': dates_history[i], 'Elo Rating': rating, 'Team': team} for i, rating in enumerate(ratings)])
plot_df = pd.DataFrame(plot_data)
plot_df['Date'] = pd.to_datetime(plot_df['Date'])
fig = px.line(plot_df, x='Date', y='Elo Rating', color='Team', hover_data=['Elo Rating'])
fig.show()
