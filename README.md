
# 🌤️ Weather Data Pipeline & Analytics

A personal project to collect, analyze, and rank weather conditions across **200 cities worldwide** using the OpenWeatherMap API.

---

## 🎯 What This Project Does

- Fetches real-time weather from 200 cities around the globe
- Extracts 20+ features: temperature, humidity, pressure, wind, clouds, sunrise/sunset, and more
- Cleans and stores the data in structured CSV format
- Performs exploratory analysis to uncover patterns and extremes
- Builds a **custom Comfort Index** to rank cities by how pleasant their weather feels
- Runs targeted correlation analysis to test common assumptions about weather perception

---

## 🛠️ Tech Stack

**Python** — pandas, requests, matplotlib, numpy
**Data** — OpenWeatherMap API
**Notebook** — Jupyter

---

## 📊 Key Findings

- **Temperature vs humidity:** moderate negative correlation (r ≈ -0.58) — hotter cities tend to be drier
- **Feels-like gap:** neither wind nor humidity alone explains the difference between actual and perceived temperature — it's a non-linear combination
- **Comfort ranking:** averaging actual and perceived temperature produces more realistic scores than raw temperature alone
- **Top comfortable cities:** Istanbul, Novosibirsk, Johannesburg, Busan, Ufa
- **Least comfortable:** Chennai, Murmansk, Tashkent, Hong Kong, Shenzhen

---

## 🧪 Comfort Index Formula

$$
\text{Comfort} = 100 - 2.0 \cdot \left| \frac{T + F}{2} - 22 \right| - 0.3 \cdot |H - 50| - 1.5 \cdot W - 0.2 \cdot C
$$

Where:

- $T$ — temperature (°C)
- $F$ — feels like (°C)
- $H$ — humidity (%)
- $W$ — wind speed (m/s)
- $C$ — cloud cover (%)

---

## 🚀 Future Ideas

- Automate daily collection for time-series analysis
- Build a prediction model for perceived temperature
- Deploy as an interactive dashboard
- Build some analysis models
