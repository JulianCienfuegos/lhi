import sys
import copy
import pprint

def change_level(level_vals, new):
	'''Input is a copy of the dep_dist strings for a given level and a new dep_dist string.'''
	for row in level_vals:
		new_dist = separate_dep_dist(new)[1]
		row_dist = separate_dep_dist(row)[1]
		if new_dist != row_dist: # Then we may want to make a change
			intersection = intersect(row, new) # Calculate how much they have in common
			if intersection != '': # Then they have some things in common
				deps = diff(intersection, row) # Break the row up into pieces.
				assert deps[0] == intersection
				i = level_vals.index(row)
				level_vals[i:i+1] = deps # replace the row we found with the pieces we just made.
				change_level(level_vals, new) # Try again.
				break

def separate_dep_dist(line):
	return line.split(' ')[0], line.split(' ')[1] # I think the dep and dist are split on a space

def intersect(d1, d2): 
	""" 
	This function will get the intersection of two dependencies.
	The intersection is non-empty iff there is a non-empty overlap between each of the levels.
	e.g.
	1-2-3 and 1-2-4 do not intersect. This function will return ''
	but 
	1-2-3 does intersect 1,2,3,4,5-1,2,3-3,4,5 so the function will return '1-2-3'
	"""
	dep1, dist1 = separate_dep_dist(d1)
	dep2, dist2 = separate_dep_dist(d2)
	dep1_split = [i.split(',') for i in dep1.split('-')]
	dep2_split = [i.split(',') for i in dep2.split('-')]
	n = len(dep1_split); m = len(dep2_split)
	assert n == m
	intersection = [[] for i in range(n)]
	for i in range(n):
		has_intersection = 0
		for d in dep1_split[i]: 		
			if d in dep2_split[i]:
				has_intersection = 1
				intersection[i].append(d)
		intersection[i] = [int(n) for n in intersection[i]] 
		intersection[i].sort()
		intersection[i] = [str(n) for n in intersection[i]] 
		if has_intersection == 0:
			intersection = ''
			return intersection
	return '-'.join([','.join(l) for l in intersection]) + ' ' + dist2

def make_line(a, b, c, i, dist2):
	"""
	a = 1,2,3-4,5,6-8,11
	b = 1-5,6-11
	difference = 2,3-4-8
	line i looks like:
		b[0:i] + '-' + c[i] + '-' + a[i+1:end] + ' ' + dist2
	"""
	if len(c) == 1: # the case in which there is only one  level of
		return(',').join(c[0]) + ' ' + dist2
	if i == 0 and c[0] != []:
		return (',').join(c[0]) + '-' + ('-').join([(',').join(j) for j in a[1:]]) + ' ' + dist2
	elif i == len(a)-1 and c[i] != []:
		return ('-').join([(',').join(j) for j in b[0:i]]) + '-' + (',').join(c[i]) + ' ' + dist2
	elif c[i] != []:
		return ('-').join([','.join(j) for j in b[0:i]]) + '-' + (',').join(c[i]) + '-' + ('-').join([(',').join(j) for j in a[i+1:]]) + ' ' + dist2
	else:
		return ''

def unshared_copy(l):
	""" Just doing L = l will not give an unshared copy of a list of lists. """
	L = []
	for i in l:
		L.append(i[:])
	return L


def diff(new, old):
	"""
	Decide whether or not the dependency in new is a subset of the dependency in line 2
	return the boolean isSub and a list of dependency strings called deps. deps contains 
	new, followed by all of the different subsets in the difference of old and new.
	Every string in deps contains a dependency string and an associated distribution.
	"""
	dep1, dist1 = separate_dep_dist(new)
	dep2, dist2 = separate_dep_dist(old)
	dep1_split = [i.split(',') for i in dep1.split('-')]
	dep2_split = [i.split(',') for i in dep2.split('-')]
	assert len(dep1_split) == len(dep2_split)
	difference = unshared_copy(dep2_split)
	n = len(dep1_split)
	for i in range(n):
		try:
			for j in dep1_split[i]:
				difference[i].remove(j)
		except:
			deps = []
			return deps
	# Now to construct deps!
	deps = []
	deps.append(new)
	for i in range(n):
		new_dep = make_line(dep2_split, dep1_split, difference, i, dist2)
		if new_dep != '':
			deps.append(new_dep)
	return deps


def verify_level(level_vals):
	''' this function gathers all of the distinct values present across all of the dependency strings. Then it
	constructs the cartesian product, and for each element in the cartesian product, it verifies that this element
	is in one of the dependency strings of the level. '''

if __name__ == '__main__':
	level1 = '1,2-4,5-7,8,9,10 olddist1'
	level2 = '1,2-6-7,8,9,10 olddist2'
	level3 = '3-4,5,6-7,8,9 olddist3'
	level4 = '3-4,5,6-10 olddist4'

	level_vals = [level1, level2, level3, level4]

	new_dist = '2,3-5,6-7,9,10 newdist'
	change_level(level_vals, new_dist)
	pprint.pprint(level_vals)

	level1 = '1,2,3,4 old1'
	level2 = '5,6,7,8 old2'

	level_vals = [level1, level2]
	new_dist = '4,9 new'
	change_level(level_vals, new_dist)
	pprint.pprint(level_vals)