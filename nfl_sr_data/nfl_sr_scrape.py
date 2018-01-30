import requests
import sys
import re
import sqlite3 as lite
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
from scrape_tools import strip_position,standardize_for_SQL

def get_identification(p_str):
	url_result = re.search('/players/\w+/\w+\.htm',p_str)
	name_result = re.search('\.htm\"\>.*?\s.*?\<\/a\>',p_str)
	position_result = re.search('\(.*?\)',p_str)
	years_result = re.search('\d+\-\d+',p_str)
	if url_result and name_result and position_result and years_result != None:
		player_url = url_result.group(0)
		name = standardize_for_SQL(name_result.group(0))
		position = strip_position(position_result.group(0))
		years = years_result.group(0)
	
def get_players_stats(page,cur):
	soup = BeautifulSoup(page.content,"html.parser")
	p_soup = soup.findAll('p')
	for p in p_soup:
		print p
		get_identification(str(p))

def get_data(cur):
	# for letter in range(ord('A'),ord('Z')+1):
	page = requests.get("https://www.pro-football-reference.com/players/A")
	get_players_stats(page,cur)

def attempt_connection():
    con = lite.connect('sr_nfl_players_database.db')
    return con

def main():
	con = attempt_connection()
	with con:
		cur = con.cursor()
		get_data(cur)

if __name__ == "__main__":
    main()