# Imports 
from flask import Flask, render_template, redirect
from pymongo.mongo_client import MongoClient
import scraper 

app = Flask(__name__) 

client = MongoClient("mongodb://localhost:27017")

mars_db = client['mars_db']

facts_collection = mars_db.facts_collection


@app.route("/")
def home():
  try:
    facts_data = facts_collection.find().sort('_id', -1).limit(1)[0]
  except:
    return redirect("/scrape")
  return render_template("index.html", mars_dict=facts_data)

# Scraper route
@app.route("/scrape") 
def scrape(): 
  item = scraper.scrape()
  facts_collection.insert_one(item)
  return redirect("/")

if __name__ == "__main__":
  app.run(debug=True)