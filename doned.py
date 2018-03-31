import csv
import operator

def doned(n,a,b,r):
	name=n
	new=a
	ne=b
	rate=r
	fieldnames = ['asin','overall','reviewText','reviewerName']
	with open('cellphone_15000.csv','a') as inFile:
		writer = csv.DictWriter(inFile, fieldnames=fieldnames)
		writer.writerow({'asin': new, 'overall':rate, 'reviewText': ne, 'reviewerName': name})
	sample = open('cellphone_15000.csv','r')
	sort = sorted(sample, key=operator.itemgetter(0))
	for eachline in sort:
		print (eachline)
	return name,new,ne,rate
