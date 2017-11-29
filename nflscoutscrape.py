import requests
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
import re

def parse_profiles():
    page = requests.get("http://www.nfldraftscout.com/ratings/dsprofile.php?pyid=68608&draftyear=2012&genpos=DE")
    soup = BeautifulSoup(page.content, 'html.parser')
    soup_list = soup.find_all('font')
    profiles = []
    
    profile_entry = []
    for i in range(1,len(soup.find_all('font'))):
        link_str = soup_list[i].__str__()
        stat_name = re.search('<font color="#000000" face="Verdana,Geneva,Arial,Helvetica,sans-serif" size="-2"><strong>', link_str)
        if stat_name:
            entry_str = soup_list[i+1].__str__()
            entry = re.search('>.+<',entry_str)
            if entry:
                entry_len = len(entry.group(0))
                entry = entry.group(0)[1:entry_len-1]
            profile_entry.append(entry)
    print(profile_entry)

def main():
    parse_profiles()
    return 0;

if __name__ == "__main__":
    main()
