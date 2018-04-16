# -*- coding: utf-8 -*-
import re

def strip_position(position):
	return re.sub('[()]', '', position)

def standardize_for_SQL(raw):
    return raw.replace('\'','\'\'')

def strip_brackets(string):
    left = string.find('>')
    right = string.rfind('<')
    return string[left+1:right]

def stats_search(pattern,defense_entry,p_str):
    raw_info = re.search(pattern,p_str)
    if raw_info == None:
        defense_entry.append('')
    else:
        conference = strip_brackets(raw_info.group(0))
        defense_entry.append(conference)
    return defense_entry

def strip_quotes(string):
    left = string.find('"')
    right = string.rfind('"')
    return string[left+1:right]

def strip_birthplace(string):
	string = string.replace('<a href="/friv/birthplaces.cgi?country=','')
	string = string.replace('    in ','')
	string = string.replace('"','')
	return string

def create_year_split(p_str):
	year_split = []
	all_year_result = re.findall('<a href="/years/\d+/">\d+</a></',p_str)
	for year in all_year_result:
		year_split.append(p_str.find(year))
	for i in range(0,len(year_split)):
		if i == len(year_split)-1:
			year_split[i] = p_str[year_split[i]]
		else:
			year_split[i] = p_str[year_split[i]:year_split[i+1]]
	return year_split

def parse_defense(p_str):
    def_stats_entry = []
    defense_entry = []
    year_split = create_year_split(p_str)
    for year in year_split: 
    	# Age
    	defense_entry = stats_search('data-stat="age" >\d+</td>',defense_entry,p_str)

    	def_stats_entry.append(defense_entry)

    return def_stats_entry;