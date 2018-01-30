import requests
import sys
import sqlite3 as lite

def get_players_stats(page,cur):
	soup = BeautifulSoup(page.content,"html.parser")
	p_soup = soup.findAll('p')
	
def get_data(cur):
	for letter in range(ord('A'),ord('Z')+1):
		page = requests.get("https://www.pro-football-reference.com/players/" + chr(letter))
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