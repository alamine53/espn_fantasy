import time
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.support import expected_conditions as EC # available since 2.26.0
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from pywebcopy import save_website
from pywebcopy import WebPage
import pywebcopy
from bs4 import BeautifulSoup
import pandas as pd
pywebcopy.config['bypass_robots'] = True
from datetime import datetime

def league_standings(league_id = 2098926112, save_folder = 'data', save_file = True):

	# set dataset name as today's date
	now = datetime.today().strftime('%Y-%m-%d')
	dataset_name = now + ".csv"
	url = 'https://fantasy.espn.com/basketball/league/standings?leagueId=%s' %league_id

	# open chrome browser
	driver = webdriver.Chrome()
	driver.get(url);
	time.sleep(5)

	# # accept cookies
	driver.implicitly_wait(10)
	driver.find_element_by_xpath("//button[contains(@id, 'accept-btn')]").click()

	## collect tables
	time.sleep(5)
	page = driver.page_source
	soup = BeautifulSoup(page, 'html.parser')
	tables = soup.find_all("table")

	# scrape data
	# standings table is actually 3 separate tables. 
	# table 3 contains rank and team names, and table 4 contains the data
	# I scrape each table separately then join together. 
	time.sleep(5)
	table = tables[4]
	tab_data = [[cell.text for cell in row.find_all(["th","td"])]
	                        for row in table.find_all("tr")][2:]

	headers = [[cell.text for cell in row.find_all(["th","td"])]
	                        for row in table.find_all("tr")][1]

	# scrape team names & ranks
	table = tables[3]
	tab_rownames = [[cell.text for cell in row.find_all(["th","td"])]
	                        for row in table.find_all("tr")][2:]

	# build dataframe
	df_data = pd.DataFrame(tab_data, columns = headers)
	df_names = pd.DataFrame(tab_rownames, columns = ['Rk', 'Team'])
	df = df_names.join(df_data)

	# add date column
	df['date'] = now

	# export to csv
	# print(df)
	if save_file == True:
		df.to_csv(os.path.join(save_folder, dataset_name), index = False)
		print("Dataset has been successfully exported to 'data' as ", dataset_name)

	return df 


if __name__ == '__main__':
	league_standings()
