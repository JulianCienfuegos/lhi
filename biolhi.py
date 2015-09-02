import sys
import copy
import pprint
import itertools

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

def remove_dists(level_vals):
	dependencies = [val.split(' ')[0] for val in level_vals]
	return dependencies

def verify_level(dependencies):
	''' this function gathers all of the distinct values present across all of the dependency strings. Then it
	constructs the cartesian product, and for each element in the cartesian product, it verifies that this element
	is in one of the dependency strings of the level. '''
	# How many subsets in any entry in dependencies?
	dep = dependencies[0]
	dep_split = [i.split(',') for i in dep.split('-')]
	n = len(dep_split)
	distinct = [set() for i in range(n)]

	# Gather all of the distinct values in the level.
	for val in dependencies: # split the val into the different pieces.
		dep_split = [i.split(',') for i in val.split('-')]
		for i in range(len(dep_split)):
			for d in dep_split[i]:
				distinct[i].add(d)
	distinct = [list(s) for s in distinct]
	distinct = [sorted(s) for s in distinct]
	#print distinct

	# construct the cartesian product
	cart_prod = []
	for element in itertools.product(*distinct):
		cart_prod.append(list(element))
	cart_prod = ['-'.join(cp) for cp in cart_prod]
	#pprint.pprint(cart_prod)
	
	#remove elements one by one from dependencies. We should be left with an empty list when we reach the end of the cart_prod
	remaining = unshared_copy(dependencies)
	
	for cp in cart_prod:
		cp = cp.split('-')
		for i in remaining:
			is_sub = 0
			i_list = i.split('-')
			i_list = [j.split(',') for j in i_list]
			for j in range(len(i_list)):
				if cp[j] in i_list[j]:
					is_sub += 1
			if is_sub == len(i_list):
				#print 'cp, i_list', cp, i_list
				break
		if is_sub == 0:
			print cp
			sys.exit('There is an error in the level verification step.')


if __name__ == '__main__':
	level1 = '1,2-4,5-7,8,9,10 olddist1'
	level2 = '1,2-6-7,8,9,10 olddist2'
	level3 = '3-4,5,6-7,8,9 olddist3'
	level4 = '3-4,5,6-10 olddist4'
	level_vals = [level1, level2, level3, level4]

	new_dist = '2,3-5,6-7,9,10 newdist'
	change_level(level_vals, new_dist)
	pprint.pprint(level_vals)
	verify_level(remove_dists(level_vals))


	level1 = '1,2,3,4 old1'
	level2 = '5,6,7,8 old2'

	level_vals = [level1, level2]
	new_dist = '4,9 new'
	change_level(level_vals, new_dist)
	pprint.pprint(level_vals)
	verify_level(remove_dists(level_vals))