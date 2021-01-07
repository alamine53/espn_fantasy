from os import path
from datetime import datetime
import pandas as pd 
import os
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

# this functions creates the dataset
def league_standings(data_folder = '../data', output_folder = '../'):

	# initiate empty dataframe
	df = pd.DataFrame()
	
	# today's date
	today = datetime.today().strftime('%Y-%m-%d')

	# load historical data into one df
	for file in os.listdir(data_folder):
		raw = pd.read_csv(os.path.join(data_folder, file))
		df = df.append(raw).sort_values(by = ['date', 'Rk'])

	# replace team name by first name of owner
	df['Team'] = df['Team'].str.extract(r'.*\((.*)\).*') # extract content of parenthesis
	df['Team'] = df.Team.str.split().str.get(0) # get first name
	df['Team'] = df.Team.str.capitalize()

	# tidy
	df.sort_values(['Team', 'date'], inplace = True)
	df.set_index(['Team', 'date'], inplace = True)

	# export 
	df.to_csv(os.path.join(output_folder, 'latest.csv'), index = True)

	return df


def create_subplot(file_name, data_folder = "../data", owner_name = "Ramzy", output_folder = '../static'):
	
	df = league_standings(data_folder = data_folder)
	if file_name == 'standings_per_game.png':

		# convert stats to per game
		categories = ['3PM', 'AST', 'REB', 'PTS', 'TO', 'STL', 'BLK']

		for cat in categories:
			df[cat] = df[cat] / df['GP']

	# for chart, i need to reset index
	df.reset_index(inplace = True)
	df.info()

	# format date
	df['date'] = df['date'].astype('datetime64[ns]')

	# group data set by team 
	grp = df.groupby('Team') 
	for name, group in grp:
		print(name)

	# define categories to loop over
	categories = ['FG%', 'FT%', '3PM', 'AST', 'REB', 'PTS', 'TO', 'STL', 'BLK']

	# ========= BEGIN PLOTTING ========= #

	plt.rcParams["font.family"] = "monospace"
	plt.rc('xtick', labelsize=8) 
	plt.rc('ytick', labelsize=8) 
	# set figure size
	plt.figure(figsize = (12,8), dpi = 150)


	# loop over categories to create subplots
	for i, category in enumerate(categories, 1):

		# i indicates the particular subplot instance
		plt.subplot(3, 3, i) 

		# grey lines
		for name, group in grp:   
			
			# set dates in MM/DD format
			ax = plt.gca()
			formatter = mdates.DateFormatter("%m/%d")
			ax.xaxis.set_major_formatter(formatter)

			# set x-axis so that it always shows 6 evenly-distributed ticks
			ax.xaxis.set_major_locator(plt.MaxNLocator(6))

			# plot
			plt.plot(group.date, group[category], marker='', color='grey', 
				linewidth=1, linestyle = '--', alpha=0.4, label = name)
		    # plt.text(name, horizontalalignment='left', size='small', color='grey')

		# main line 
		df = df.loc[df.Team == owner_name]
		plt.plot(df.date, df[category], marker= 'o', color='blue', linewidth= 2)
		
		# annotate
		# for x,y in zip(df.date,df[category]):
		#     label = "{:.1f}".format(y)
		#     plt.annotate(label, # this is the text
		#                  (x,y), # this is the point to label
		#                  textcoords="offset points", # how to position the text
		#                  xytext=(0,10), # distance from text to points (x,y)
		#                  ha='center') # horizontal alignment can be left, right or center

		# add title
		plt.title(category, loc = 'center', fontsize = 12, fontweight = 'bold')

	# increase space between subplots
	if file_name == 'standings_per_game.png':
		plt.suptitle(owner_name + "'s Team Stats Per Game", fontsize = 24, x = .25, y = .95, fontweight = 'bold')
	else:
		plt.suptitle(owner_name + "'s Team Totals", fontsize = 24, x = .25, y = .95, fontweight = 'bold')

	plt.tight_layout(pad=2.0)
	# plt.title("Ya 3ayni Standings", loc = 'left', fontsize = 24, fontweight = 'bold')
	plt.savefig(os.path.join(output_folder, file_name), dpi = 600)

##
# plt.clear()
# fig, ax = plt.subplots(df, sharex = True)

# def stats_per_game(df, owner_name = "Ramzy"):
	
# 	# convert stats to per game
# 	categories = ['3PM', 'AST', 'REB', 'PTS', 'TO', 'STL', 'BLK']

# 	for cat in categories:
# 		df[cat] = df[cat] / df['GP']

# 	# show per game stats table
# 	print(df)
# 	return df
	# df_norm =(df-df.min())/(df.max()-df.min())
	# df_norm.reset_index('date', inplace = True)

	# # df_normalized = df_normalized.loc[df_normalized.Team == "Ramzy"]
	# categories = ['FG%', 'FT%', '3PM', 'AST', 'REB', 'PTS', 'TO', 'STL', 'BLK']

	# # keep relevant categories
	# df_norm = df_norm[categories]
	# df = df_norm.transpose()

	# # plot
	# plt.rcParams["font.family"] = "monospace"
	# plt.rc('xtick', labelsize=8) 
	# plt.rc('ytick', labelsize=8) 
	# # set figure size
	# fig, ax = plt.subplots(figsize=(12, 6), tight_layout=True)
	# for owner in owners:
	# 	df[owner].plot(kind="bar", ax=ax, color ='none', edgecolor = 'black', width = 0.5, label = owner)

	# # for name in df_normalized.Team:
	# # plt.bar(df_normalized, height = color='#b5ffb9', edgecolor='white', width=barWidth)
	# # df.plot.bar(color ='grey', edgecolor = 'black')
	# ax.axes.yaxis.set_visible(False)
	# plt.show()

if __name__ == "__main__":
	
	create_subplot(file_name = 'standings.png')
	create_subplot(file_name = 'standings_per_game.png')
	# stats_per_game()
