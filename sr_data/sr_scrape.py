import requests
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
import re
import sys
import csv
import sqlite3 as lite


def parse_year(text):
    year = re.search('\>\d+\<\/a\>',text)
    return strip_raw(year.group(0))

def strip_raw_info(raw_conference):
    left = raw_conference.find('>')
    right = raw_conference.find('<')
    return raw_conference[left+1:right]

def stats_search(pattern,def_stats_entry,tr):
    raw_info = re.search(pattern,tr)
    if raw_info == None:
        def_stats_entry.append('')
    else:
        conference = strip_raw_info(raw_info.group(0))
        def_stats_entry.append(conference)
    return def_stats_entry

def parse_defense(tr,def_stats):
    year = int(parse_year(tr))
    def_stats_entry = []
    ## Conference
    def_stats_entry = stats_search('href\=\"\/cfb\/conferences\/.*?\/\d+\.html\"\>.*?\<\/a\>\<\/td\>',def_stats_entry,tr)
    ## Class
    def_stats_entry = stats_search('\"class\"\s\>\w+\<\/td\>',def_stats_entry,tr)
    ## Position Played
    def_stats_entry = stats_search('\"pos\"\s\>\w+\<\/td',def_stats_entry,tr)
    ## Games
    def_stats_entry = stats_search('stat\=\"g\"\s\>\d+\<\/td',def_stats_entry,tr)
    ## Solo Tackles
    def_stats_entry = stats_search('\"tackles\_solo\"\s\>\d+\<\/td',def_stats_entry,tr)
    ## Assisted Tackles
    def_stats_entry = stats_search('\"tackles\_assists\"\s\>\d+\<\/td',def_stats_entry,tr)
    ## Total Tackles
    def_stats_entry = stats_search('\"tackles\_total\"\s\>\d+\<\/td',def_stats_entry,tr)
    ## Tackles For Losses
    def_stats_entry = stats_search('\"tackles\_loss\"\s\>\d+\.\d+\<\/td',def_stats_entry,tr)
    ## Sacks
    def_stats_entry = stats_search('\"sacks\"\s\>\d+\.\d+\<\/td',def_stats_entry,tr)
    ## Interceptions
    def_stats_entry = stats_search('\"def\_int\"\s\>\d+\<\/td',def_stats_entry,tr)
    ## Interceptions Yards
    def_stats_entry = stats_search('\"def\_int\_yds\"\s\>\d+\<\/td',def_stats_entry,tr)
    ## Interception Return Yards Per Interception
    def_stats_entry = stats_search('\"def\_int\_yds\_per\_int\"\s\>\d+\.\d+\<\/td',def_stats_entry,tr)
    ## Interception Touchdowns
    def_stats_entry = stats_search('\"def\_int\_td\"\s\>\d+\<\/td',def_stats_entry,tr)
    ## Passes Defensed
    def_stats_entry = stats_search('\"pass\_defended\"\s\>\d+\<\/td',def_stats_entry,tr)
    ## Fumbles Recovered
    def_stats_entry = stats_search('\"fumbles\_rec\"\s\>\d+\<\/td',def_stats_entry,tr)
    ## Fumbles Recovery Return Yards
    def_stats_entry = stats_search('\"fumbles\_rec\_yds\"\s\>\d+\<\/td',def_stats_entry,tr)
    ## Fumble Recovery Return Touchdowns
    def_stats_entry = stats_search('\"fumbles\_rec\_td\"\s\>\d+\<\/td',def_stats_entry,tr)
    ## Fumbles Forced
    def_stats_entry = stats_search('\"fumbles\_forced\"\s\>\d+\<\/td',def_stats_entry,tr)
    def_stats[year] = def_stats_entry
    return def_stats;

