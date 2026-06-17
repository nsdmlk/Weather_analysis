"""Global Weather Analytics — daily collector.

Ingestion script for the Weather_analysis project. Fetches current weather for
each city in `data/cities.txt` from the OpenWeatherMap API and writes a dated
CSV snapshot under `data/`.

Designed to be run unattended via launchd. It is resilient to transient network
failures (retry + backoff), isolates per-city errors so one bad request cannot
kill the whole batch, refuses to push empty/partial datasets, and exits with a
non-zero code so launchd can detect and retry the run.

Exit codes:
    0  success
    1  unrecoverable failure (no network, no records, git error)
"""

import datetime
import logging
import os
import subprocess
import time

import pandas as pd
import requests as rq
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

# --------------------------------------------------------------------------- #
# Configuration
# --------------------------------------------------------------------------- #
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
API_KEY_FILE = os.path.join(BASE_DIR, "data", "API_key.txt")
CITIES_FILE = os.path.join(BASE_DIR, "data", "cities.txt")
DATA_DIR = os.path.join(BASE_DIR, "data")
BASE_URL = "https://api.openweathermap.org/data/2.5/weather"  # https, not http

# Per-request sleep to respect OpenWeatherMap's rate limit (free tier: 60/min).
SLEEP_BETWEEN_REQUESTS_SEC = 1
# Pre-flight connectivity check target.
CONNECTIVITY_CHECK_URL = "https://api.openweathermap.org"

# --------------------------------------------------------------------------- #
# Logging — real timestamps so launchd's log actually tells you something
# --------------------------------------------------------------------------- #
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)
log = logging.getLogger("weather_collector")


# --------------------------------------------------------------------------- #
# HTTP session with automatic retry + exponential backoff
# --------------------------------------------------------------------------- #
def make_session() -> rq.Session:
    """Return a Session that retries transient failures automatically."""
    session = rq.Session()
    retry = Retry(
        total=5,                      # up to 5 attempts per request
        backoff_factor=2,             # waits 2s, 4s, 8s, 16s, 32s...
        status_forcelist=[429, 500, 502, 503, 504],
        allowed_methods=["GET"],
        raise_on_status=False,
    )
    adapter = HTTPAdapter(max_retries=retry)
    session.mount("http://", adapter)
    session.mount("https://", adapter)
    return session


def check_connectivity(session: rq.Session) -> bool:
    """Fail fast if there is no network — better than a confusing crash later."""
    try:
        session.get(CONNECTIVITY_CHECK_URL, timeout=10)
        return True
    except rq.RequestException as e:
        log.error(f"No network connectivity, aborting: {e}")
        return False


# --------------------------------------------------------------------------- #
# Core collection loop — one bad city must NOT ruin the whole batch
# --------------------------------------------------------------------------- #
def collect_weather(session: rq.Session, api_key: str, cities: list[str]) -> list[dict]:
    records: list[dict] = []
    failures: list[str] = []

    for i, city in enumerate(cities, 1):
        params = {"q": city, "appid": api_key, "units": "metric"}
        try:
            response = session.get(BASE_URL, params=params, timeout=15)
            response.raise_for_status()
            data = response.json()

            records.append({
                'city': city,
                'country': data['sys']['country'],
                'lon': data['coord']['lon'],
                'lat': data['coord']['lat'],
                'temp': data['main']['temp'],
                'feels_like': data['main']['feels_like'],
                'temp_min': data['main']['temp_min'],
                'temp_max': data['main']['temp_max'],
                'pressure': data['main']['pressure'],
                'humidity': data['main']['humidity'],
                'sea_level': data['main'].get('sea_level'),
                'grnd_level': data['main'].get('grnd_level'),
                'visibility': data.get('visibility'),
                'wind_speed': data['wind']['speed'],
                'wind_deg': data['wind']['deg'],
                'wind_gust': data['wind'].get('gust'),
                'clouds': data['clouds']['all'],
                'weather_main': data['weather'][0]['main'],
                'weather_description': data['weather'][0]['description'],
                'weather_icon': data['weather'][0]['icon'],
                'timezone': data['timezone'],
            })
            log.info(f"[{i}/{len(cities)}] OK  {city}")
        except rq.RequestException as e:
            # Isolate the failure — log it and keep going.
            log.warning(f"[{i}/{len(cities)}] FAIL {city}: {e}")
            failures.append(city)

        time.sleep(SLEEP_BETWEEN_REQUESTS_SEC)

    if failures:
        log.warning(f"{len(failures)} city/cities failed: {failures}")
    return records


# --------------------------------------------------------------------------- #
# Persistence + git commit (only when there is real new data)
# --------------------------------------------------------------------------- #
def save_dataset(records: list[dict]) -> str | None:
    if not records:
        log.error("No records collected — not writing anything")
        return None

    os.makedirs(DATA_DIR, exist_ok=True)
    out_path = os.path.join(
        DATA_DIR, f"dataset_{datetime.date.today().strftime('%Y-%m-%d')}.csv"
    )
    df = pd.DataFrame(records)
    df.to_csv(out_path, index=False)
    log.info(f"Wrote {len(df)} rows -> {out_path}")
    return out_path


def commit_and_push(path: str) -> bool:
    """Stage + commit + push the dataset. Returns True on success."""
    try:
        subprocess.run(["git", "add", path], check=True, cwd=BASE_DIR)
        subprocess.run(
            ["git", "commit", "-m", f"Daily weather dataset {datetime.date.today()}"],
            check=True,
            cwd=BASE_DIR,
        )
        subprocess.run(["git", "push"], check=True, cwd=BASE_DIR)
        log.info("Pushed to GitHub")
        return True
    except subprocess.CalledProcessError as e:
        log.error(f"Git step failed: {e}")
        return False


# --------------------------------------------------------------------------- #
# Entry point
# --------------------------------------------------------------------------- #
def main() -> int:
    # Read secrets/inputs.
    try:
        with open(API_KEY_FILE) as f:
            api_key = f.read().strip()
        with open(CITIES_FILE) as f:
            cities = [line.strip() for line in f if line.strip()]
    except OSError as e:
        log.error(f"Cannot read input file: {e}")
        return 1

    log.info(f"Starting collection for {len(cities)} cities")

    session = make_session()
    if not check_connectivity(session):
        return 1

    records = collect_weather(session, api_key, cities)

    out_path = save_dataset(records)
    if out_path is None:
        return 1

    commit_and_push(out_path)
    log.info("Done.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
