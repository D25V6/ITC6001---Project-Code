import hyperloglog
import math
import os
import json
import pympler
from pympler import asizeof
import re
import numpy as np

# create HyperLogLog objects with given accuracy
hll = hyperloglog.HyperLogLog(0.01)
hll2 = hyperloglog.HyperLogLog(0.01)

# Creation of empty lists 
list = []
list2 = []
tags = []

# First Approach Function Users
def count_users(my_list):    
    freq = {x: 0 for x in my_list}
    for items in my_list:
        freq[items] = freq[items] + 1
        
    # Print results

    for key, value in freq.items():
        print("User with id: % d has % d tweet(s)" % (key, value))

# First Approach Function Hashtags
def count_hashtags(my_list):    
    freq = {x: 0 for x in my_list}
    for items in my_list:
        freq[items] = freq[items] + 1
        
     # Print results

    for key, value in freq.items():
        print("Hashtag: % s has % d appearances" % (key, value))

# Importing files
for file in os.scandir('C:/Python/twitter_world_cup_1m/'):
    with open(file, 'r', encoding='utf8') as f:
        for line in open(file, 'r', encoding='utf8'):
            data = json.loads(line)

            # Finding the user's ids
            list.append(data['user']['id'])
            
            # Finding the hashtags
            list2 = re.findall("\'text\': \'\\w+\'", str(data))
            if list2:
                hashtags = str(list2).strip('[]')
                hashtags2 = re.findall(r"[\w]+", hashtags)
                htags = [x for x in hashtags2 if x != 'text']
                if htags is not None:
                    for i in htags:                        
                        tags.append(i)
                        
            data.clear()
        f.close()
    f.close()
    
result = count_users(list)
print('The user results are: \n', result)
result2 = count_hashtags(tags)
print('The hashtags results are: \n', result2)

# Creation of empty user dictionary
d = {}
for i in list:
    if i not in d:
        d[i] = 1
    else:
        d[i] += 1
    hll.add(str(i))

# Creation of empty hahstags dictionary
ht = {}
for i in tags:
    if i not in ht:
        ht[i] = 1
    else:
        ht[i] += 1
    hll2.add(str(i))
    
print('Actual list Cardinality: {0}'.format(list))
print('Actual Cardinality of user dictionary:', len(d))
print('Estimated Cardinality of user hll: {0}'.format(math.ceil(hll.card())))

print('Actual list Cardinality: {0}'.format(tags))
print('Actual Cardinality of hashtag dictionary:', len(ht))
print('Estimated Cardinality of hashtag hll: {0}'.format(math.ceil(hll2.card())))



# Reporting the absolute error

ae = np.abs(math.ceil(hll.card()) - len(d))
ae2 = np.abs(math.ceil(hll2.card()) - len(ht))


print('The absolute error between user dictionary and hll is: ', ae)
print('The aabsolute error between hashtag dictionary and hll is: ', ae2)


# Reporting on the size of each object
print('The size of user dict is: %d bytes,while the size of hll is: %d bytes'%pympler.asizeof.asizesof(d,hll))

print('\nThe size of hashtag dict is: %d bytes,while the size of hll is: %d bytes'%pympler.asizeof.asizesof(ht,hll2))