def parse_passing(tr,pass_stats):
    year = int(parse_year(tr))
    pass_stats_entry = []
    ## School
    pass_stats_entry = stats_search('\"\/cfb\/schools\/.*?\/\d+\.html\"\>.*?\<\/a',pass_stats_entry,tr)
    ## Conferences
    pass_stats_entry = stats_search('\"\/cfb\/conferences\/.*?\/\d+\.html\"\>.*?\<\/a',pass_stats_entry,tr)
    ## Class
    pass_stats_entry = stats_search('class\"\s\>\w+\<\/',pass_stats_entry,tr)
    ## Position Played
    pass_stats_entry = stats_search('\"pos\"\s\>\w+\<\/td',pass_stats_entry,tr)
    ## Games
    pass_stats_entry = stats_search('stat\=\"g\"\s\>\d+\<\/td',pass_stats_entry,tr)
    ## Pass Completions
    pass_stats_entry = stats_search('\"pass\_cmp\"\s\>\d+\<\/td',pass_stats_entry,tr)
    ## Pass Attempts
    pass_stats_entry = stats_search('\"pass\_att\"\s\>\d+\<\/td',pass_stats_entry,tr)
    ## Pass Completion Percentage
    pass_stats_entry = stats_search('\"pass\_cmp\_pct\"\s\>\d+\.\d+\<\/td',pass_stats_entry,tr)
    ## Passing Yards
    pass_stats_entry = stats_search('\"pass\_yds\"\s\>\d+\<\/td',pass_stats_entry,tr)
    ## Passing Yards Per Attempt
    pass_stats_entry = stats_search('\"pass\_yds\_per\_att\"\s\>d+\.\d+\<\/td',pass_stats_entry,tr)
    ## Adjusted Passing Yards Per Attempt
    pass_stats_entry = stats_search('\"adj\_pass\_yds\_per\_att\"\s\>\d+\.\d+\<\/td',pass_stats_entry,tr)
    ## Passing Touchdowns
    pass_stats_entry = stats_search('\"pass\_td\"\s\>\d+\<\/td',pass_stats_entry,tr)
    ## Passing Interceptions
    pass_stats_entry = stats_search('\"pass\_int\"\s\>\d+\<\/td',pass_stats_entry,tr)
    ## Passing Efficency Rating
    pass_stats_entry = stats_search('\"pass\_rating\"\s\>\d+\.\d+\<\/td',pass_stats_entry,tr)
    pass_stats[year] = pass_stats_entry
    return pass_stats;

def rushing_receiving(tr,rr_stats):
    year = int(parse_year(tr))
    rr_stats_entry = []
    
    ## School
    rr_stats_entry = stats_search('\"\/cfb\/schools\/.*?\/\d+\.html\"\>.*?\<\/a',rr_stats_entry,tr)
    ## Conferences
    rr_stats_entry = stats_search('\"\/cfb\/conferences\/.*?\/\d+\.html\"\>.*?\<\/a',rr_stats_entry,tr)
    ## Class
    rr_stats_entry = stats_search('class\"\s\>\w+\<\/',rr_stats_entry,tr)
    ## Position Played
    rr_stats_entry = stats_search('\"pos\"\s\>\w+\<\/td',rr_stats_entry,tr)
    ## Games
    rr_stats_entry = stats_search('stat\=\"g\"\s\>\d+\<\/td',rr_stats_entry,tr)
    ## Rush Attempts
    rr_stats_entry = stats_search('\"rush\_att\"\s\>\d+\<\/td\>',rr_stats_entry,tr)
    ## Rushing Yards
    rr_stats_entry = stats_search('\"rush\_yds\"\s\>\d+\<\/td\>',rr_stats_entry,tr)
    ## Rushing Yards Per Attempt
    rr_stats_entry = stats_search('\"rush\_yds\_per\_att\"\s\>\d+\.\d+\<\/td\>',rr_stats_entry,tr)
    ## Rushing Touchdowns
    rr_stats_entry = stats_search('\"rush\_td\"\s\>\d+\<\/td\>',rr_stats_entry,tr)
    ## Receptions
    rr_stats_entry = stats_search('\"rec\"\s\>\d+\<\/td\>',rr_stats_entry,tr)
    ## Receiving Yards
    rr_stats_entry = stats_search('\"rec\_yds\"\s\>\d+\<\/td\>',rr_stats_entry,tr)
    ## Receiving Yards Per Reception
    rr_stats_entry = stats_search('\"rec\_yds\_per\_rec\"\s\>\d+\.\d+\<\/td\>',rr_stats_entry,tr)
    ## Receiving Touchdowns
    rr_stats_entry = stats_search('\"rec\_td\"\s\>\d+\<\/td\>',rr_stats_entry,tr)
    ## Plays From Scrimmage
    rr_stats_entry = stats_search('\"scrim\_att\"\s\>\d+\<\/td\>',rr_stats_entry,tr)
    ## Yards From Scrimmage
    rr_stats_entry = stats_search('\"scrim\_yds\"\s\>\d+\<\/td\>',rr_stats_entry,tr)
    ## Yards From Scrimmage Per Play
    rr_stats_entry = stats_search('\"scrim\_yds\_per\_att\"\s\>\d+\.\d+\<\/td\>',rr_stats_entry,tr)
    ## Touchdowns From Scrimmage
    rr_stats_entry = stats_search('\"scrim\_td\"\s\>\d+\<\/td\>',rr_stats_entry,tr)
    
    rr_stats[year] = rr_stats_entry
    return rr_stats

