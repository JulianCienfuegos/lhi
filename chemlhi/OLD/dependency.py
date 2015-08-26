"""
This code will rewrite a dependency such that a certain level is removed.

There are 16 distinct ways we can find a number n, n_0 < n < n_1 in the sequence of values in a given level.

Column1      Column2            Column3          Column4
(n),         (n_0-n_1),         (n-n_1),         (n_0-n)
(n|...),     (n_0-n_1|...),     (n-n_1|...),     (n_0-n|...)
(...|n),     (...|n_0-n_1),     (...|n-n_1),     (...|n_0-n)
(...|n|...), (...|n_0-n_1|...), (...|n-n_1|...), (...|n_0-n|...)

Case Column1: we have no leftover dependencies.
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
"""

class RemoveDependency:
	def __init__(self, s, level, value):
		self.s = s
		self.new_s = ''
		self.new_dependency = self.RemoveValue(self.new_s, level, value)
		
	def SplitString(self):
		"""
		This function will split a string in a way useful to us.
		We first split the string.
		Then, the numbers that are longer than one digit will be split in two!
		So we rejoin them.
		We find all characters occurring between one special character and the next special character that immediately appears.
			'(' is always followed by '-' or ')'
			'-' is always followed by '|' or ')'
			'|' is always followed by '-' or ')'
		THE SOLE PURPOSE OF THIS FUNCTION IS TO GROUP EVERY TERM IN A DEPENDENCY STRUCTURE BY ITSELF IN A LIST. In this
		function, a GROUP is a set of numeric characters which occur between a key in 'd' and one of it's values.
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
		
	def col3(subl):
		"""
		This function handles the case when when our number of interest is one of the lower bounds of the range.
		The reasoning is similar to the reasoning presented in the docstring for the col2 function.
		"""
		if subl[i+1] == str(int(sub[i-1]) + 1):
			subl[i-1:i+2] = subl[i+1] # remove the range and replace with the single remaining value.
		else:
			subl[i-1:i+2] = [str(int(sub[i-1]) + 1), '-', subl[i+1]]
		return subl

	def col4(subl):
		"""
		This function handles the case when the number of interest is the upper bound of some range, as is the 
		case in column 4 above. The reasoning here is similar to the reasoning in the col2 function.
		"""
		if subl[i-1] == str(int(sub[i+1]) - 1):
			subl[i-1:i+2] = subl[i-1] # remove the range and replace with the single remaining value.
		else:
			subl[i-1:i+2] = [sub[i-1], '-', str(int(sub[i+1]) - 1)]
		return subl
		
		
	def RemoveValue(new_s, level, value):
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
			n = len(new_s)
			for i in range(1, n):	
				if new_s[i] == '(' and new_s[i-1] == level:
					start_of_sub = i
					end_of_sub = new_s[i:].index(')') + i
					subl = new_s[start_of_sub:end_of_sub]
					m = len(subl)
					for i in range(1,m-1):
						print subl[i-1], subl[i], subl[i+1]
						if subl[i] == value and (( subl[i-1]=='(' and subl[i+1] == ')') or (subl[i-1]=='(' and subl[i+1] == '|') or (subl[i-1]=='|' and subl[i+1] == ')') or (subl[i-1]=='|' and subl[i+1] == '|')):
							print('col1')
							return '' # case column 1
							break
						if subl[i] == '-' and int(subl[i-1]) < int(value) and int(subl[i+1]) > int(value):
							print('col2')
							print subl[i-1], subl[i], subl[i+1]
							subl = col2(subl, value, i)
							break
						if subl[i] == '-' and subl[i-1] == value and int(subl[i+1]) > int(value):
							print('col3')
							subl = col3(subl, value, i)
							break
						if subl[i] == '-' and int(subl[i-1]) < int(value) and subl[i+1] == value:
							print('col4')
							subl = col4(subl, value, i)
							break
					new_s[start_of_sub:end_of_sub] = subl
					break
			s = ''.join(new_s)
			return s