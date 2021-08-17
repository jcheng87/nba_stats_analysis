#Import Essential Libraries
import streamlit as st 
import pandas as pd
import numpy as np

# Plot Package
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# nba_function
from nba_functions import *
from retrieve_data import *

@st.cache
def load_data():
    gamelog_2020_21_fn= '2020-2021_gamelog.csv'
    gamelog_2020_21_raw = pd.read_csv(gamelog_2020_21_fn)
    seasongamelog = SeasonGameLog()
    gamelog_2020_21 = seasongamelog.vs_gamelog(gamelog_2020_21_raw)

    return gamelog_2020_21[gamelog_2020_21['WL']=='W']


winners = load_data()

cols = ['FGM', 'FGA', 'FG_PCT', 'FG3M', 'FG3A', 'FG3_PCT', 'FTM', 'FTA',
       'FT_PCT', 'OREB', 'DREB', 'REB', 'AST', 'STL', 'BLK', 'TOV', 'PF', 'PTS']

diff_cols = [col+'_diff' for col in cols]

for col in diff_cols: 
    fig = px.scatter(winners, x=col, y='PTS_diff', title=col)
    st.write(fig)
