import re
import csv
import json

fh=open("dataset.csv","r")
reader = csv.reader(fh, delimiter='+')

dataset={}
no_of_items={}
feature_set={}

for row in reader:
	# print(row)
	no_of_items.setdefault(row[1],0)
	# print(no_of_items)
	no_of_items[row[1]]+=1
	# print(no_of_items)
	dataset.setdefault(row[1],{})
	# print(dataset)
	split_data=re.split('[^a-zA-Z\']',row[0])
	
	for i in split_data:
		# print("break")
		if len(i) > 2: #removing unnecessary words that are less than 2 characters
			dataset[row[1]].setdefault(i.lower(),0)
			# +print(dataset)
			dataset[row[1]][i.lower()]+=1  # Increase the word count on its occurence with label row[1]
			# print(dataset)
			feature_set.setdefault(i.lower(),{})   # Initialze a dictionary for a newly found word in feature set
			# print(feature_set)
			feature_set[i.lower()].setdefault(row[1],0)
			# print(feature_set)
			feature_set[i.lower()][row[1]]+=1 # Increment the count for the word 
			# print(feature_set)

with open('dataset.json', 'w') as fp:
    json.dump(dataset, fp)

with open('feature_set.json', 'w') as fp:
    json.dump(feature_set, fp)

with open('no_of_items.json', 'w') as fp:
    json.dump(no_of_items, fp)