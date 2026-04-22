# Frankenstein — Football Player Similarity Engine

A scouting tool that identifies statistically similar football players across multiple leagues. Built as Master's Thesis for the MSc in Big Data for Football Analytics and Scouting at the Real Madrid Graduate School.

## What it does

Frankenstein lets you build a target player profile by combining stats from multiple real players with custom weights, then ranks candidates by statistical proximity to that profile. Supports both Euclidean distance and Cosine similarity as comparison methods.

## Tech stack

- **Python** — core logic
- **Pandas / NumPy / SciPy** — data processing and distance metrics
- **Dash (Plotly)** — interactive web interface
- **Docker** — containerization (coming soon)

## How to run

```bash
git clone https://github.com/FranciscoNM-dev/TFM-Frankenstein.git
cd TFM-Frankenstein
python -m venv .venv
source .venv/Scripts/activate  # Windows
pip install -r requirements.txt
python -m src.app
```

Open `http://localhost:2024` in your browser.

## Project structure
```
TFM-Frankenstein/
├── src/
│   ├── app.py        # Dash application and callbacks
│   └── utils.py      # Similarity functions (Euclidean, Cosine)
├── data/
│   ├── raw/          # Source data from fbref and Transfermarkt
│   └── processed/    # Cleaned datasets ready for the app
├── scripts/          # Data acquisition and processing scripts
├── assets/           # CSS styles
└── requirements.txt
```

## Known limitations

- The fbref scraper (`scripts/actualizarFbref.py`) is currently broken due to fbref updating their anti-scraping measures. The processed datasets included in the repo reflect data from the 2023/24 season.
- UI styling partially broken after upgrading to Dash 4.x.

## Next steps

- Fix Dash 4.x styling issues
- Replace fbref scraper with a working alternative
- Add Docker support for easier deployment