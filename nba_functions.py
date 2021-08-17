#Import Essential Libraries
import streamlit as st 
import pandas as pd
import numpy as np

import time

# Import Team list
from nba_api.stats.static import teams

# Import parameters packages
from nba_api.stats.library.parameters import Season
from nba_api.stats.library.parameters import SeasonTypeAllStar
from nba_api.stats.library.parameters import SeasonType

# Import Stats Endpoints
from nba_api.stats.endpoints import teamgamelog
from nba_api.stats.endpoints import teamgamelogs
from nba_api.stats.endpoints import playergamelogs



class Team:
    def __init__(self):
        self.list = Team.dataframe()

    def dataframe():
        """
        Returns Dataframe of Team List
        """
        teams_list = teams.get_teams()
        teams_list_header =  teams_list[0].keys()

        return pd.DataFrame(teams_list, columns=teams_list_header)

         
    def search_teaminfo(self, team_abbr):
        """
        Return Team list row based on team_abbr argument
        """

        return self.list.loc[self.list['abbreviation']==team_abbr]

class StatCalls:

    def retrieveGameLog(team_ids, season, season_type):
        """
        returns season's gamelog for team
        
        Parameters:
        -------------
        team_ids (list of ints), 
        season (str)
        season_type: (str)


        Returns:
        ---------
        DataFrame

        """

        season_gamelog = []

        for idx, team_id in enumerate(team_ids):
            
            if idx == 15:
                time.sleep(10)

            result = teamgamelog.TeamGameLog(team_id=team_id, season=season, season_type_all_star=season_type).get_data_frames()[0]

            season_gamelog.append(result)

            print(f"{idx}: {team_id} retrieved")
        
        return pd.concat(season_gamelog, ignore_index=True)




class SeasonGameLog:

    def clean_data(self, gamelog):
        # convert 'GAME_DATE' to datetime
        team_list = Team()

        gamelog['GAME_DATE'] = pd.to_datetime(gamelog['GAME_DATE'])

        gamelog['TEAM'] = gamelog['MATCHUP'].str[:3]
        gamelog['OPP'] = gamelog['MATCHUP'].str[-3:]
        gamelog['Team_ID_OPP'] = gamelog['OPP'].map(lambda x: team_list.search_teaminfo(x).iloc[0]['id'])



        return gamelog


    def merge_gamelog(self, gamelog):

        opponents_columns = ['Team_ID','Game_ID','FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA',
       'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF',
       'PTS']
        opp_gamelog = gamelog[opponents_columns].rename(columns={'Team_ID':'Team_ID_OPP'})

        return gamelog.merge(opp_gamelog, left_on=['Game_ID', 'Team_ID_OPP'], right_on=['Game_ID', 'Team_ID_OPP'], how='left', suffixes=('','_OPP'))
    
    def add_stat_diff(self, gamelog):
        # calculates difference between team and opps stats

        diff_columns = ['FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA',
       'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF']
        
        for col in diff_columns:
            gamelog[col + "_diff"] = gamelog[col] - gamelog[col+"_OPP"]
        
        return gamelog


    def vs_gamelog(self, gamelog):
        gamelog = self.clean_data(gamelog)
        gamelog = self.merge_gamelog(gamelog)
        gamelog = self.add_stat_diff(gamelog)

        return gamelog

    


    




