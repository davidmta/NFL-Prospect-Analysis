import requests
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
import re
import sqlite3 as lite
import sys

def store_url(soup,urls):
    for link in soup.find_all('a'):
        link_str = link.__str__()
        root = re.search('http://www.nfldraftscout.com/ratings/dsprofile.php\?pyid?\=\d+', link_str)
        draft_branch = re.search('draftyear\=\d+', link_str)
        pos_branch = re.search('genpos\=\w+', link_str)
        if root:
            url = root.group(0) + "&" + draft_branch.group(0) + "&" + pos_branch.group(0)
            print("Adding url: " + url)
            urls.append(url)
    return urls

def get_url(url_list):
    for year in range(0,1):
        urls = []
        for listing in range(65,90):
            page = requests.get("http://www.nfldraftscout.com/searchcollege.php?draftyear=" + str(1999 + year) + "&colabbr=" + chr(listing))
            soup = BeautifulSoup(page.content, 'html.parser')
            urls = store_url(soup,urls)
        url_list.append(urls)
    return url_list

def attempt_connection():
    try:
        con = lite.connect('user.db')
        return con
    except Error as e:
        print(e)

def create_table(cur):
    cur.execute("CREATE TABLE URL(URL_A TEXT, URL_B TEXT, URL_C TEXT,URL_D TEXT, URL_E TEXT, URL_F TEXT,URL_G TEXT, URL_H TEXT, URL_I TEXT,URL_J TEXT, URL_K TEXT, URL_L TEXT, URL_M TEXT, URL_N TEXT,URL_O TEXT, URL_P TEXT, URL_Q TEXT)")

def add_to_db():
    con = attempt_connection()
    with con:
        cur = con.cursor()
    create_table(cur)
    con.commit()
    con.close()

def main():
    url_list = []
    url_list = get_url(url_list)
    print(url_list)
    #add_to_db()
    return 0;

if __name__ == "__main__":
    main()
