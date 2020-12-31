from os import path
from datetime import datetime
import pandas as pd 
import os
import matplotlib.pyplot as plt


def create_subplot(owner_name = "Ramzy"):
	# parameters
	data_folder = '../data'
	output_folder = '../static'

	today = datetime.today().strftime('%Y-%m-%d')

	# initiate empty dataframe
	df = pd.DataFrame()

	# load all data into one df
	for file in os.listdir(data_folder):
		raw = pd.read_csv(os.path.join(data_folder, file))
		df = df.append(raw).sort_values(by = ['date', 'Rk'])

	# replace team name by first name of owner
	df['Team'] = df['Team'].str.extract(r'.*\((.*)\).*') # extract content of parenthesis
	df['Team'] = df.Team.str.split().str.get(0) # get first name
	df['Team'] = df.Team.str.capitalize()

	# set inex
	df.sort_values(['Team', 'date'], inplace = True)
	df.set_index(['Team', 'date'], inplace = True)

	# export to csv
	df.to_csv('latest.csv', index = True)

	# for chart, i need to reset index
	df.reset_index(inplace = True)
	
	# format date
	# df['date'] = df['date'].datetime.strftime('%m/%d')

	# group data set by team
	grp = df.groupby('Team') 
	for name, group in grp:
		print(name)

	# define categories to loop over
	categories = ['FG%', 'FT%', '3PM', 'AST', 'REB', 'PTS', 'TO', 'STL', 'BLK']

	# ========= BEGIN PLOTTING ========= #

	# set font and themes
	# plt.style.use('seaborn-whitegrid')
	# csfont = {'fontname':'Arial'}
	# hfont = {'fontname':'Helvetica'}
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
	plt.tight_layout(pad=2.0)
	# plt.title("Ya 3ayni Standings", loc = 'left', fontsize = 24, fontweight = 'bold')
	plt.savefig(os.path.join(output_folder, 'standings.png'), dpi = 600)

##
# plt.clear()
# fig, ax = plt.subplots(df, sharex = True)


if __name__ == "__main__":
	create_subplot()
