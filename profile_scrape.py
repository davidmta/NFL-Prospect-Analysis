import requests
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
import re

def parse_profiles(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content, 'html.parser')
    personal_info = soup.find_all('b')
    stats_info = soup.find_all('font')
    profile_entry = []
    profile_entry = parse_personal(personal_info,profile_entry)
    for i in range(1,len(soup.find_all('font'))):
        profile_entry = store_profile(profile_entry,personal_info,stats_info,i)

def store_profile(profile_entry,personal_info,stats_info,i):
    link_str = stats_info[i].__str__()
    stat_name = re.search('<font color="#000000" face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><strong>', link_str)
    if stat_name:
        entry_str = stats_info[i+1].__str__()
        entry = re.search('>[\d.\'\"]+<',entry_str)
        if entry:
            entry_len = len(entry.group(0))
            entry = entry.group(0)[1:entry_len-1]
            profile_entry.append(entry)
        elif entry_str == '<font color="#000000" face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"></font>':
            profile_entry.append(None)
    return profile_entry

def strip_rawpos(pl_list):
    strip_pos = pl_list[1].rfind(" ")
    pl_list[1] = pl_list[1][strip_pos+1:]
    return pl_list

def strip_rawline(pl_info_line):
    return pl_info_line[3:len(pl_info_line)-4]

def parse_personal(personal_info,profile_entry):
    pl_info_line = str(personal_info[4])
    pl_info_line = strip_rawline(pl_info_line)
    pl_list = pl_info_line.split(",")
    profile_entry = strip_rawpos(pl_list)
    print("Adding player - " + pl_info_line)
    return profile_entry



