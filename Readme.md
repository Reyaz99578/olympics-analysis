# Olympics Data Analysis

An interactive Streamlit dashboard that explores 120 years of Summer Olympics history (1896-2016).

## Features

- **Medal Tally**: filter by year and country, with team events counted once.
- **Overall Analysis**: editions, hosts, sports, events, athletes and nations; trends over time; events-per-sport heatmap; most successful athletes by sport.
- **Country-wise Analysis**: medals per year, strongest sports (heatmap) and top athletes for any country.
- **Athlete-wise Analysis**: age distribution of medalists, height vs weight by sport, men vs women participation over time.

## Tech stack

Python, pandas, Plotly, Matplotlib, Seaborn, Streamlit.

## Data

[120 years of Olympic history: athletes and results](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results) from Kaggle (`athlete_events.csv` and `noc_regions.csv`). The athlete file is stored compressed as `athlete_events.csv.gz` to keep the repository small.

## Run locally

```
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python -m streamlit run app.py
```

## Project structure

```
app.py               Streamlit UI
helper.py            Analysis functions
preprocessor.py      Data cleaning (Summer games, region merge, medal columns)
requirements.txt     Dependencies
athlete_events.csv.gz
noc_regions.csv
```
