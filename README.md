
# 🌍 Global Weather Analytics Pipeline

> An end-to-end data collection and analytics project that fetches real-time
> weather data for **200 cities worldwide**, engineers 20+ features, and ranks
> cities by a custom **Comfort Index**.

<p align="center">
  <a href="https://www.python.org/"><img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white" alt="Python"></a>
  <a href="https://pandas.pydata.org/"><img src="https://img.shields.io/badge/pandas-2.x-150458?logo=pandas&logoColor=white" alt="pandas"></a>
  <a href="https://numpy.org/"><img src="https://img.shields.io/badge/NumPy-1.26+-013243?logo=numpy&logoColor=white" alt="NumPy"></a>
  <a href="https://matplotlib.org/"><img src="https://img.shields.io/badge/Matplotlib-3.x-11557C?logo=matplotlib&logoColor=white" alt="Matplotlib"></a>
  <a href="https://jupyter.org/"><img src="https://img.shields.io/badge/Jupyter-Notebook-F37626?logo=jupyter&logoColor=white" alt="Jupyter"></a>
  <a href="https://openweathermap.org/api"><img src="https://img.shields.io/badge/Data-OpenWeatherMap-EB6E4B?logo=openweathermap&logoColor=white" alt="OpenWeatherMap"></a>
  <img src="https://img.shields.io/badge/Cities-200-2EA44F" alt="Cities">
  <img src="https://img.shields.io/badge/Features-20+-9CF" alt="Features">
</p>

---

## 📑 Table of Contents

