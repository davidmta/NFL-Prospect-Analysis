import re

def strip_position(position):
	return re.sub('[()]', '', position)

def standardize_for_SQL(raw):
    return raw.replace('\'','\'\'')


