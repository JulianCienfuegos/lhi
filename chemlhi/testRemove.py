from Remove import *

dep = '[1(1-4)&2(1-40|100-120|404)&3(1)]'
dep2 = '[1(1-2|4)&2(1-40|105-120|404)&3(1-5)]'
print 'dep',dep
print 'dep2', dep2
print 'int', Intersection(dep, dep2)


level = '2'
a2 = '105'
a3 = '120'
s =  RemoveSubset(dep, level, a2, a3)
print 's', s
level = '1'
a2 = '1'
a3 = '4'
s =  RemoveSubset(dep, level, a2, a3)
print 's', s
level = '1'
a2 = '1'
a3 = '3'
s =  RemoveSubset(dep, level, a2, a3)
print 's', s
o