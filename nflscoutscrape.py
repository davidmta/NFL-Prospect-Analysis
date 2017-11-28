import requests
from bs4 import BeautifulSoup
from lxml.html.soupparser import fromstring
import re

def get_url():
    url_list = []
    for listing in range(65,90):
        page = requests.get("http://www.nfldraftscout.com/searchcollege.php?draftyear=2012&colabbr="+chr(listing))
        soup = BeautifulSoup(page.content, 'html.parser')

        for link in soup.find_all('a'):
            link_str = link.__str__()
            root = re.search('http://www.nfldraftscout.com/ratings/dsprofile.php\?pyid?\=\d+', link_str)
            draft_branch = re.search('draftyear\=\d+', link_str)
            pos_branch = re.search('genpos\=\w+', link_str)
            
            if root:
                url = '\"' + root.group(0) + "&" + draft_branch.group(0) + "&" + pos_branch.group(0) + '\"'
                url_list.append(url)
    return url_list

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
    stats = []

def main():
    #url_list = get_url()
    parse_profiles()
    return 0;

if __name__ == "__main__":
    main()
