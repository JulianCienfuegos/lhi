"""
by Melvyn Ian Drag. 7-23-2015.
This code will rewrite a dependency such that a certain level is removed.

There are 16 distinct ways we can find a number n, n_0 < n < n_1 in the sequence of values in a given level.

Column1                    Column2            Column3          Column4
(n), (case nought)        (n_0-n_1),         (n-n_1),         (n_0-n)
(n|...),                  (n_0-n_1|...),     (n-n_1|...),     (n_0-n|...)
(...|n),                  (...|n_0-n_1),     (...|n-n_1),     (...|n_0-n)
(...|n|...),              (...|n_0-n_1|...), (...|n-n_1|...), (...|n_0-n|...)

Case Column1: we have no leftover dependencies (case nought), or we just remove the one value.
Case Column2: we have to split the dependency like:
		(*n_0-n_1*) ==> (*n_0-nminus1|nplus1-n_1) OR
						(*n_0-nminus1|n_1) OR
						(*n_0|nplus1-n_1)
Case Column3: we have to remove 'n'
		(*n-n_1*) ==> (n_1) OR
					  (nplus1-n_1)
Case Column4 :very similar to Case Column3
		(*n_0-n*) ==> (n_0) OR
					  (n_0-nminus1)
					  
To begin reading this code, start with RemoveDependency(). It calls all of the other functions. The API makes things very readable!

NOTE : This could all probably be implemented in regular expressions in about 10 lines but I'm not yet good enough with regex to do that!
We've got about 200 lines of code here, and about 100 lines of documentation.
"""
import sys
from collections import Counter
from itertools import groupby 
from operator import itemgetter

def SplitString(s):
	"""
	We first split the string.
	Then, the numbers that are longer than one digit will be split in two!
	So we rejoin them.
	We find all characters occurring between one special character and the next special character that immediately appears.
		'(' is always followed by '-' or ')'
		'-' is always followed by '|' or ')'
		'|' is always followed by '-' or ')'
	THE SOLE PURPOSE OF THIS FUNCTION IS TO GROUP EVERY TERM IN A DEPENDENCY STRUCTURE BY ITSELF IN A LIST. In this
	function, a GROUP is a set of alphanumeric characters which form a logical unit.
	"""
	new_s = []
	S = list(s)
	d = {'(':['-', ')'], 
		 '|':['-', ')', '|'], 
		 '-':['|', ')']}
	inGroup = False
	c = []
	search = []
	for i in S:
		if inGroup:
			if i not in search:
				c.append(i)
			if i in search:
				search = []
				c = ('').join(c)
				new_s.append(c)
				c = []
				inGroup = False
		if not inGroup and i in d:
			new_s.append(i)
			inGroup = True
			search = d[i]
		if not inGroup and i not in d:
			new_s.append(i)
	return new_s
	
def col1(subl, value, i):
	"""
	This function will remove a dependency. If the dependency is of the non-nought type specified above.
	"""
	if (subl[i-1]=='(' and subl[i+1] == '|'):
		subl[i-1:i+2] = ['(']
	elif(subl[i-1]=='|' and subl[i+1] == ')'):
		subl[i-1:i+2] = [')']
	elif (subl[i-1]=='|' and subl[i+1] == '|'):
		subl[i-1:i+2] = ['|']
	else:
		sys.exit('Error! I don\'t understand this col1 dependency in col1()!')
	return subl		
	
def col2(subl, value, i):
	"""
	This function reformats a sublist when  the sublist is of the form specified in column 2 at the top of 
	this file. It first checks the bounds surrounding the value of interest. If the lower bound is smaller than value - 1
	and the upeper bounds is larger than value + 1, then we write in place of sublist[i-1:i+1] the following:
		sublist[i-1] - value-1 | value + 1 - sublist[i+1]
	If, on the other hand, the lower bound is equal to value - 1, then we replace with:
		sublist[i-1] | value + 1 - sublist[i+1]
	If the upper bound is equal to value + 1, then we replace with:
		sublist[i-1] -  value-1 | sublist[i+1]
	Lastly, if both are just one unit away from value, we write:
		sublist[i-1]|sublist[i+1]
	"""
	subl[i] = '|' # replace the hyphen with a bar
	if subl[i-1] == str(int(value) - 1):
		x = 1 + 1
	else:
		subl[i-1: i] = [subl[i-1], '-', str(int(value) - 1)]
		i = i+2	 # THIS IS VERY IMPORTANT!!!!!!!! WE INSERT THREE VALUES INTO ONE POSITION, SO INDICES MOVE UP BY 2.
	if subl[i+1] == str(int(value) + 1):
		x = 1+1
	else:
		subl[i+1:i+2] = [str(int(value) + 1), '-', subl[i+1]]
	return subl
	
