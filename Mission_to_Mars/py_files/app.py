from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scrape_mars

# Create an instance of Flask
app = Flask(__name__)

#establish Mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)
# Route to render index.html template using data from Mongo
@app.route("/")
def index():

    # Find one record of data from the mongo database
    mars_dict = mongo.db.mars_dict.find_one()
    # Return template and data
    return render_template("index.html", mars=mars_dict)


# Route that will trigger the scrape function
@app.route("/scrape")
def scrape():

    mars_dict = mongo.db.mars_dict
    # Get the dictionary from the scrape_mars python script
    mars_data = scrape_mars.scrape()

    mars_dict.update({}, mars_data, upsert=True)

    # Redirect back to home page
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)