- [Overview](#-overview)
- [Pipeline Architecture](#-pipeline-architecture)
- [Tech Stack](#-tech-stack)
- [Repository Structure](#-repository-structure)
- [Getting Started](#-getting-started)
- [Data Schema](#-data-schema)
- [Methodology — Comfort Index](#-methodology--comfort-index)
- [Key Findings](#-key-findings)
- [Roadmap](#-roadmap)
- [License](#-license)

---

## 📖 Overview

This project demonstrates a complete **data engineering & analytics workflow**:

1. **Ingestion** — Pull real-time weather observations from the OpenWeatherMap API across 200 cities.
2. **Processing** — Clean, normalize, and engineer 20+ descriptive features.
3. **Storage** — Persist structured records in versioned CSV format for reproducibility.
4. **Analysis** — Perform exploratory data analysis (EDA) and correlation studies.
5. **Ranking** — Score cities using a domain-driven **Comfort Index** and surface global patterns.

It's both a portfolio piece and a foundation for a production-grade pipeline (see [Roadmap](#-roadmap)).

---

## 🏗 Pipeline Architecture

```
  ┌─────────────────┐     ┌──────────────────┐     ┌─────────────────┐
  │  OpenWeatherMap │────▶│  daily_collection│────▶│   Raw + Clean   │
  │      API        │     │       .py        │     │   CSV (data/)   │
  └─────────────────┘     └──────────────────┘     └────────┬────────┘
                                                            │
                                                            ▼
                                                  ┌──────────────────┐
                                                  │   main.ipynb     │
                                                  │ EDA · Features · │
                                                  │  Comfort Index   │
                                                  └────────┬─────────┘
                                                           │
                                                           ▼
                                                  ┌──────────────────┐
                                                  │  Rankings · Plots│
                                                  │   · Insights     │
                                                  └──────────────────┘
```

---

## 🧰 Tech Stack

| Layer         | Tools                                   |
| ------------- | --------------------------------------- |
| Language      | Python 3.10+                            |
| Data          | pandas, NumPy                           |
| I/O           | `requests` (REST), OpenWeatherMap API |
| Visualization | Matplotlib                              |
| Environment   | Jupyter Notebook                        |

---

## 📂 Repository Structure

```
Weather_analysis/
├── data/                 # Collected weather datasets (raw + cleaned)
├── daily_collection.py   # Scheduled ingestion script (200-city fetch)
├── main.ipynb            # End-to-end analysis notebook
├── .gitignore
└── README.md
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10 or higher
- A free [OpenWeatherMap API key](https://openweathermap.org/api)

### Installation

```bash
git clone https://github.com/nsdmlk/Weather_analysis.git
cd Weather_analysis
python -m venv .venv && source .venv/bin/activate   # optional
pip install pandas numpy requests matplotlib jupyter
```

### Configuration

Export your API key as an environment variable:

```bash
export OPENWEATHER_API_KEY="your_api_key_here"
```

### Usage

```bash
# 1. Collect a fresh snapshot of weather for all 200 cities
python daily_collection.py

# 2. Explore the analysis
jupyter notebook main.ipynb
```

---

## 🗃 Data Schema

Each record represents one city's weather snapshot. Representative fields:

| Field          | Description                 | Unit |
| -------------- | --------------------------- | ---- |
| `city`       | City name                   | —   |
| `country`    | Country code                | —   |
| `temp`       | Air temperature             | °C  |
| `feels_like` | Perceived temperature       | °C  |
| `humidity`   | Relative humidity           | %    |
| `pressure`   | Atmospheric pressure        | hPa  |
| `wind_speed` | Wind speed                  | m/s  |
| `clouds`     | Cloud cover                 | %    |
| `sunrise`    | Local sunrise time          | ISO  |
| `sunset`     | Local sunset time           | ISO  |
| …             | *+10 additional features* |      |

---

## 🧪 Methodology — Comfort Index

To move beyond raw temperature, I designed a **Comfort Index** that blends perceived temperature, humidity, wind, and cloud cover into a single 0–100 score:

$$
\text{Comfort} = 100 - 2.0 \cdot \left| \frac{T + F}{2} - 22 \right| - 0.3 \cdot |H - 50| - 1.5 \cdot W - 0.2 \cdot C
$$

| Symbol | Meaning           |
| ------ | ----------------- |
| $T$  | Temperature (°C) |
| $F$  | Feels-like (°C)  |
| $H$  | Humidity (%)      |
| $W$  | Wind speed (m/s)  |
| $C$  | Cloud cover (%)   |

The model anchors comfort to **22 °C / 50% RH** — a widely cited thermal comfort baseline — and penalizes deviations in each dimension.

---

## 📊 Key Findings

- **Temperature ↔ humidity:** moderate negative correlation (**r ≈ −0.58**) — hotter cities tend to be drier.
- **Feels-like gap:** neither wind nor humidity alone explains the difference between measured and perceived temperature — it's a non-linear interaction.
- **Ranking realism:** averaging actual and perceived temperature yields more believable comfort scores than raw temperature alone.

### 🏆 Most Comfortable Cities

Istanbul · Novosibirsk · Johannesburg · Busan · Ufa

### 🥶 Least Comfortable Cities

Chennai · Murmansk · Tashkent · Hong Kong · Shenzhen

---

## 🗺 Roadmap

This project is the foundation for a production-grade pipeline. Planned work:

- [ ] **Orchestration** — migrate `daily_collection.py` to an **Airflow** DAG for scheduled runs.
- [ ] **Warehouse** — load data into **PostgreSQL** / **ClickHouse** for time-series storage.
- [ ] **Transformations** — add a **dbt** layer for reusable metric models.
- [ ] **Dashboard** — deploy an interactive **Streamlit / Metabase** view.
- [ ] **ML modeling** — predict perceived temperature from environmental features.
- [ ] **Containerization** — ship everything in **Docker**.

---

## 📄 License

This project is released for educational and portfolio purposes. Weather data is
provided by [OpenWeatherMap](https://openweathermap.org/) under their terms of service.

---

<p align="center">
  <em>Built by <a href="https://github.com/nsdmlk">nsdmlk</a> — feedback and suggestions welcome.</em>
</p>
