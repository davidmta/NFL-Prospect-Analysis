# -*- coding: utf-8 -*-
import re
import sys

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

def strip_ending_label(str):
	return str[:-4]

def create_year_split(p_str):
	year_split = {}
	all_year_result = re.findall('<a href="/years/\d+/">\d+</a><',p_str)
	for i in range(0,len(all_year_result)):
		start = p_str.find(all_year_result[i])
		if i == len(all_year_result)-1:
			year = strip_brackets(all_year_result[i])
			year = strip_ending_label(year)
			year_split[year] = p_str[start:]	
		else:
			end = p_str.find(all_year_result[i+1])
			year = strip_brackets(all_year_result[i])
			year = strip_ending_label(year)
			year_split[year] = p_str[start:end]
	return year_split

def parse_defense(p_str):
    def_stats_entry = {}
    year_split = create_year_split(p_str)

    for year, raw in year_split.iteritems():
    	defense_entry = []
    	# Age
    	defense_entry = stats_search('data-stat="age">\d+</td>',defense_entry,raw)
    	# Team
    	defense_entry = stats_search('a href="/teams/\w+/\d+.htm" title="\w+ \w+">\w+</a>',defense_entry,raw)
    	# Position
    	defense_entry = stats_search('data-stat="pos">.*?</td>',defense_entry,raw)
    	# Uniform Number
    	defense_entry = stats_search('data-stat="uniform_number">\d+</td>',defense_entry,raw)
    	# Games Played
    	defense_entry = stats_search('data-stat="g">\d+</td>',defense_entry,raw)
    	# Games Started
    	defense_entry = stats_search('data-stat="gs">\d+</td>',defense_entry,raw)
    	# Interceptions
    	defense_entry = stats_search('data-stat="def_int">\d+</td><',defense_entry,raw)
    	# Interception Return Yards
    	defense_entry = stats_search('data-stat="def_int_yds">\d+</td>',defense_entry,raw)
    	# Interceptions Return For A Touchdown
    	defense_entry = stats_search('data-stat="def_int_td">\d+</td>',defense_entry,raw)
    	# Longest Interception Return
    	defense_entry = stats_search('data-stat="def_int_long">\d+</td>',defense_entry,raw)
    	# Passes Defensed
    	defense_entry = stats_search('data-stat="pass_defended">\d+</td><',defense_entry,raw)
    	# Fumbles Forced
    	defense_entry = stats_search('data-stat="fumbles_forced">\d+</td><',defense_entry,raw)
    	# Fumbles
    	defense_entry = stats_search('data-stat="fumbles">\d+</td>',defense_entry,raw)
    	# Fumbles Recovered
    	defense_entry = stats_search('data-stat="fumbles_rec">\d+</td>',defense_entry,raw)
    	# Fumble Recovery Yard
    	defense_entry = stats_search('data-stat="fumbles_rec_yds">\d+</td>',defense_entry,raw)
    	# Fumble Recovery Touchdown
    	defense_entry = stats_search('data-stat="fumbles_rec_td"></td>',defense_entry,raw)
    	# Sacks
    	defense_entry = stats_search('data-stat="sacks">\d+</td>',defense_entry,raw)
    	# Solo Tackles
    	defense_entry = stats_search('data-stat="tackles_solo">\d+</td>',defense_entry,raw)
    	# Assisted Tackles
    	defense_entry = stats_search('data-stat="tackles_assists">\d+</td>',defense_entry,raw)
    	# Safeties
    	defense_entry = stats_search('data-stat="safety_md"></td>',defense_entry,raw)
    	# AV
    	defense_entry = stats_search('data-stat="av">\d+</td>',defense_entry,raw)
    	def_stats_entry[year] = defense_entry 
    return def_stats_entry;

def parse_passing(tr):
	pass_stats_entry = {}
	print tr
	return pass_stats_entry