def scoring(tr,scoring_stats):
    year = int(parse_year(tr))
    scoring_stats_entry = []
    
    ## School
    scoring_stats_entry = stats_search('\"\/cfb\/schools\/.*?\/\d+\.html\"\>.*?\<\/a',scoring_stats_entry,tr)
    ## Conferences
    scoring_stats_entry = stats_search('\"\/cfb\/conferences\/.*?\/\d+\.html\"\>.*?\<\/a',scoring_stats_entry,tr)
    ## Class
    scoring_stats_entry = stats_search('class\"\s\>\w+\<\/',scoring_stats_entry,tr)
    ## Position Played
    scoring_stats_entry = stats_search('\"pos\"\s\>\w+\<\/td',scoring_stats_entry,tr)
    ## Games
    scoring_stats_entry = stats_search('stat\=\"g\"\s\>\d+\<\/td',scoring_stats_entry,tr)
    ## Rushing Touchdowns
    scoring_stats_entry = stats_search('\"td\_rush\"\s\>\d+\<\/td\>',scoring_stats_entry,tr)
    ## Receiving Touchdowns
    scoring_stats_entry = stats_search('\"td\_rec\"\s\>\d+\<\/td',scoring_stats_entry,tr)
    ## Interception Return Touchdowns
    scoring_stats_entry = stats_search('\"td\_def\_int\"\s\>\d+\<\/td\>',scoring_stats_entry,tr)
    ## Fumble Recovery Return Touchdowns
    scoring_stats_entry = stats_search('\"td\_fumbles\_rec\"\s\>\d+\<\/td',scoring_stats_entry,tr)
    ## Punt Return Touchdowns
    scoring_stats_entry = stats_search('\"td\_punt\_ret\"\s\>\d+\<\/td',scoring_stats_entry,tr)
    ## Kick Return Touchdowns
    scoring_stats_entry = stats_search('\"td\_kick\_ret\"\s\>\d+\<\/td',scoring_stats_entry,tr)
    ## Other Touchdowns
    scoring_stats_entry = stats_search('\"td\_other\"\s\>\d+\<\/td',scoring_stats_entry,tr)
    ## Total Touchdowns
    scoring_stats_entry = stats_search('=\td\_total\"\s\>\d+\<\/td',scoring_stats_entry,tr)
    ## Punt Return Touchdowns
    scoring_stats_entry = stats_search('\"xpm\"\s\>\d+\<\/td',scoring_stats_entry,tr)
    ## Kick Return Touchdowns
    scoring_stats_entry = stats_search('\"fgm\"\s\>\d+\<\/td',scoring_stats_entry,tr)
    ## Other Touchdowns
    scoring_stats_entry = stats_search('\"two\_pt\_md\"\s\>\d+\<\/td',scoring_stats_entry,tr)
    ## Total Touchdowns
    scoring_stats_entry = stats_search('\"safety\_md\"\s\>\d+\<\/td',scoring_stats_entry,tr)
    ## Total Touchdowns
    scoring_stats_entry = stats_search('\"points\"\s\>\d+\<\/td',scoring_stats_entry,tr)
    
    scoring_stats[year] = scoring_stats_entry
    return scoring_stats

