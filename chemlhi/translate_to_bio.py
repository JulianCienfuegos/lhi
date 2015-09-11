# ---------------------------------------------------------------------------
# helper funcs
# ---------------------------------------------------------------------------
def remove_brackets(row):
	row = row.split()
	row = row[1:-1]
	return ''.join(row)

def split_on_ampersand(row):
	return row.split('&')

def extract_levels(a_list):
	split_a_list = [item.split('(') for item in a_list]
	return [item[0] for item in split_a_list]

def make_new_row(split_row):
	split_a_list = [item.split('(') for item in a_list] # ['1(2|4-9)', '2(3-9)'] => [['1', '2|4-9)'], ['2','3-9)']]
	split_a_list2 = [item[1].rstrip(')') for item in split_a_list] # [['1', '(2|4-9)'], ['2','(3-9)']] => ['2|4-9', '3-9'] 
	split_bars = [item.split('|') for item in split_a_list2]
	expand_dashes = []
	no_hyphen_yet = [item.join(',') for ]


def translate_c2b(row):
	''' 
	input:  a row from a chem lhi file.
	output: the level values and distribution parameters reformatted in the biolhi format.
	'''
	# remove the square brakets
	# split on '&' 
	# grab levels and turn the stuff in parens into a line of dash separated sets of comma separated sets.
	no_brack_row = remove_brackets(row)
	split_row = split_on_ampersand(no_brack_row)
	levels = extract_levels(split_row)
	new_row = make_new_row(split_row)
	return levels, new_row

def translate_b2c(levels , row):
	'''
	input: a row in biolhi format and the associated levels
	output: the same row reformatted in the chemlhi format.
	'''
	pass