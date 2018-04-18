import requests
import sys
import re
import sqlite3 as lite
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
from scrape_support import strip_position,standardize_for_SQL,strip_brackets,strip_quotes,strip_birthplace,parse_defense,parse_passing

def gather_stats(player_url):
	page = requests.get(player_url)
	p_soup = BeautifulSoup(page.content,"html.parser")
	for p in p_soup:
		p_str = str(p)        
		college_result = re.search('\<a href\=\"\/schools\/.*?\/\"\>.*?\<\/a\>',p_str)
		height_result = re.search('\"height\"\>.*?\<\/',p_str)
		weight_result = re.search('\"weight\"\>.*?\<\/',p_str)
		birthday_result = re.search('data\-birth\=\"\d+\-\d+\-\d+\"',p_str)
		birthplace_result = re.search('.*?\<a href\=\"\/friv\/birthplaces\.cgi\?country\=.*?\"',p_str)
		high_school_result = re.search('hs\_state\=.*?\"\>',p_str)
		if college_result and height_result and height_result and birthday_result and high_school_result and birthplace_result!= None:
			college = strip_brackets(college_result.group(0))
			height = strip_brackets(height_result.group(0))
			weight = strip_brackets(weight_result.group(0))
			birthday = strip_quotes(birthday_result.group(0))
			birthplace = strip_birthplace(birthplace_result.group(0))
			hs_state = high_school_result.group(0)[:-2]
			hs_state = hs_state.split("=")[1]
		trs = re.findall('\<tr\s\>.*?\<\/tr\>',page.content)
		
		#matching = [s for s in trs if "pass_cmp" in s]
		for tr in trs:
			print tr
			print re.search('pass_cmp',tr) is not None
		# # 	if re.search('Defense &amp; Fumbles',tr) != None:
		# # 		defense_stats = parse_defense(tr)
	 #        if re.search('pass_cmp',tr) is not None:
	 #        	print "here"
	        	#pass_stats = parse_passing(tr)
        # elif re.search('rush_att',p_soup) != None:
        #     rr_stats = rushing_receiving(p_soup,rr_stats)
        # elif re.search('td_def_int',p_soup) != None:
        #     scoring_stats = scoring(p_soup,scoring_stats)
        # elif re.search('punt_yds_per_punt',p_soup) != None:
        #     pk_stats = punting_and_kicking(p_soup,pk_stats)
        # elif re.search('kick_ret_yds_per_ret',p_soup) != None:
        #     pkreturn_stats = punt_kick_returns(tr,pkreturn_stats)
			
	sys.exit(1)

def get_identification(p_str):
	url_result = re.search('/players/\w+/\w+\.htm',p_str)
	name_result = re.search('\.htm\"\>.*?\s.*?\<\/a\>',p_str)
	position_result = re.search('\(.*?\)',p_str)
	years_result = re.search('\d+\-\d+',p_str)
	return url_result,name_result,position_result, years_result

def get_players_stats(page,cur):
	soup = BeautifulSoup(page.content,"html.parser")
	p_soup = soup.findAll('p')
	for p in p_soup:
		url_result,name_result,position_result, years_result = get_identification(str(p))
		if url_result and name_result and position_result and years_result != None:
			player_url = url_result.group(0)
			name = standardize_for_SQL(name_result.group(0))
			position = strip_position(position_result.group(0))
			years = years_result.group(0)
			#gather_stats('https://www.pro-football-reference.com' + player_url)
			gather_stats('https://www.pro-football-reference.com/players/L/LuckAn00.htm')

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