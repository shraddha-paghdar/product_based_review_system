import re
import os
import csv
import json
import pygal
from pygal.style import Style
import matplotlib.pyplot as plt

custom_style = Style(
  tooltip_font_size='1000',
  title_font_size='100',
  value_label_font_size='100',
  value_font_size='100',
  major_label_font_size='100',
  label_font_size='100'
)

# Load the necessary files into variables
with open('dataset.json', 'r') as fp:
    dataset = json.load(fp)

with open('feature_set.json', 'r') as fp:
    feature_set = json.load(fp)
    
with open('no_of_items.json', 'r') as fp:
    no_of_items = json.load(fp)


def calc_prob(word, category):

	if word not in feature_set.keys() or word not in dataset[category].keys():
		print("Not found: ", word)
		return 0

	return float(dataset[category][word])/no_of_items[category]


# Weighted probability of a word for a category
def weighted_prob(word,category):
	# basic probability of a word - calculated by calc_prob
	basic_prob=calc_prob(word,category)

	# total_no_of_appearances - in all the categories
	if word in feature_set:
		tot=sum(feature_set[word].values())
	else:
		tot=0
		
	# (weight*assumedprobability + total_no_of_appearances*basic_probability)/(total_no_of_appearances+weight)
	# weight by default is taken as 1.0
	# assumed probability is 0.5 here
	weight_prob=((1.0*0.5)+(tot*basic_prob))/(1.0+tot)
	return weight_prob


# To get probability of the test data for the given category
def test_prob(test,category):
	# Split the test data
	split_data=re.split('[^a-zA-Z][\'][ ]',test)
	
	data=[]
	for i in split_data:
		if ' ' in i:
			i=i.split(' ')
			for j in i:
				if j not in data:
					data.append(j.lower())
		elif len(i) > 2 and i not in data:
			data.append(i.lower())

	p=1
	for i in data:
		p*=weighted_prob(i,category)
	return p


# Naive Bayes implementation
def naive_bayes(test):
	'''
		p(A|B) = p(B|A) * p(A) / p(B)
		Assume A - Category
			   B - Test data
			   p(A|B) - Category given the Test data	'''
	results={}
	for i in dataset.keys():
		# Category Probability
		# Number of items in category/total number of items
		cat_prob=float(no_of_items[i])/sum(no_of_items.values())

		# p(test data | category)
		test_prob1=test_prob(test,i)

		results[i]=test_prob1*cat_prob

	return results


def product_to_review(ASIN):
	positive = 0 #initialize positive comments counter
	negative = 0 #initialize negative comments counter
	counter = 0 # for counting number of reviews for a particular product
	overall= 0 #for overall review
	names='positive', 'negative',
	
 	# Create a circle for the center of the plot
	my_circle=plt.Circle( (0,0), 0.7, color='white')
	i=0
	j=0
	postext=[]
	negtext=[]
	posname=[]
	negname=[]
	cellphone_read=open("cellphone_15000.csv" , 'r') #open csv file to test the model
	reader = csv.reader(cellphone_read) #read the csv file 
	rows = [row for row in reader if row[0] == ASIN] #store only those rows whoes entered ASIN number is same as asin number in csv file
	counter = len(list(rows)) #counting total number of reviews for a entered product
	for read in rows: #read those rows whos ASIN number is matched
		try:		
			text=read[2] #read only review text column from csv file
			result=naive_bayes(text) #give the comment to function
			user_name=read[3]
			if result['1'] > result['-1']:
				positive += 1 #increment the positive counter if comment is positive\
				postext.append(text)	
				posname.append(user_name)
			else:
				negative += 1 #increment the negative counter if comment is negative
				negtext.append(text)
				negname.append(user_name)
			overall_review = read[1]
			overall += float(overall_review) 
			average_review = overall/counter
		except IndexError as e:
			print()
	product_info_read=open('product_info.csv' , 'r')
	product_info_reader=csv.reader(product_info_read)
	for i in product_info_reader:
		if i[0] == ASIN:
			product_info=i[1]

	size=[positive,negative]
	# plt.rcParams['text.color'] = 'red'
	# plt.pie(size, labels=names, wedgeprops = { 'linewidth' : 7, 'edgecolor' : 'white' })
	# p=plt.gcf()
	# p.gca().add_artist(my_circle)
	# plt.show()
	style=pygal.style.styles['default'](value_font_size=80),
	pie_chart = pygal.Pie(inner_radius=.69)
	pie_chart.add('Positive', positive)
	pie_chart.add('Negative', negative)
	pie_chart.render_to_file("static/img/p_chart.svg")

	return positive, negative,postext,posname,negtext,negname,average_review,product_info,plt
	
			
# print ('Enter the sentence')
# text=input()
# result=naive_bayes(text)

# if result['1'] > result['-1']:
# 	print ('positive')
# else:
# 	print ('negative')
