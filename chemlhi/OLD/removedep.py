from RemoveDependency import *


old_dep = '[1(1-13)&4(1-4|6|10-12)]'
level = '4'
value = '6'
dep = RemoveDependency(old_dep, level, value)
print 'old_dep, level, value, new_dep:', old_dep, level, value, dep
level = '1'
value = '6'
dep = RemoveDependency(old_dep, level, value)
print 'old_dep, level, value, new_dep:', old_dep, level, value, dep
level = '1'
value = '1'
dep = RemoveDependency(old_dep, level, value)
print 'old_dep, level, value, new_dep:', old_dep, level, value, dep
level = '4'
value = '12'
dep = RemoveDependency(old_dep, level, value)
print 'old_dep, level, value, new_dep:', old_dep, level, value, dep