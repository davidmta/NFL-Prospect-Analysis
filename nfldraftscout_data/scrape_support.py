# -*- coding: utf-8 -*-
import re

def profile_entry_fix(entry):
    entry = entry.replace("\"","-")
    entry = entry.replace("\'", "-")
    return entry

def fix_name(name):
    return name.replace("\'","-")

def strip_rawpos(pl_list):
    strip_pos = pl_list[1].rfind(" ")
    pl_list[1] = pl_list[1][strip_pos+1:]
    return pl_list

def strip_rawline(pl_info_line):
    return pl_info_line[3:len(pl_info_line)-4]

def edge_case(pl_list):
    if len(pl_list) == 4:
        del pl_list[1]
    return pl_list

def token_fix(profile_entry):
    if profile_entry[11] != "NULL":
        profile_entry[11] = re.sub('[\'\"]', ' ', profile_entry[11])
    if profile_entry[22] != "NULL":
        profile_entry[22] = re.sub('[\'\"]', ' ', profile_entry[22])
    return profile_entry