# -*- coding: utf-8 -*-
import re
import sys
import sqlite3 as lite
import requests
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
from scrape_support import strip_rawpos, strip_rawline, edge_case, token_fix, profile_entry_fix, fix_name

def parse_profiles(url):
    try:
        page = requests.get(url)
        soup = BeautifulSoup(page.content, 'html.parser')
        personal_info = soup.find_all('b')
        stats_info = soup.find_all('font')
        profile_entry = []
        profile_entry = parse_personal(personal_info,profile_entry,url)
        for i in range(1,len(soup.find_all('font'))):
            profile_entry = store_profile(profile_entry,personal_info,stats_info,i)
        return profile_entry
    except:
        return url

def store_profile(profile_entry,personal_info,stats_info,i):
    link_str = stats_info[i].__str__()
    stat_name = re.search('<font color="#000000" face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><strong>', link_str)
    if stat_name:
        entry_str = stats_info[i+1].__str__()
        entry = re.search('>[\d.\\/ \”\’\'\"Yes]+</font',entry_str)
        if entry:
            entry_len = len(entry.group(0))
            entry = entry.group(0)[1:entry_len-6]
            profile_entry.append(entry)
        elif entry_str == '<font color="#000000" face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"></font>':
            profile_entry.append("NULL")
    profile_entry = determine_combine_participation(link_str,stats_info,profile_entry,i)
    return profile_entry

def determine_combine_participation(link_str,stats_info,profile_entry,i):
    if link_str == '<font color="#BA303E" face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><strong></strong></font>' and stats_info[i-1].__str__() == '<font color="#000000" face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><strong>Combine Invite:</strong></font>':
        profile_entry.append("No")
    elif link_str == '<font color="#BA303E" face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><strong>Yes</strong></font>':
        profile_entry.append("Yes")
    if link_str == '<font color="#000000" face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><strong>Dates:</strong></font>':
        if stats_info[i+1].__str__() == '<font color="#D90000" face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><strong> </strong></font>':
            profile_entry.append("No")
        else:
            profile_entry.append("Yes")
    return profile_entry

def parse_personal(personal_info,profile_entry,url):
    pl_info_line = str(personal_info[4])
    pl_info_line = strip_rawline(pl_info_line)
    pl_list = pl_info_line.split(",")
    pl_list = edge_case(pl_list)
    profile_entry = strip_rawpos(pl_list)
    print "Adding player - " + pl_info_line
    print url
    return profile_entry

def get_final_url(url,year):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    position_search = re.search('Position\:\<\/strong\> \<a href\="http://www.draftscout.com/members/ratings/players.php\?genpos\=\w+', str(soup))  
    position = position_search.group(0)[-2:] 
    return(url+"&draftyear="+str(year)+"&genpos="+position)

def store_data(soup,cur,year):
    url_list = re.findall('http://www.draftscout.com/members/ratings/profile.php\?pyid\=\d+', str(soup))
    for url in url_list:
        final_url = get_final_url(url,year)
        profile_entry = parse_profiles(final_url)
        if(profile_entry == final_url):
            cur.execute("INSERT INTO PLAYERS VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
              % (url,"","","","","","","","","","","","","","","","","","","","","","","","",""))
        else:
            profile_entry = token_fix(profile_entry)
            profile_entry[0] = fix_name(profile_entry[0])
            profile_entry[14] = profile_entry_fix(profile_entry[14])
            profile_entry[22] = profile_entry_fix(profile_entry[22])
            cur.execute("INSERT INTO PLAYERS VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')"
              % (url,profile_entry[0],profile_entry[1],profile_entry[2],profile_entry[3],profile_entry[4],profile_entry[5],profile_entry[6],profile_entry[7],profile_entry[8],profile_entry[9],
                 profile_entry[10],profile_entry[11],profile_entry[12],profile_entry[13],profile_entry[14],profile_entry[15],profile_entry[16],profile_entry[17],profile_entry[18],profile_entry[19],
                 profile_entry[20],profile_entry[21],profile_entry[22],profile_entry[23],profile_entry[24]))
        

def get_data(cur):
    for year in range(1,19):
        for listing in range(65,90):
            try:
                page = requests.get("http://www.draftscout.com/members/searchcollege.php?draftyear=" + str(1999 + year) + "&colabbr=" + chr(listing))
                soup = BeautifulSoup(page.content, 'html.parser')
                store_data(soup,cur,1999+year)
            except:
                print("ERROR")
                print("http://www.draftscout.com/members/searchcollege.php?draftyear=" + str(1999 + year) + "&colabbr=" + chr(listing))


def attempt_connection():
    try:
        con = lite.connect('nfldraftscout_players.db')
        return con
    except Error as e:
        print(e)

def create_table(cur):
    cur.execute("CREATE TABLE PLAYERS(URL TEXT,NAME TEXT,POSITION TEXT,COLLEGE TEXT,CB_INVITE TEXT,CB_HEIGHT TEXT,CB_WEIGHT TEXT,CB_FORTY TEXT,CB_TWENTY TEXT,CB_TEN TEXT,"
                "CB_REPS TEXT,CB_VERT TEXT,CB_BROAD TEXT,CB_SHUTTLE TEXT,CB_DRILL TEXT, PRO_INVITE TEXT, PRO_HEIGHT TEXT,PRO_WEIGHT TEXT,PRO_FORTY TEXT,PRO_TWENTY TEXT,PRO_TEN TEXT,"
                "PRO_REPS TEXT,PRO_VERT TEXT,PRO_BROAD TEXT,PRO_SHUTTLE TEXT,PRO_DRILL TEXT)")

def main():
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