def punting_and_kicking(tr,pk_stats):
    year = int(parse_year(tr))
    pk_stats_entry = []
    
    ## School
    pk_stats_entry = stats_search('\"\/cfb\/schools\/\w+\/.*?\.html\"\>.*?\<\/a',pk_stats_entry,tr)
    ## Conferences
    pk_stats_entry = stats_search('\"\/cfb\/conferences\/.*?\/\d+\.html\"\>.*?\<\/a',pk_stats_entry,tr)
    ## Class
    pk_stats_entry = stats_search('class\"\s\>\w+\<\/',pk_stats_entry,tr)
    ## Position Played
    pk_stats_entry = stats_search('\"pos\"\s\>\w+\<\/td',pk_stats_entry,tr)
    ## Games
    pk_stats_entry = stats_search('stat\=\"g\"\s\>\d+\<\/td',pk_stats_entry,tr)
    ## Punts
    pk_stats_entry = stats_search('\"punt\"\s\>\d+\<\/td\>',pk_stats_entry,tr)
    ## Punting Yards
    pk_stats_entry = stats_search('\"punt\_yds\"\s\>\d+\<\/td',pk_stats_entry,tr)
    ## Punting Yards Per Punt
    pk_stats_entry = stats_search('\"punt\_yds\_per\_punt\"\s\>\d+\.\d+\<\/td',pk_stats_entry,tr)
    ## Extra Point Made
    pk_stats_entry = stats_search('\"xpm\"\s\>\d+\<\/td',pk_stats_entry,tr)
    ## Extra Point Attempts
    pk_stats_entry = stats_search('\"xpa\"\s\>\d+\<\/td',pk_stats_entry,tr)
    ## Extra Point Percentage
    pk_stats_entry = stats_search('\"xp\_pct\"\s\>\d+\<\/td',pk_stats_entry,tr)
    ## Field Goals Made
    pk_stats_entry = stats_search('\"fgm\"\s\>\d+\<\/td',pk_stats_entry,tr)
    ## Field Goal Attempts
    pk_stats_entry = stats_search('\"fga\"\s\>\d+\<\/td',pk_stats_entry,tr)
    ## Field Goal Percentage
    pk_stats_entry = stats_search('"fg_pct" >\d+\.\d+\<\/td',pk_stats_entry,tr)
    ## Points Kicking
    pk_stats_entry = stats_search('\"kick\_points\"\s\>\d+\<\/td',pk_stats_entry,tr)
    
    pk_stats[year] = pk_stats_entry
    return pk_stats

