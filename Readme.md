# 🏅 Olympics Data Analysis Dashboard

An interactive web app that explores **120 years of Summer Olympics history (1896-2016)**: who won, which countries dominate which sports, and how the Games have changed over time.

**🔗 Live demo:** (https://olympics-analysis-fhvcvp5sszjnnhvfwxza4t.streamlit.app/)

![Olympics Data Analysis banner](file:///C:/Users/windows%2010/Downloads/banner.svg)

## Why I built this

I wanted an end-to-end data project: take a large, messy real-world dataset (~270k rows), clean it properly, answer real questions with it, and ship it as an app anyone can open with a link.

## What you can do in the app

| Section | What it shows |
|---|---|
| **Medal Tally** | Medals by country and year. Filter by edition, country, or both. |
| **Overall Analysis** | Editions, host cities, sports, events, athletes and nations; growth of nations, events and athletes over time; events-per-sport heatmap; most successful athletes by sport. |
| **Country-wise Analysis** | Medals per year for any country, a sport-by-year heatmap showing where it is strong, and its top 10 athletes. |
| **Athlete-wise Analysis** | Age distribution of all athletes vs gold/silver/bronze medalists, height vs weight by sport, men vs women participation over time. |

## Data

[120 years of Olympic history: athletes and results](https://www.kaggle.com/datasets/heesoo37/120-years-of-olympic-history-athletes-and-results) (Kaggle). Two files are used: `athlete_events.csv` (one row per athlete per event) and `noc_regions.csv` (maps NOC codes to country names).

## Data cleaning and analysis decisions

These are the details that make the numbers correct, not just plausible:

- **Summer Games only.** The dataset mixes Summer and Winter; the app filters to Summer for consistent comparison across eras.
- **Team events counted once.** In a team event (hockey, relay) every player has a medal row, so a naive count gives a country 16 hockey golds instead of 1. Medal tallies de-duplicate on `Team, NOC, Games, Year, City, Sport, Event, Medal`.
- **No de-duplication on athlete ID.** Dropping duplicates on `ID` would delete the second and third medal of the same athlete and under-count medals.
- **Medals one-hot encoded** (`Gold`, `Silver`, `Bronze`) so counts are simple, fast sums.
- **Country names merged** from the NOC table (`left` merge keeps every athlete row).
- **1906 excluded from the edition count.** The 1906 Intercalated Games are not officially counted as an Olympic edition.
- **Missing values handled explicitly.** Age, height and weight have many gaps; charts drop only the rows missing the specific field they use, and height/weight scatter plots keep each athlete's best medal.
- **Performance.** Data loading is cached (`st.cache_data`), the scatter plot samples up to 5,000 points, and the 41 MB CSV is stored as a 5 MB `.csv.gz` that pandas reads directly.

## Tech stack

Python · pandas · Plotly · Matplotlib · Seaborn · Streamlit

## Project structure

```
app.py                  Streamlit UI and navigation
helper.py               Analysis functions (one function per chart/table)
preprocessor.py         Cleaning and feature preparation
requirements.txt        Dependencies
athlete_events.csv.gz   Athlete-level results (compressed)
banner.svg              README header image
noc_regions.csv         NOC code to country mapping
```

The UI (`app.py`) contains no analysis logic; all calculations live in `helper.py`, which keeps the code easy to test and extend.

## Run locally

```bash
python -m venv venv
venv\Scripts\activate          # Windows
pip install -r requirements.txt
python -m streamlit run app.py
```

## Limitations

- The dataset ends at **Rio 2016**; later Games (Tokyo 2020, Paris 2024) are not included.
- Winter Games are filtered out.
- Early-era records (pre-1950) have more missing age, height and weight values.

## Ideas for next steps

- Add Tokyo 2020 and Paris 2024 data and a Summer/Winter toggle.
- Medals per capita and per GDP to compare countries fairly.
- Predict a country's medal count from past editions.
- Add automated tests for the functions in `helper.py`.

## Author

**Your Name** · [LinkedIn](https://www.linkedin.com/in/YOUR_PROFILE) · [GitHub](https://github.com/YOUR_USERNAME)
