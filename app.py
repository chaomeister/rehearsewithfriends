from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
import jinja2
import os
import datetime

app = Flask(__name__)
dbclient = MongoClient("mongodb://chao:rehearsewithfriends1@ds049094.mlab.com:49094/rehearsewithfriendsdb")
db = dbclient.get_default_database()
people = db.People


@app.route('/', methods=['GET'])
def hello():
	deleteFinishedRehearsals()
	if request.args.get("error") is not None:
		return render_template("index.html",people=people.find(),error=request.args.get("error"))
	return render_template("index.html",people=people.find())

def deleteFinishedRehearsals():
	allPeople = people.find()
	curr_time = datetime.datetime.now().time()
	for person in allPeople:
		end_time = datetime.datetime.strptime(person["etime"], "%H:%M").time()
		if curr_time > end_time:
			people.delete_one({'_id':person['_id']})

@app.route('/add', methods=['POST'])
def add():
	name = request.form.get("name")
	location = request.form.get("location")
	stime = request.form.get("stime")
	etime = request.form.get("etime")
	if name == "" or location == "":
		return redirect(url_for('.hello', error="Please completely fill out the form."))
	try: 
		datetime.datetime.strptime(stime, "%H:%M").time()
		datetime.datetime.strptime(etime, "%H:%M").time()
	except ValueError:
		return redirect(url_for('.hello', error="Please enter correctly formatted times."))
	people.insert_one(
		{
		"name":name,
		"location":location,
		"stime":stime,
		"etime":etime
		})
	return redirect('/')

if __name__ == '__main__':
	port = int(os.environ.get('PORT', 8000))
	app.run(host='0.0.0.0', port=port,debug=True)