import requests
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
import re
import sqlite3 as lite
import sys
from profile_scrape import parse_profiles

def store_data(soup,cur):
    for link in soup.find_all('a'):
        link_str = link.__str__()
        root = re.search('http://www.nfldraftscout.com/ratings/dsprofile.php\?pyid?\=\d+', link_str)
        draft_branch = re.search('draftyear\=\d+', link_str)
        pos_branch = re.search('genpos\=\w+', link_str)
        if root and draft_branch and pos_branch:
            url = root.group(0) + "&" + draft_branch.group(0) + "&" + pos_branch.group(0)
            profile_entry = parse_profiles(url)
            profile_entry = token_fix(profile_entry)
            cur.execute("INSERT INTO URL VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (url,profile_entry[0],profile_entry[1],profile_entry[2],profile_entry[3],profile_entry[4],profile_entry[5],profile_entry[6],profile_entry[7],profile_entry[8],profile_entry[9],profile_entry[10],profile_entry[11],profile_entry[12],profile_entry[13],profile_entry[14],profile_entry[15],profile_entry[16],profile_entry[17],profile_entry[18],profile_entry[19],profile_entry[20],profile_entry[21],profile_entry[22],profile_entry[23],profile_entry[24]))

def token_fix(profile_entry):
    if profile_entry[11] != "NULL":
        profile_entry[11] = re.sub('[\'\"]', ' ', profile_entry[11])
    return profile_entry

def get_data(cur):
    ##22
    for year in range(0,1):
        urls = []
        #90
        for listing in range(65,66):
            page = requests.get("http://www.nfldraftscout.com/searchcollege.php?draftyear=" + str(1999 + year) + "&colabbr=" + chr(listing))
            soup = BeautifulSoup(page.content, 'html.parser')
            store_data(soup,cur)

def attempt_connection():
    try:
        con = lite.connect('user.db')
        return con
    except Error as e:
        print(e)

def create_table(cur):
    cur.execute("CREATE TABLE URL(URL TEXT,NAME TEXT,POSITION TEXT,COLLEGE TEXT,CB_INVITE TEXT,CB_HEIGHT TEXT,CB_WEIGHT TEXT,CB_FORTY TEXT,CB_TWENTY TEXT,CB_TEN TEXT,CB_REPS TEXT,CB_VERT TEXT,CB_BROAD TEXT,CB_SHUTTLE TEXT,CB_DRILL TEXT, PRO_INVITE TEXT, PRO_HEIGHT TEXT,PRO_WEIGHT TEXT,PRO_FORTY TEXT,PRO_TWENTY TEXT,PRO_TEN TEXT,PRO_REPS TEXT,PRO_VERT TEXT,PRO_BROAD TEXT,PRO_SHUTTLE TEXT,PRO_DRILL TEXT)")

def main():
    url_list = []
    con = attempt_connection()
    with con:
        cur = con.cursor()
    create_table(cur)
    get_data(cur)
    con.commit()
    con.close()
    return 0;

if __name__ == "__main__":
    main()
