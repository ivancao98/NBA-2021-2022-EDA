import nltk
import pandas as pd

df = pd.read_csv(r"C:\Users\Ivan Cao\Downloads\ASA All NBA Raw Data.csv")
df['Win'] =  df['Team_Score'] > df['Opponent_Score']
df['Conference'] = df['Team_Abbrev'].isin(['ATL', 'IND', 'BRK', 'CHO', 'MIL', 'CLE', 'BOS', 'CHI','TOR', 'NYK', 'MIA','DET', 'PHI', 'ORL', 'WAS'])
df['Conference'] = df['Conference'].map({True:'Eastern' ,False:'Western'})


df.loc[df['Team_Abbrev'].isin(['ATL', 'IND', 'BRK', 'CHO', 'MIL', 'CLE', 'BOS', 'CHI','TOR', 'NYK', 'MIA','DET', 'PHI', 'ORL', 'WAS'])]

playerstats = df.groupby(['player']).sum()
playerstats = playerstats[['starter', 'fg', 'fga',
       'fg_pct', 'fg3', 'fg3a', 'fg3_pct', 'ft', 'fta', 'ft_pct', 'orb', 'drb',
       'trb', 'ast', 'stl', 'blk', 'tov', 'pf', 'pts', 'plus_minus','Win', 'Conference']]



def pct(df, success, attempted, correct):
    for i,j,k in zip(success, attempted, correct):
        df[k] = (df[i]/df[j]) * 100
    
    return df
        
playerstats = pct(playerstats, ['fg', 'fg3', 'ft'], ['fga', 'fg3a', 'fta'], ['fg_pct', 'fg3_pct', 'ft_pct'])
playerstats.fillna(0, inplace = True)


teamtotals = df.drop(['game_id', 'Inactives', 'player', 'player_id', 'starter', 'DKP', 'FDP',
       'SDP', 'DKP_per_minute', 'FDP_per_minute', 'SDP_per_minute',
       'pf_per_minute', 'ts', 'last_60_minutes_per_game_starting',
       'last_60_minutes_per_game_bench', 'PG%', 'SG%', 'SF%', 'PF%', 'C%',
       'active_position_minutes', 'mp', 'fg3_pct', 'ft_pct', 'minutes', 'season', 'bpm', 'did_not_play', 'is_inactive', 'plus_minus'], axis = 1)

teamtotals1 = teamtotals[['game_date', 'OT', 'H_A', 'Team_Abbrev', 'Team_Score', 'Team_pace',
       'Team_efg_pct', 'Team_tov_pct', 'Team_orb_pct', 'Team_ft_rate',
       'Team_off_rtg', 'Opponent_Abbrev', 'Opponent_Score', 'Opponent_pace',
       'Opponent_efg_pct', 'Opponent_tov_pct', 'Opponent_orb_pct',
       'Opponent_ft_rate', 'Opponent_off_rtg', 'Win', 'Conference']].drop_duplicates()

teamtotals1A = teamtotals1.sort_values(by = ['Team_Abbrev', 'game_date'])








teamtotals1Average = teamtotals1A.groupby(['Team_Abbrev', 'Conference']).mean()



teamtotals1WINSORT = teamtotals1Average.sort_values(by = 'Win', ascending = False)
teamtotals1playoffsranking = teamtotals1WINSORT.groupby('Conference').head(8)




teamtotals = df.groupby(['Team_Abbrev']).sum()
teamtotals = pct(teamtotals, ['fg', 'fg3', 'ft'], ['fga', 'fg3a', 'fta'], ['fg_pct', 'fg3_pct', 'ft_pct'])
teamtotals.fillna(0, inplace = True)




gamedays = df.groupby(['game_date', 'Team_Abbrev', 'Team_Score']).sum()





