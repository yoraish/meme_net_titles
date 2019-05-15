# THIS script will be used to convert database data to workable template
# it will take in the database, and output:

# * a json object mapping words to their index in the frequency list
# * a json object mapping each frequency list to a score (0,3)

import json
from math import log
import matplotlib.pyplot as plt
import numpy as np
import os

def vis(dict, heading):
    plt.figure(0)
    lst = sorted([i for i in dict.values()])

    plotting_bins=np.arange(0,10,1) # need to add an extra bin when plotting 
    plt.hist(lst, bins=plotting_bins)
    plt.title(heading)
    plt.show()

def title_to_freq(title):
    pass


words = {} #" maps words to the number of times seen"
title_to_ups = {}

srt_lst = []
with open("../db.json") as db:
    data = json.load(db)
    for i in range(1,len(data['_default'])):
        title = data['_default'][str(i)]['title'].lower()
        ups = data['_default'][str(i)]['ups']
        ups = round(log(ups,4))-5
        if ups < 0:
            ups = 0
        if ups > 3:
            ups = 3
        title_to_ups[title] = ups # <----------------maybe log scale here

        # find the words in the title
        wlst = title.split()
        # put in words dict
        for w in wlst:
            if w in words.keys():
                words[w]+= 1
            else:
                words[w] = 1

to_rem = []
for word, count in words.items():
    if count < 4:
        to_rem.append(word)

'''
# can take out words that are redundant, but this is tricky becasue it will result in count_lst collisions later
'''
to_rem += ['it','a', 'the', 'to', 'is', 'this',')']
for word in to_rem:
    words.pop(word)

num_words = len(words)

# create the dictionary that maps words to index at count list
word_to_ix = {}
ix = 0
for word in words.keys():
    word_to_ix[word] = ix
    ix +=1



# save to json file
with open('word_to_ix.json', 'w') as json_file:  
    json.dump(word_to_ix, json_file)

# now create the actual data:
# dctionary mapping a count list to a score (0,3)

scores = {}
for title,score in title_to_ups.items():
    # initialize an empty count list
    count_lst = [0]*num_words
    # split to words
    word_lst = title.split()
    # go through each word and, if exists in our dict, add 1 to correspoinding bin
    for word in word_lst:
        if word in word_to_ix:
            ix = word_to_ix[word]
            count_lst[ix] += 1
    
    if tuple(count_lst) in scores:
        print('collision, existing score = ', scores[tuple(count_lst)], " new score = ", score, 'of title==' , title)
    scores[tuple(count_lst)] = score

# clean up, if any empty data points, take them out
empty = tuple([0]*num_words)
to_rem = []
for count_lst, score in scores.items():
    if count_lst == empty:
        to_rem.append(count_lst)
for rem in to_rem:
    print('removing empty with score', score)
    scores.pop(count_lst)

# convert the tuples to strings
string_scores = {}
for count, score in scores.items():
    string_scores[str(count)] = score

print(len(title_to_ups))
print(len(scores))
print(len(string_scores))
# save the db
vis(scores,'hi')

# save to json file
with open('overall.json', 'w') as json_file:  
    json.dump(string_scores, json_file)

# 85% to train
# sort the thing
srtd = sorted(string_scores.items(), key=lambda x: x[1])
counter = 0
test_data = {}
train_data = {}

for tup in srtd:
    # if multiple of 4 - put in test
    # else put in train
    count_lst = tup[0]
    score = tup[1]
    if counter%9 == 0:
        test_data[count_lst] = score
    else:
        train_data[count_lst] = score
    counter +=1


# save the dict as a json file
with open('train_db.json', 'w') as json_file:  
    json.dump(train_data, json_file)
    vis(train_data, 'train')

with open('test_db.json', 'w') as json_file:  
    json.dump(test_data, json_file)
    vis(test_data,'test')

print('num_words=', num_words, len(word_to_ix))
