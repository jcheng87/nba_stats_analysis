#Import Essential Libraries
import streamlit as st 
import pandas as pd
import numpy as np

# Plot Package
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Import parameters packages
from nba_api.stats.library.parameters import Season
from nba_api.stats.library.parameters import SeasonTypeAllStar
from nba_api.stats.library.parameters import SeasonType

# Import Team list
from nba_api.stats.static import teams
nba_teams = teams.get_teams()
nba_teams_dict =  { team['full_name'] : team for team in nba_teams }

# Team Selection
nba_select = st.selectbox("NBA Teams:", ([team['full_name'] for team in nba_teams]))


# Display Team Info
team_result_df = pd.DataFrame.from_dict(nba_teams_dict, orient='index').loc[[nba_select]]
st.dataframe(team_result_df)


# Display TeamGameLog
from nba_api.stats.endpoints import teamgamelog
teamgamelog_params = {'season':Season.default,
                     'season_type_all_star':SeasonTypeAllStar.default,
                     'team_id':team_result_df.id}

team_gamelog_df = teamgamelog.TeamGameLog(**teamgamelog_params).get_data_frames()[0]
team_gamelog_df['GAME_DATE'] = pd.to_datetime(team_gamelog_df['GAME_DATE']).dt.date
st.write(team_gamelog_df)

# Plot Game Data

# User chooses Y-Axis value
team_column_select_y = st.selectbox('On Y-Axis:', team_gamelog_df.columns, key='team_column_select_y')
team_column_select_x = st.selectbox('On X-Axis:', team_gamelog_df.columns, key='team_column_select_x')


col1, col2 = st.beta_columns(2)

fig = px.line(team_gamelog_df, x='GAME_DATE', y=team_column_select_y)
col1.write(fig)

fig = px.density_contour(team_gamelog_df, x=team_column_select_x, y=team_column_select_y, color='WL', marginal_x='histogram',  marginal_y='histogram')
col2.write(fig)




# PlayerGameLogs
from nba_api.stats.endpoints import playergamelogs

playergamelogs_params =      {'season_nullable':Season.default,
                             'season_type_nullable':SeasonTypeAllStar.default,
                             'team_id_nullable':team_result_df.id}

playergamelogs2_result = playergamelogs.PlayerGameLogs(**playergamelogs_params).get_data_frames()[0]
playergamelogs2_result['GAME_DATE'] = pd.to_datetime(playergamelogs2_result['GAME_DATE']).dt.date

# Display Roster
player_select = st.multiselect("Players", pd.unique(playergamelogs2_result['PLAYER_NAME']))

# Diplay Players Game Log
player_gamelog_res = playergamelogs2_result[playergamelogs2_result['PLAYER_NAME'].isin(player_select)]
st.write(player_gamelog_res)

# Graph Pts over time 
# User chooses Y-Axis value
column_select = st.selectbox('On Y-Axis:', player_gamelog_res.columns)

col1, col2 = st.beta_columns(2)

# Plot Graph for players game log
fig = px.line(player_gamelog_res, x='GAME_DATE', y=column_select, color='PLAYER_NAME')
col1.write(fig)


# Plot points score relative to minutes played
fig = px.scatter(player_gamelog_res, x='MIN', y=column_select, color='PLAYER_NAME', marginal_x='histogram',  marginal_y='histogram')
col2.write(fig)






