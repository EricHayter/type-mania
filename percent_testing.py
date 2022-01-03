# SOLUTION 1 0:00:00.000480
from collections import Counter
import datetime
start_time = datetime.datetime.now()

s2 = 'qsrqq' 
s1 = 'qqtrr'

common_letters = Counter(s1) & Counter(s2)  # => {'q': 2, 'r': 1}
print()         # => 3

end_time = datetime.datetime.now()
print(end_time - start_time)

from collections import Counter
import datetime
start_time = datetime.datetime.now()

s2 = 'qsrqq' 
s1 = 'qqtrr'

common_letters = Counter(s1) & Counter(s2)  # => {'q': 2, 'r': 1}
print(sum(common_letters.values()))         # => 3

end_time = datetime.datetime.now()
print(end_time - start_time)

start_time = datetime.datetime.now()

s2 = 'qsrqq' 
s1 = 'qqtrr'

common_letters = Counter(s1) & Counter(s2)  # => {'q': 2, 'r': 1}
print(sum(common_letters.values()))         # => 3

end_time = datetime.datetime.now()
print(end_time - start_time)



# SOLUTION 2
start_time = datetime.datetime.now()

s2 = sorted("qsrqq")
s1 = sorted("qqtrr")

count = 0
while len(s1)>0 and len(s2)>0:
    if s1[0] == s2[0]:
        count += 1
        s1 = s1[1:]
        s2 = s2[1:]
    elif s1[0] < s2[0]:
        s1 = s1[1:]
    else:
        s2 = s2[1:]

print(count)

end_time = datetime.datetime.now()
print(end_time - start_time)