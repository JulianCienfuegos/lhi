import sys

""" 
This script is used for changing the format of a chem lhi file to the bio format. 
Then the bio tool can be used to update dependencies, and then the file can be translated back.
"""

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
	#print split_bars
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

def add_bars(r, i = 0):
	""" Do you know what tail recursion is? Here's an example! """
	if i < len(r) - 1:
		if type(r[i]) == int and r[i+1] == r[i] + 1:
			return add_bars(r, i+1)
		else:
			r.insert(i+1, '|')
			return add_bars(r, i+2)
	else:
		return r


def remove_intermediate(row):
	bar_idxs = [-1] + [idx for idx, item in enumerate(row) if item == '|']
	for i in range(len(bar_idxs)):
		if i+1 != len(bar_idxs): # Then we aren't at the last index.
			if bar_idxs[i+1] > bar_idxs[i] + 1: # Then there are at least two numbers in this interval and we need a hyphen.
				row[bar_idxs[i] : bar_idxs[i+1]] = [row[bar_idxs[i], '-', row[bar_idxs[i+1] - 1]]
				bar_idxs = [-1] + [idx for idx, item in enumerate(row) if item == '|']
		else:
			if len(row) > bar_idxs[i] + 1: # Then there are at least two numbers in this interval and we need a hyphen.
				row[bar_idxs[i] : ] = [row[bar_idxs[i], '-', row[-1]]
	return row

def interleave(levels, row):
	pass

def translate_b2c(levels , row):
	'''
	input: a row in biolhi format and the associated levels
	output: the same row reformatted in the chemlhi format.
	'''
	# Take in a row and a list of levels associated with the row.
	# peel off and store the distribution information.
	# Translate the values between the hyphens into chem format. 
	# Then join the level numbers and the numbers between the hypens into one dependency string.
	dist = row.split(' ')[1]
	row = row.split(' ')[0]
	row = row.split('-')
	for i, r in enumerate(row):
		row[i] = [int(j) for j in r.split(',')]
	print row
	for i, r in enumerate(row):
		row[i] = add_bars(r)
	for i, r in enumerate(row):
		row[i] = remove_intermediates(r)
	return row
	chemrow = interleave(levels, row)
	return chemrow + ' ' + dist

if __name__ == '__main__':
	print translate_c2b('[1(2|4-9)&2(3-9)] a_dist')
	#print add_bars('1,2,3,4,6')
	print translate_b2c(['1', '2'], '1,2,3,5-4,6,7,9 dist')
