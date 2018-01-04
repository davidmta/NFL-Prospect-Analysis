import requests
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
import re
import sys
import csv
import sqlite3 as lite
import os

FILE_NAME = 'sr_players_database.db'

def get_raw_logsplits(stats_type,player_url):
    url = re.sub('.html','/' + stats_type + '/',player_url)
    page = requests.get("https://www.sports-reference.com" + url)
    if page.status_code == 404:
        return
    soup = BeautifulSoup(page.content,"html.parser")
    return soup.findAll('table')

def attempt_connection():
    try:
        con = lite.connect(FILE_NAME)
        return con
    except Error as e:
        print(e)

def main():
    con = attempt_connection()
    with con:
        cur = con.cursor()
    return 0;

if __name__ == "__main__":
    main()