def col3(subl, value, i):
	"""
	This function handles the case when when our number of interest is one of the lower bounds of the range.
	The reasoning is similar to the reasoning presented in the docstring for the col2 function.
	"""
	if subl[i+1] == str(int(subl[i-1]) + 1):
		subl[i-1:i+2] = subl[i+1] # remove the range and replace with the single remaining value.
	else:
		subl[i-1:i+2] = [str(int(subl[i-1]) + 1), '-', subl[i+1]]
	return subl

def col4(subl, value, i):
	"""
	This function handles the case when the number of interest is the upper bound of some range, as is the 
	case in column 4 above. The reasoning here is similar to the reasoning in the col2 function.
	"""
	if subl[i-1] == str(int(subl[i+1]) - 1):
		subl[i-1:i+2] = subl[i-1] # remove the range and replace with the single remaining value.
	else:
		subl[i-1:i+2] = [subl[i-1], '-', str(int(subl[i+1]) - 1)]
	return subl
	
	
def RemoveDependency(s, level, value):
		"""
		This function provides step 2 of the process started by SplitString().
		SplitString() takes a string which describes a dependency and translates it into a list of items. 
		Now we will iterate through the list of items, find the appropriate level, then remove the appr-
		opriate value from that level of the dependency.
		The sixteen ways in which the value can be found are specified in the beginning of this file.
		A level number always comes before a '('
		This function returns the 'leftovers' of the dependency. So, if after removing a value there
		will be no leftovers, as described in column 1 of the documentation appearing at the beginning of this file, 
		we return an empty string. Otherwise, we return a string describing the left over dependency.
		"""
		new_s = SplitString(s)
		n = len(new_s)
		levelFound = False
		valueFound = False
		for i in range(1, n):	
			if new_s[i] == '(' and new_s[i-1] == level:
				levelFound = True
				start_of_sub = i
				end_of_sub = new_s[i:].index(')') + i + 1 
				subl = new_s[start_of_sub:end_of_sub]
				m = len(subl)
				for i in range(1,m-1):
					if subl[i] == value and subl[i-1]=='(' and subl[i+1] == ')':
						valueFound = True
						return '' # case nought. One unique dependency in this level.
						break
					if subl[i] == value and ((subl[i-1]=='(' and subl[i+1] == '|') or (subl[i-1]=='|' and subl[i+1] == ')') or (subl[i-1]=='|' and subl[i+1] == '|')):
						valueFound = True
						subl = col1(subl, value, i)
						break
					if subl[i] == '-' and int(subl[i-1]) < int(value) and int(subl[i+1]) > int(value):
						valueFound = True
						subl = col2(subl, value, i)
						break
					if subl[i] == '-' and subl[i-1] == value and int(subl[i+1]) > int(value):
						valueFound = True
						subl = col3(subl, value, i)
						break
					if subl[i] == '-' and int(subl[i-1]) < int(value) and subl[i+1] == value:
						valueFound = True
						subl = col4(subl, value, i)
						break
				new_s[start_of_sub:end_of_sub] = subl
				break
		if not levelFound:
			sys.exit('Error! Level not found in the provided dependency string.')
		if not valueFound:
			sys.exit('Error! Value not found in the provided dependency string.')
		s = ''.join(new_s)
		return s

"""
The following routine is similar to the remove dependency routine above, except this function removes a subset of the form (a2-a3)
from a dependency. As above, there are four columns of choices to consider. a1<a2<a3<a4 in the following examples. What
follow are the 16 types of dependencies in which a dependency of the form a2-a3 could be nested.

Column 1            Column 2          Column 3          Column 4
(a2-a3)             (a1-a4)           (a2-a4)           (a1-a3)
(...|a2-a3)         (...|a1-a4)       (...|a2-a4)       (...|a1-a3)
(a2-a3|...)         (a1-a4|...)       (a2-a4|...)       (a1-a3|...)
(...|a2-a3|...)     (...|a1-a4|...)   (...|a2-a4|...)   (...|a1-a3|...)

The 'case nought' is, as before, the first entry in column 1.
"""

