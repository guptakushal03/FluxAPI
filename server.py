import datetime
import json
import random
import re

import requests
from flask import Flask, Response, jsonify, request
import pandas as pd

GEOLOCATE_URL = "http://ip-api.com/json"
WEATHER_API_KEY = "b3798bbdd6e117731b783155edc5b655"
WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"

dictionary_df = pd.read_csv("data/dictionary.csv").set_index("word")
jokes_df = pd.read_csv("data/jokes.csv")
quotes_df = pd.read_csv("data/quotes.csv")

jokes = jokes_df.to_dict(orient="records")
quotes = quotes_df.to_dict(orient="records")

app = Flask(__name__)

def pretty_print_response(data):
    return json.dumps(data, indent=2, sort_keys=True)

@app.route("/")
def home():
    data = {
        "name": "Kushal Gupta",
        "github": "https://github.com/guptakushal03",
        "linkedin": "https://www.linkedin.com/in/guptakushal03/",
        "project": "Utility API",
        "description": "A REST API that is build to support another project by providing random jokes, quotes, and other functionalities.",
        "endpoints": {
            "/datetime": "Get current date and time",
            "/define?word=word": "Get meaning of a word provided",
            "/joke": "Get a random joke",
            "/quote": "Get a random quote",
            "/weather": "Get weather information"
        }
    }
    
    response = pretty_print_response(data)
    return Response(response, mimetype="application/json")

def get_location():
    try:
        response = requests.get(GEOLOCATE_URL, timeout=3)
        data = response.json()
        return data.get("city", "Ahmedabad")
    except requests.RequestException:
        return "Ahmedabad"

@app.route('/weather', methods=['GET'])
def get_weather():
    city = get_location()
    params = {"q": city, "appid": WEATHER_API_KEY, "units": "metric"}

    try:
        response = requests.get(WEATHER_URL, params=params, timeout=3)
        response.raise_for_status()
        data = response.json()
    except requests.RequestException:
        return jsonify({"error": "Weather API request failed"}), 500

    data = {
        "city": data.get("name", city),
        "temperature": data["main"]["temp"],
        "humidity": data["main"]["humidity"],
        "condition": data["weather"][0]["description"]
    }
    
    response = pretty_print_response(data)
    return Response(response, mimetype="application/json")

@app.route('/define', methods=['GET'])
def get_definition():
    word = request.args.get("word", "").strip().lower()
    if not word:
        return jsonify({"error": "No word provided"}), 400

    if word not in dictionary_df.index:
        return jsonify({"error": "Word not found"}), 404

    definition = dictionary_df.loc[word, "definition"]
    definition = re.sub(r'\\n\d+', '', definition).replace("\\n", " ")

    data = {"word": word, "definition": definition}
    
    response = pretty_print_response(data)
    return Response(response, mimetype="application/json")

@app.route('/datetime', methods=['GET'])
def get_datetime():
    now = datetime.datetime.now()
    data = {
        "date": now.strftime("%Y-%m-%d"),
        "time": now.strftime("%H:%M:%S"),
        "weekday": now.strftime("%A"),
    }
    
    response = pretty_print_response(data)
    return Response(response, mimetype="application/json")

@app.route('/joke', methods=['GET'])
def get_joke():
    joke = random.choice(jokes)
    data = {"id": joke["ID"], "joke": joke["Joke"]}
    
    response = pretty_print_response(data)
    return Response(response, mimetype="application/json")

@app.route('/quote', methods=['GET'])
def get_quote():
    quote = random.choice(quotes)
    data = {"quote": quote["quote"], "author": quote["author"]}
    
    response = pretty_print_response(data)
    return Response(response, mimetype="application/json")

if __name__ == "__main__":
    app.run(debug=True)