def punt_kick_returns(tr,pkreturn_stats):
    year = int(parse_year(tr))
    pkreturns_stats_entry = []
    
    ## School
    pkreturns_stats_entry = stats_search('\"\/cfb\/schools\/.*?\/\d+\.html\"\>.*?\<\/a',pkreturns_stats_entry,tr)
    ## Conferences
    pkreturns_stats_entry = stats_search('\"\/cfb\/conferences\/.*?\/\d+\.html\"\>.*?\<\/a',pkreturns_stats_entry,tr)
    ## Class
    pkreturns_stats_entry = stats_search('class\"\s\>\w+\<\/',pkreturns_stats_entry,tr)
    ## Position Played
    pkreturns_stats_entry = stats_search('\"pos\"\s\>\w+\<\/td',pkreturns_stats_entry,tr)
    ## Games
    pkreturns_stats_entry = stats_search('stat\=\"g\"\s\>\d+\<\/td',pkreturns_stats_entry,tr)
    ## Kickoff Returns
    pkreturns_stats_entry = stats_search('\"kick\_ret\"\s\>\d+\<\/td',pkreturns_stats_entry,tr)
    ## Kickoff Return Yards
    pkreturns_stats_entry = stats_search('\"kick\_ret\_yds\"\s\>\d+\<\/td',pkreturns_stats_entry,tr)
    ## Kickoff Return Yards Per Return
    pkreturns_stats_entry = stats_search('\"kick\_ret\_yds\_per\_ret\"\s\>\d+\.\d+\<\/td',pkreturns_stats_entry,tr)
    ## Kickoff Return Touchdowns
    pkreturns_stats_entry = stats_search('\"kick\_ret\_td\"\s\>\d+\<\/td',pkreturns_stats_entry,tr)
    ## Punt Returns
    pkreturns_stats_entry = stats_search('\"punt\_ret\"\s\>\d+\<\/td',pkreturns_stats_entry,tr)
    ## Punt Return Yards
    pkreturns_stats_entry = stats_search('\"punt\_ret\_yds\"\s\>\d+\<\/td',pkreturns_stats_entry,tr)
    ## Punt Return Yards Per Return
    pkreturns_stats_entry = stats_search('\"punt\_ret\_yds\_per\_ret\"\s\>\d+\.\d+\<\/td',pkreturns_stats_entry,tr)
    ## Punt Return Touchdowns
    pkreturns_stats_entry = stats_search('\"punt\_ret\_td\"\s\>\d+\<\/td',pkreturns_stats_entry,tr)
   
    pkreturn_stats[year] = pkreturns_stats_entry
    return pkreturn_stats

def strip_position(raw_str):
    start = raw_str.find(':')
    return raw_str[start+2:len(raw_str)-5]


def player_stats(player_url,years_active,player_name):
    page = requests.get("https://www.sports-reference.com" + player_url)
    pkreturn_stats = {}
    pk_stats = {}
    scoring_stats = {}
    rr_stats = {}
    pass_stats = {}
    def_stats = {}
    trs = re.findall('\<tr\s\>.*?\<\/tr\>',page.content)

    ## Position
    position_match = re.search('Position<\/strong\>\:\s\w+\s\<\/p\>',page.content)
    if position_match!=None:
        position = strip_position(position_match.group(0))
    else:
        position = ""
    ## Draft
    draft_match = re.search('\<p\>\<strong\>Draft\:\<\/strong\>.*?\<\/p\>',page.content)
    if draft_match == None:
        draft = ""
    else:
        draft = draft_match.group(0)
    ## Height
    height_match = re.search('itemprop\=\"height\"\>\d\-\d+\<\/span\>\,\&nbsp\;\<span',page.content)
    if height_match!= None:
        height = strip_raw_info(height_match.group(0))
    else:
        height = ""
    ## Weight
    weight_match = re.search('itemprop\=\"weight\"\>\d+lb\<\/span\>\&nbsp',page.content)
    if weight_match!= None:
        weight = strip_raw_info(weight_match.group(0))
    else:
        weight = ""
 
    for tr in trs:
        if re.search('tackles_assists',tr) != None:
            def_stats = parse_defense(tr,def_stats)
        elif re.search('pass_att',tr) != None:
            pass_stats = parse_passing(tr,pass_stats)
        elif re.search('rush_att',tr) != None:
            rr_stats = rushing_receiving(tr,rr_stats)
        elif re.search('td_def_int',tr) != None:
            scoring_stats = scoring(tr,scoring_stats)
        elif re.search('punt_yds_per_punt',tr) != None:
            pk_stats = punting_and_kicking(tr,pk_stats)
        elif re.search('kick_ret_yds_per_ret',tr) != None:
            pkreturn_stats = punt_kick_returns(tr,pkreturn_stats)
    stats = [str(def_stats).replace('\'','\'\''),str(pass_stats).replace('\'','\'\''),str(rr_stats).replace('\'','\'\''),str(scoring_stats).replace('\'','\'\''),str(pk_stats).replace('\'','\'\''),str(pkreturn_stats).replace('\'','\'\'')]
    return position,draft,height,weight,stats

