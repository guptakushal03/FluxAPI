# FluxAPI

A simple REST API built using Flask that provides random jokes, quotes, weather updates, dictionary definitions, and the current date/time. Designed to support other projects with utility-based responses.

---

## Live Endpoints

| Endpoint         | Description                                 |
|------------------|---------------------------------------------|
| `/`              | Project info and list of endpoints          |
| `/datetime`      | Returns current date, time, and weekday     |
| `/define?word=`  | Returns the definition of a given word      |
| `/joke`          | Returns a random joke                       |
| `/quote`         | Returns a random inspirational quote        |
| `/weather`       | Returns weather data based on your location |

---

## Features

- **Joke API**: Pulls from a dataset of 200k+ jokes.
- **Quote API**: Returns motivational quotes with author names.
- **Dictionary API**: Offline dictionary support from CSV.
- **Weather API**: Auto-detects your city and fetches real-time weather using OpenWeatherMap.
- **Datetime API**: Provides formatted date, time, and weekday.

---

## Tech Stack

- Python
- Flask
- Pandas
- Requests
- OpenWeatherMap API

---

## Datasets Required

Ensure the following files exist in a `data/` folder:
- `dictionary.csv`
- `jokes.csv`
- `quotes.csv`

---

## Getting Started

```bash
pip install -r requirements.txt
python app.py
```

---

## Author

[Kushal Ravindrakumar Gupta](https://github.com/guptakushal03)
