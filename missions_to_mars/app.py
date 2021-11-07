# Imports 
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scraper

# Create flask instance 
app = Flask(__name__)

mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_db")

# Index/Home route
@app.route("/")
def home():
  mars_dict = mongo.db.mars_dict.find_one()
  
  return render_template("index.html", mars_dict=mars_dict)

# Scraper route 
@app.route("/scrape")
def scrape():
  mars_dict = mongo.db.mars_dict
  mars_dict_scrape = scraper.scrape()
  # Update Mongo
  mars_dict.update({}, mars_dict_scrape, upsert=True)
  # Get redirect
  return redirect('/')

# Initialize app
if __name__ == "__main__":
  app.run(debug=True)