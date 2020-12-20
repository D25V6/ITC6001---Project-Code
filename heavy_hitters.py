# Importing the appropriate libraries
import json
import os
import csv
import probables
import pympler
from pympler import asizeof
import re
import numpy as np
import math

# Creatting empty list and counter for the 1000 data points
b = 0
list1 = []
list2 = []
list3 = []
tags = []
tags2 =[]
# First Function: To list the users every 1000 lines

def count(my_list): 
    freq = {x: 0 for x in my_list}
    for items in my_list:
        freq[items] = freq[items] + 1

    # The frequency dictionary is sorted and printed as a tuple

    tuples_list = sorted(freq.items(), reverse=True, key=lambda x: x[1])
    for elem in tuples_list:
        if elem[1] > n:
            print("User with id:", elem[0], "appears::", elem[1])

# Second Function: To list the hashtags every 1000 lines

def count_tags(my_list): 
    freq = {x: 0 for x in my_list}
    for items in my_list:
        freq[items] = freq[items] + 1

    # The frequency dictionary is sorted and printed as a tuple

    tuples_list = sorted(freq.items(), reverse=True, key=lambda x: x[1])
    for elem in tuples_list:
        if elem[1] > n:    
            print("Hashtags:", elem[0], "appears::", elem[1])
        
# Third Function: To export user results at the end of stream as a csv

def final_count_users(my_list):
    freq = {x: 0 for x in my_list}
    for items in my_list:
        freq[items] = freq[items] + 1
        
    # Counts saved in csv
    with open('user-counter.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames =["User_ID", "Frequency"])
        writer.writeheader()
        for key in freq.keys():
            f.write("%s,%s\n" % (key, freq[key]))
    f.close()

# Fourth Function: To export hahstags results at the end of stream as a csv

def final_count_hashtags(my_list):
    freq = {x: 0 for x in my_list}
    for items in my_list:
        freq[items] = freq[items] + 1
     
     # Counts saved in csv
    with open('hashtags-counter.csv', 'w') as f:
        writer = csv.DictWriter(f, fieldnames =["Hashtags", "Frequency"])
        writer.writeheader()
        for key in freq.keys():
            f.write("%s,%s\n" % (key, freq[key]))
    f.close()

# Providing path for the json files

for file in os.scandir('C:/Python/twitter_world_cup_1m/'):
    with open(file, 'r', encoding='utf8') as f:
        for line in open(file, 'r', encoding='utf8'):
            data = json.loads(line)
            b += 1

            # Finding the user's ids

            list1.append(data['user']['id'])
            list2.append(data['user']['id'])

            # Finding the hashtags

            list3 = re.findall("\'text\': \'\\w+\'", str(data))
            if list3:
                hashtags = str(list3).strip('[]')
                hashtags2 = re.findall(r"[\w]+", hashtags)
                htags = [x for x in hashtags2 if x != 'text']
                if htags is not None:
                    for i in htags:
                        
                        tags.append(i)
                        tags2.append(i)

            # Printing every 1000 points


            if b == 1000:
                b = 0
                n = int(input("Enter threshold for the users: "))
                print("The user heavy hitters are:\n")
                print(count(list2))
                list2.clear()
                n = int(input("Enter threshold for the hashtags: "))
                print('The hashtags Heavy Hitters are:\n')
                print(count_tags(tags2))
                tags2.clear()                       
            data.clear()
        f.close()
    f.close()


#End of stream
result1 = final_count_users(list1)
result2 = final_count_hashtags(tags)

# Creation of empty dictionary 
d = {}
d2 = {}
# Creation of cms object
cms = probables.CountMinSketch(width=600000, depth=5)
cms2 = probables.CountMinSketch(width=100000, depth=5)

# Adding of list items in user dictionary and cms
for i in list1:
    if i not in d:
        d[i] = 1
    else:
        d[i] += 1
    a = str(i)
    cms.add(a)

# Adding of list items in hashtag dictionary and cms
for i in tags:
    if i not in d2:
        d2[i] = 1
    else:
        d2[i] += 1
    a = str(i)
    cms2.add(a)



# Reporting the user counters for the exact and approximate counts
absolute = []
absolute2 = []
square1=[]
square2= []

print('Exact/approx counters')
for (k, v) in d.items():
    print('{0}: {1:3d}/{2}'.format(k, v, cms.check(str(k))))
    absolute.append(np.abs(cms.check(str(k)) - v))
    square1.append((cms.check(str(k)) - v)**2)

# Reporting the hashtag counters for the exact and approximate counts

print('Exact/approx counters')
for (k, v) in d2.items():
    print('{0}: {1:3d}/{2}'.format(k, v, cms2.check(str(k))))
    absolute2.append(np.abs(cms2.check(str(k)) - v))
    square2.append((cms2.check(str(k)) - v)**2)

# Finding and printing Mean Absolute Error and square root mean error
def mae(list):
    total = 0
    for ele in range(0, len(list)):
        total = total + list[ele]
    return total/len(list)

print('The mean absolute error between user dictionary and cms is: ', mae(absolute))
print('The mean absolute error between hashtag dictionary and cms is: ', mae(absolute2))

def rmse(list):
    total = 0
    for ele in range(0, len(list)):
        total = total + list[ele]
    return math.sqrt(total / len(list))

print('The root mean square error between user dictionary and cms is: ', rmse(square1))
print('The root mean square error between hashtag dictionary and cms is: ', rmse(square2))

# Reporting on the size of each object in bytes
print('The size of user dictionary is: %d bytes,while the size of cms is: %d bytes'% pympler.asizeof.asizesof(d,cms))
print('The size of hashtag dictionary is: %d bytes,while the size of cms2 is: %d bytes'% pympler.asizeof.asizesof(d2,cms2))
