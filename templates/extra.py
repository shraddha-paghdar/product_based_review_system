if request.method == 'POST':
	 	comment = request.form['newcomment']
	 	key = request.form['key']
	 	fieldnames = ['asin', 'reviewText']
	 	with open('addeddata.csv','w') as inFile:
	 		writer = csv.DictWriter(inFIle, fieldnames=fieldnames)
	 		writer.writerow({'asin': key, 'reviewText': comment})
	 	return render_template('DEO.html')


	sample = open('cellphone_15000.csv','r')
	sort = sorted(sample, key=operator.itemgetter(0))
	for eachline in sort:
		print (eachline)