def strip_raw(raw):
    return raw[1:len(raw)-4]

def strip_raw_url(raw_url):
    return raw_url[12:]

def get_player_splits(player_url):
    splits_url = re.sub('.html','/splits/',player_url)
    page = requests.get("https://www.sports-reference.com" + splits_url)
    if page.status_code == 404:
        return
    soup = BeautifulSoup(page.content,"html.parser")
    return soup.findAll('table')

def get_player_logs(player_url):
    gamelog_url = re.sub('.html','/gamelog/',player_url)
    page = requests.get("https://www.sports-reference.com" + gamelog_url)
    if page.status_code == 404:
        return
    soup = BeautifulSoup(page.content,"html.parser")
    return soup.findAll('table')


def get_players(page,cur):
    soup = BeautifulSoup(page.content,"html.parser")
    p_soup = soup.findAll('p')
    for p in p_soup:
        url_result = re.search('\<p\>\<a href\=\"/cfb/players/\w+\-\w+\-\d.html',str(p))
        years_result = re.search('\(\d+\-\d+\)',str(p))
        name_result = re.search('\.html\"\>.*?\s.*?\<\/a\>',str(p))
        college_result = re.search('\/cfb\/schools\/.*?\/\"\>.*?\<\/a\>',str(p))
        if url_result and years_result and name_result and college_result != None:
            years_active = years_result.group(0)
            player_url = strip_raw_url(url_result.group(0))
            player_name = strip_raw_info(name_result.group(0))
            player_name = player_name.replace('\'','\'\'')
            print player_name
            print player_url
            college = strip_raw_info(college_result.group(0))
            position,draft,height,weight,stats = player_stats(player_url,years_active,player_name)
            raw_player_logs = get_player_logs(player_url)
            raw_player_splits = get_player_splits(player_url)
            cur.execute("INSERT INTO SR_PLAYERS VALUES('%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s','%s')" % (player_name,player_url,college,years_active,position,height,weight,draft,stats[0],stats[1],stats[2],stats[3],stats[4],stats[5],str(raw_player_logs),str(raw_player_splits)))

def get_data(cur):
    for letter in range(ord('a'),ord('b')):
        page_index = 2
        page = requests.get("https://www.sports-reference.com/cfb/players/" + chr(letter) + "-index" + ".html")
        get_players(page,cur)
        while(True):
            page = requests.get("https://www.sports-reference.com/cfb/players/" + chr(letter) + "-index" + str(page_index) + ".html")
            if page.status_code == 404:
                return
            get_players(page,cur)
            page_index = page_index + 1

def attempt_connection():
    try:
        con = lite.connect('sr_players_database.db')
        return con
    except Error as e:
        print(e)

def create_table(cur):
    cur.execute("CREATE TABLE SR_PLAYERS(PLAYER TEXT,URL TEXT,COLLEGE TEXT,YEARS_ACTIVE TEXT,POSITION TEXT,HEIGHT TEXT,WEIGHT TEXT,DRAFT TEXT,DEFENSE_AND_FUMBLES TEXT,PASSING TEXT,RUSHING_AND_RECEIVING TEXT,SCORING TEXT,PUNTING_AND_KICKING TEXT,PUNT_AND_KICK_RETURNS TEXT,GAMELOGS TEXT,SPLITS TEXT)")
def main():
    con = attempt_connection()
    with con:
        cur = con.cursor()
        #create_table(cur)
        get_data(cur)
    return 0;

if __name__ == "__main__":
    main()
