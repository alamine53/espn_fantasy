from src import scrape
from os import path
from datetime import datetime
import pandas as pd 
import os

# parameters
data_folder = 'data'
leagueID = 2098926112
today = datetime.today().strftime('%Y-%m-%d')

# scrape today's data if I haven't yet
if not path.exists(os.path.join(data_folder, today + ".csv")):
	df = league_standings(league_id = leagueID, save_file = True, save_folder = data_folder)
else:
	print("today's standings have already been scraped.")

# initiate empty dataframe
df = pd.DataFrame()

# load all data into one df
for file in os.listdir(data_folder):
	raw = pd.read_csv(os.path.join(data_folder, file))
	df = df.append(raw).sort_values(by = ['date', 'Rk'])

# replace team name by owner
df['Team'] = df['Team'].str.extract(r'.*\((.*)\).*')

# export to csv
df.to_csv('latest.csv', index = False)

# group df by team
# df = df.groupby(['Team', 'date'])
# df = df.loc[df.Team == "Ramzy Al Amine"]

# plot
# =====
print(df)
column = 'FG%'
df = df.loc[('date', 'Team', 'FG%')]

df_wide = df.pivot_table(index='date', columns= 'Team', values='column')

# unstack(level = 'Team')
print(df_wide)

import matplotlib.pyplot as plt
# plt.style.use('seaborn-whitegrid')
csfont = {'fontname':'Arial'}
hfont = {'fontname':'Helvetica'}
plt.rcParams["font.family"] = "Roboto"

# # grey lines
# for name, group in df.groupby('Team'):
#    plt.plot(df.date, df[column], marker='', color='grey', linewidth=1, alpha=0.4)

plt.plot(df.date, df['FG%'])
plt.title('FG%', loc = 'left', fontsize = 24, fontweight = 'bold', **hfont)
plt.show()




