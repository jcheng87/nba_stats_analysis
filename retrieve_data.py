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


class RetreieveData:
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