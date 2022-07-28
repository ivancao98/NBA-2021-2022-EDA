import pandas as pd
from matplotlib import pyplot as plt
import seaborn as sns
import numpy as np
import random

df = pd.read_csv(r"C:\Users\Ivan Cao\Downloads\ASA All NBA Raw Data.csv")
df['Win'] =  df['Team_Score'] > df['Opponent_Score']
df['team_plus_minus'] = df['Team_Score'] - df['Opponent_Score']

gamestats = df[['game_date', 'H_A', 'Team_Abbrev', 'Team_Score',
       'Opponent_Abbrev', 'Opponent_Score', 'Win', 'team_plus_minus']].drop_duplicates().sort_values(by = ['Team_Abbrev', 'game_date']).reset_index()

playerstats = df[['game_date', 'Team_Abbrev', 'H_A', 'fg', 'fga',
       'fg_pct', 'fg3', 'fg3a', 'fg3_pct', 'ft', 'fta', 'ft_pct', 'orb', 'drb',
       'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts']].drop_duplicates().groupby(['Team_Abbrev', 'game_date']).sum().reset_index()


seasongamestats = pd.merge(gamestats, playerstats)
seasongamestats = seasongamestats.iloc[: , 1:]


# this function corrects percentage errors when taking sum of all rows
def correct_percent(df, success, attempted, corrected_pct):
    for i,j,k in zip(success, attempted, corrected_pct):
        df[k] = (df[i]/df[j]) * 100
    
    return df

def season_stats(game_stats):
    # will be analyzing home games vs away games
    # a full NBA season is 82 games, half are scheduled away (41 games) and half are scheduled home (41 games). Dividing the rows by 41 will give us averages
    # on home vs away games.
    home_away_totals =  game_stats.groupby(['Team_Abbrev', 'H_A']).sum().div(41).reset_index()
    
    # wins does not need to be divided and percentages need to be corrected
    home_away_totals['Win'] = home_away_totals['Win'].apply(lambda x: x*41)
    home_away_totals = correct_percent(home_away_totals, ['fg', 'fg3', 'ft'], ['fga', 'fg3a', 'fta'], ['fg_pct', 'fg3_pct', 'ft_pct'])
    
    home_away_totals['Conference'] = home_away_totals['Team_Abbrev'].isin(['ATL', 'IND', 'BRK', 'CHO', 'MIL', 'CLE', 'BOS', 'CHI','TOR', 'NYK', 'MIA','DET', 'PHI', 'ORL', 'WAS'])
    home_away_totals['Conference'] = home_away_totals['Conference'].map({True:'Eastern' ,False:'Western'})
    
    pergameaverages = home_away_totals.groupby(['Team_Abbrev', 'Conference']).mean().reset_index()
    pergameaverages['Win'] = pergameaverages['Win'].apply(lambda x: x*2)
    
    stats_at_home = home_away_totals.loc[home_away_totals['H_A'] == 'H']
    stats_at_away = home_away_totals.loc[home_away_totals['H_A'] == 'A']
    
    
    return home_away_totals, stats_at_home, stats_at_away, pergameaverages

seasonbreakdown = season_stats(seasongamestats)
seasontotals = seasonbreakdown[0]
stats_at_home = seasonbreakdown[1]
stats_at_away = seasonbreakdown[2]
pergameaverages = seasonbreakdown[3]
    

# Historically in the NBA, along with other sports, home teams on average win a larger percentage of the games compared to away teams. We can check this with home 
# and away totals by plotting it
HA_wins = seasontotals[['Team_Abbrev', 'H_A', 'Win']]
sns.catplot(data = HA_wins, kind = 'bar', x = 'Team_Abbrev', y = 'Win', hue = 'H_A')
plt.xlabel('Teams')
plt.ylabel('Total Wins')
plt.title('Teams Wins at Home vs Away Games')

# Out of the 30 teams, 22 teams (~73%) have more wins at home games than away games.



# To set up playoffs, there are 2 conferences: East and West
# Each teams plays their respected conferences and the winner of each conference plays each other in the NBA Finals
# The top 8 teams with the most wins of each conference will make the playoffs
# There are four rounds to the playoffs with teams playing a best of 7 series (first to 4 wins)
# The first round of the playoffs are as follows:
# The #1 ranked team plays the #8th ranked team, #2 ranked team plays the #7 ranked team, 
# #3 ranked team plays the 6th ranked team, and the 4th ranked team plays the 5th ranked team
# I have provided a diagram that outlines the bracket


# Before setting up the format, I am going to pull the top 8 teams from each conference
WesternConference = pergameaverages.loc[pergameaverages['Conference'] == 'Western'].nlargest(8, 'Win')
EasternConference = pergameaverages.loc[pergameaverages['Conference'] == 'Eastern'].nlargest(8, 'Win')

# Going to reorder the columns before setting playoff standings
def reorderfirstcolumn(df, column):
    store = df.pop(column)
    df.insert(0, 'Win', store)
    return df

WesternConference = reorderfirstcolumn(WesternConference, 'Win')
EasternConference = reorderfirstcolumn(EasternConference, 'Win')


def playoff_matchups(conference):
    playoffs_df = []
    for i in range(len(conference)//2):
        playoffs_df.append(pd.concat([conference.iloc[i], conference.iloc[len(conference)-1-i]], axis = 1).T)
    
    return playoffs_df

Western_seeding = playoff_matchups(WesternConference)
Eastern_seeding = playoff_matchups(EasternConference)


