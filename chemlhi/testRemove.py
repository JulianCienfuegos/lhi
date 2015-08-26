from Remove import *

dep = '[1(1-4)&2(1-40|100-120)&3(1)]'
level = '2'
a2 = '105'
a3 = '120'
s =  RemoveSubset(dep, level, a2, a3)
print s
level = '1'
a2 = '1'
a3 = '4'
s =  RemoveSubset(dep, level, a2, a3)
print s
level = '1'
a2 = '1'
a3 = '3'
s =  RemoveSubset(dep, level, a2, a3)
print s
