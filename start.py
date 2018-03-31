from flask import Flask, redirect, url_for, request, render_template
from test import product_to_review
from doned import doned
import json
import csv

app = Flask(__name__)

@app.route('/index')
def index():
	return render_template('DEMO.HTML')

@app.route('/analyse', methods=['GET', 'POST'])
def analyse():
	if request.method == 'POST':
		ASIN = request.form['ASIN']
		pos, neg, postext, posname, negtext, negname, avg, product_info, plt= product_to_review(ASIN)
		return render_template('index.html', pos=pos, neg=neg, pos_name_text=zip(posname,postext), neg_name_text=zip(negname,negtext), avg=avg ,product_info=product_info, asin=ASIN)

@app.route('/done', methods=['GET','POST'])
def done():
	if request.method == 'POST':
		name = request.form['u_name']
		comment = request.form['newcomment']
		key = request.form['key']
		rate = request.form['rate']
		n,a,b,r=doned(name,key,comment,rate)
		return render_template('DEO.html',name=n, key=a, c=b,r=r)

if __name__ == '__main__':
   app.run(debug = True)