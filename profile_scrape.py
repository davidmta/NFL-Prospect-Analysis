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
    return profile_entry

def store_profile(profile_entry,personal_info,stats_info,i):
    link_str = stats_info[i].__str__()

    stat_name = re.search('<font color="#000000" face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><strong>', link_str)
    if stat_name:
        entry_str = stats_info[i+1].__str__()
        entry = re.search('>[\d.\'\\/ "Yes]+</font',entry_str)
        if entry:
            entry_len = len(entry.group(0))
            entry = entry.group(0)[1:entry_len-6]
            profile_entry.append(entry)
        elif entry_str == '<font color="#000000" face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"></font>':
            profile_entry.append("NULL")
    profile_entry = determine_participation(link_str,stats_info,profile_entry,i)
    return profile_entry

def determine_participation(link_str,stats_info,profile_entry,i):
    if link_str == '<font color="#BA303E" face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><strong></strong></font>' and stats_info[i-1].__str__() == '<font color="#000000" face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><strong>Combine Invite:</strong></font>':
        profile_entry.append("No")
    elif link_str == '<font color="#BA303E" face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><strong>Yes</strong></font>':
        profile_entry.append("Yes")
    if link_str == '<font color="#000000" face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><strong>Dates:</strong></font>':
        print stats_info[i+1].__str__()
        if stats_info[i+1].__str__() == '<font color="#D90000" face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><strong> </strong></font>':
            profile_entry.append("No")
        else:
            profile_entry.append("Yes")
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