def scol1(subl, a2, a3, i):
	"""
	This function handles the non case nought dependencies which are described in column1.
	a2 and a3 are as above, subl is the sublist we are looking in, and i is the position of the '-'.
	"""
	if subl[i-1]=='(' and subl[i+3] == '|':
		subl[i-1:i+4] = ['(']
	elif subl[i-1]=='|' and subl[i+3] == ')':
		subl[i-1:i+4] = [')']
	elif subl[i-1]=='|' and subl[i+3] == '|':
		subl[i-1:i+4] = ['|']
	else:
		sys.exit('Error! I don\'t understand this col1 dependency in scol1()!')
	return subl

def scol2(subl, a2, a3, i):
	"""
	This function handles the dependencies described in column 2. 
	a2 and a3 are as above, subl is the sublist we are looking in, and i is the position of the '-'.
	We know:
			subl[i+1] == '-' and int(subl[i]) < int(a2) and int(subl[i+2]) > int(a3)
	"""
	subl[i+1] = '|' # replace the hyphen with a bar
	if subl[i] == str(int(a2) - 1):
		x = 1 + 1 # do nothing code
	else:
		subl[i: i+1] = [subl[i], '-', str(int(a2) - 1)]
		i = i+2	 # THIS IS VERY IMPORTANT!!!!!!!! WE INSERT THREE VALUES INTO ONE POSITION, SO INDICES MOVE UP BY 2.
	if subl[i+2] == str(int(a3) + 1):
		x = 1+1 # do nothing code.
	else:
		subl[i+2:i+3] = [str(int(a3) + 1), '-', subl[i+2]]
	return subl 


def scol3(subl, a2, a3, i):
	"""
	This function handles the dependencies described in column 3. 
	a2 and a3 are as above, subl is the sublist we are looking in, and i is the position of the '-'.
	We know:
		subl[i+1] == '-' and subl[i] == a2 and int(subl[i+2]) > int(a3)
	"""
	if subl[i+2] == str(int(a3) + 1):
		subl[i:i+3] = subl[i+2] # remove the range and replace with the single remaining value.
	else:
		subl[i:i+3] = [str(int(a3) + 1), '-', subl[i+2]]
	return subl

def scol4(subl, a2, a3, i):
	"""
	This function handles the dependencies described in column 4.
	a2 and a3 are as above, subl is the sublist we are looking in, and i is the position of the '-'.
	We know:
		 subl[i+1] == '-' and int(subl[i]) < int(a2) and subl[i+2] == a3
	"""
	if subl[i] == str(int(a2) - 1):
		subl[i:i+3] = subl[i] # remove the range and replace with the single remaining value.
	else:
		subl[i:i+3] = [subl[i], '-', str(int(a2) - 1)]
	return subl

def RemoveSubset(s, level, a2, a3):
		"""
		This function is like the RemoveDependency function, however this function can remove a 
		subset of a dependency and not just an individual value. For example, this function can turn
									s = [1(1-3)&2(1-4|6-8)]
		into 
									[1(1-3)&2(1|4|6-8)]
		when you pass it the parameters s, level='2', a2='2', a3='3'.
		"""
		new_s = SplitString(s)
		n = len(new_s)
		levelFound = False
		setFound = False
		for i in range(1, n-3): # 1(1)] # we need to go 4 back from the end of the list to get the last level value's parenthesis.	
			if new_s[i] == '(' and new_s[i-1] == level:
				levelFound = True
				start_of_sub = i
				end_of_sub = new_s[i:].index(')') + i + 1
				subl = new_s[start_of_sub:end_of_sub]
				m = len(subl)
				for i in range(1,m-3):
					if subl[i-1]=='(' and subl[i] == a2 and subl[i+1] == '-' and subl[i+2] == a3 and subl[i+3] == ')':
						setFound = True
						return '' # case nought. One unique dependency in this level.
						break
					if (subl[i] == a2 and subl[i+1] == '-' and subl[i+2] == a3) and ((subl[i-1]=='(' and subl[i+3] == '|') or (subl[i-1]=='|' and subl[i+3] == ')') or (subl[i-1]=='|' and subl[i+3] == '|')):
						setFound = True
						subl = scol1(subl, a2, a3, i)
						break
					if  subl[i+1] == '-' and int(subl[i]) < int(a2) and int(subl[i+2]) > int(a3):
						setFound = True
						subl = scol2(subl, a2, a3, i)
						break
					if subl[i+1] == '-' and subl[i] == a2 and int(subl[i+2]) > int(a3):
						setFound = True
						subl = scol3(subl, a2, a3, i)
						break
					if subl[i+1] == '-' and int(subl[i]) < int(a2) and subl[i+2] == a3:
						setFound = True
						subl = scol4(subl, a2, a3, i)
						break
				new_s[start_of_sub:end_of_sub] = subl
				break
		if not levelFound:
			sys.exit('Error! Level not found in the provided dependency string.')
		if not setFound:
			sys.exit('Error! Subset not found in the provided dependency string.')
		s = ''.join(new_s)
		return s

