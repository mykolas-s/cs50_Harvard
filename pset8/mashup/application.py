import os
import re
from flask import Flask, jsonify, render_template, request

from cs50 import SQL
from helpers import lookup

# Configure application
app = Flask(__name__)

# Configure CS50 Library to use SQLite database
db = SQL("sqlite:///mashup.db")

# Ensure responses aren't cached
@app.after_request
def after_request(response):
    response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
    response.headers["Expires"] = 0
    response.headers["Pragma"] = "no-cache"
    return response


@app.route("/")
def index():
    """Render map"""
    return render_template("index.html")

# We are looking up in Google's (or Onion's) RSS feed, and returning RSS feed items
# (i.e. information about each article in location, determined by postal code, which
# is stored in 'geo'). In that information there is article's name and link for it. 
# We JSON'ifying this info - i.e. converting it to JSON format and return it.
@app.route("/articles")
def articles():
    """Look up articles for geo"""

    geo = request.args.get("geo")
    if (geo == ""):
        raise RuntimeError('missing geo')

    # lookup for articles
    articles = lookup(geo)

    # return JSON of articles
    return jsonify(articles)


@app.route("/search")
def search():
    """Search for places that match query"""
    q = request.args.get("q")

    if len(q.split(",")) == 1:
        rows = db.execute("""SELECT * FROM places WHERE
        postal_code LIKE :q0 OR place_name LIKE :q0 OR
        admin_name1 LIKE :q0 OR admin_code1 LIKE :q0 OR
        admin_name2 LIKE :q0 OR admin_code2 LIKE :q0 OR
        admin_name3 LIKE :q0 OR admin_code3 LIKE :q0
        """, q0=q.capitalize() + "%")

    elif len(q.split(",")) == 2:
        rows = db.execute("""SELECT * FROM places WHERE
        (place_name LIKE :q1 AND admin_code1 LIKE :q2) OR
        (place_name LIKE :q1 AND admin_name1 LIKE :q2)
        """, q1=q.split(', ')[0].capitalize() + "%", q2=q.split(', ')[1].capitalize() + "%")

    elif len(q.split(",")) == 3:
        rows = db.execute("""SELECT * FROM places WHERE
        place_name LIKE :q1 AND admin_name1 LIKE :q2 AND country_code LIKE :q3
        """, q1=q.split(', ')[0].capitalize() + "%", q2=q.split(', ')[1].capitalize() + "%", q3=q.split(', ')[2].capitalize() + "%")

    return jsonify(rows)


@app.route("/update")
def update():
    """Find up to 10 places within view"""

    # Ensure parameters are present
    if not request.args.get("sw"):
        raise RuntimeError("missing sw")
    if not request.args.get("ne"):
        raise RuntimeError("missing ne")

    # Ensure parameters are in lat,lng format
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("sw")):
        raise RuntimeError("invalid sw")
    if not re.search("^-?\d+(?:\.\d+)?,-?\d+(?:\.\d+)?$", request.args.get("ne")):
        raise RuntimeError("invalid ne")

    # Explode southwest corner into two variables
    sw_lat, sw_lng = map(float, request.args.get("sw").split(","))

    # Explode northeast corner into two variables
    ne_lat, ne_lng = map(float, request.args.get("ne").split(","))

    # Find 10 cities within view, pseudorandomly chosen if more within view
    if sw_lng <= ne_lng:

        # Doesn't cross the antimeridian
        rows = db.execute("""SELECT * FROM places
                          WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude AND longitude <= :ne_lng)
                          GROUP BY country_code, place_name, admin_code1
                          ORDER BY RANDOM()
                          LIMIT 10""",
                          sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    else:

        # Crosses the antimeridian
        rows = db.execute("""SELECT * FROM places
                          WHERE :sw_lat <= latitude AND latitude <= :ne_lat AND (:sw_lng <= longitude OR longitude <= :ne_lng)
                          GROUP BY country_code, place_name, admin_code1
                          ORDER BY RANDOM()
                          LIMIT 10""",
                          sw_lat=sw_lat, ne_lat=ne_lat, sw_lng=sw_lng, ne_lng=ne_lng)

    # Output places as JSON
    return jsonify(rows)
