# ---------------------------------------------------------------------------
# helper funcs
# ---------------------------------------------------------------------------
def remove_brackets(row):
	row = list(row)
	row = row[1:-1]
	return ''.join(row)

def split_on_ampersand(row):
	return row.split('&')

def extract_levels(a_list):
	split_a_list = [item.split('(') for item in a_list]
	return [item[0] for item in split_a_list]

def make_new_row(split_row):
	split_a_list = [item.split('(') for item in split_row] # ['1(2|4-9)', '2(3-9)'] => [['1', '2|4-9)'], ['2','3-9)']]
	split_a_list2 = [item[1].rstrip(')') for item in split_a_list] # [['1', '(2|4-9)'], ['2','(3-9)']] => ['2|4-9', '3-9'] 
	split_bars = [item.split('|') for item in split_a_list2] # ['2|4-9', '3-9']  =>  [['2', '4-9'], ['3-9']
	for split_list in split_bars:
		for idx, item in enumerate(split_list):
			if '-' in item:
				bds = [int(val) for val in item.split('-')]
				split_list[idx] = ','.join([str(i) for i in range(bds[0], bds[1] + 1)])
	print split_bars
	no_hyphen_yet = [','.join(item) for  item in split_bars]
	return '-'.join(no_hyphen_yet)


def translate_c2b(row):
	''' 
	input:  a row from a chem lhi file.
	output: the level values and distribution parameters reformatted in the biolhi format.
	'''
	# remove the square brakets
	# split on '&' 
	# grab levels and turn the stuff in parens into a line of dash separated sets of comma separated sets.
	dist = row.split(' ')[-1]
	row = row.split(' ')[0]
	no_brack_row = remove_brackets(row)
	#print 'no_brack_row', no_brack_row
	split_row = split_on_ampersand(no_brack_row)
	#print 'split_row', split_row
	levels = extract_levels(split_row)
	#print 'levels', levels
	new_row = make_new_row(split_row)
	return levels, new_row + ' ' + dist

def translate_b2c(levels , row):
	'''
	input: a row in biolhi format and the associated levels
	output: the same row reformatted in the chemlhi format.
	'''
	pass

if __name__ == '__main__':
	print translate_c2b('[1(2|4-9)&2(3-9)] a_dist')