def Intersection(dependency1, dependency2): # This function is symmetrical!
	''' Return the intersection string of dependency1 and dependency2 '''
	dep1 = SplitString(dependency1)
	dep2 = SplitString(dependency2)
	n = Counter(dep1)['(']
	m = Counter(dep2)['('] # the number of levels is equal to the number of parentheses.
	assert n == m
	#Convert the ranges in parentheses
	
	start_indices1 = [i for i, x in enumerate(dep1) if x == '(']
	end_indices1   = [i for i, x in enumerate(dep1) if x == ')']		
	start_indices2 = [i for i, x in enumerate(dep2) if x == '(']
	end_indices2   = [i for i, x in enumerate(dep2) if x == ')']
	levels = [dep1[i-1] for i in start_indices1]
	assert len(start_indices1) == len(start_indices2)
	assert len(end_indices1) == len(end_indices2)
	# For every set of parentheses 
	Intersections = []
	for i in range(n):
		range_1 = dep1[start_indices1[i]+1:end_indices1[i]]
		range_2 = dep2[start_indices2[i]+1:end_indices2[i]] # we don't include the parens in these slices
		dont_convert = [',', '-', '|']
		#print 'range_2', range_2
		range_1 = [int(i) if i not in dont_convert else i for i in range_1 ]
		range_2 = [int(i) if i not in dont_convert else i for i in range_2 ]
		loc_of_bar1 = [i for i, x in enumerate(range_1) if x == '|']
		loc_of_bar2 = [i for i, x in enumerate(range_2) if x == '|'] # now we know where the bars are
		# either there are bars, or there are not.
		Intersections.append(do_intersect(range_1, range_2, loc_of_bar1, loc_of_bar2))
	Intersections = finalize_intersect(Intersections, levels)
	return Intersections

def do_intersect(range_1, range_2, loc_of_bar1, loc_of_bar2):
	'''Input is two ranges of values separated with bars and dashes. We have to translate these strings 
	into sets of integers. Then return a set containing the common integers, nicely formatted'''
	ints_1 = set(expand(range_1, loc_of_bar1))
	ints_2 = set(expand(range_2, loc_of_bar2))
	intersect_set = ints_1 & ints_2
	return format_intersect(intersect_set)

def expand(range_N, loc_of_barN):
	'''input the range and the locations of the bars. Then transform the range into a set of integers '''
	expansion = set()
	#print 'range_N', range_N
	if loc_of_barN == []:
		if len(range_N) == 1:
			expansion.add(range_N[0])
		else:
			for i in range(range_N[0], range_N[2] + 1):
				expansion.add(i)
	else:
		start_bars = [-1] + loc_of_barN
		end_bars = loc_of_barN + [len(range_N)]
		for i in range(len(start_bars)):
			range_n = range_N[start_bars[i]+1:end_bars[i]]
			if len(range_n) == 1:
				expansion.add(range_n[0])
			else:
				#print 'range_n[0], range_n[2] + 1', range_n[0], range_n[2] + 1
				for i in range(range_n[0], range_n[2] + 1):
					expansion.add(i)
	return list(expansion)

def format_intersect(intersect_set):
	'''input a set of integers, output the set packaged in parentheses with bars and dashes as it should be. '''
	l_intersect_set = list(intersect_set)
	ranges = []
	for k,g in groupby(enumerate(l_intersect_set), lambda (i,x):i-x):
		ranges.append(map(itemgetter(1), g))
	transformed_ranges = []
	for r in ranges:
		if len(r) == 1:
			transformed_ranges.append(str(r[0]))
		else:
			transformed_ranges.append(''.join([str(r[0]), '-', str(r[-1])]))
	return '|'.join(transformed_ranges)


def finalize_intersect(Intersections, levels): 
	result = []
	for i, lev in enumerate(levels):
		result.append(lev + '(' + Intersections[i] + ')')
	return '[' + '&'.join(result) + ']'

def gen_new_levels(Intersection, Current):
	'''remove the intersection from the current distribution and return the new distributions'''
	# Anything between a '[' or a '&' and a '(' is a level number.
	# anything between '(' and ')'  in a  nongreedy regex is a set of level params.
	# split the level params on '|'
	# Difference = for param in level params if '-' in param RemoveSubset from level else Remove Element.
	# 