import datetime as dt
import json
from time import perf_counter

import dotenv
import requests
from dateutil.relativedelta import relativedelta as rd
from requests.adapters import HTTPAdapter, Retry

API_KEY = dotenv.get_key(".env", key_to_get="FRED_API")


class SyncClient:
    def __init__(self, api_key: str, num_retries: int = 5) -> None:
        self.api_key = api_key
        self._session = self.make_session(num_retries)

    @staticmethod
    def make_session(num_retries: int) -> requests.Session:
        s = requests.Session()
        retries = Retry(total=num_retries, backoff_factor=1)
        s.mount("https://", HTTPAdapter(max_retries=retries))

        return s

    def _get(self, endpoint: str) -> requests.Response:
        # This makes it easier to add other endpoints later.
        base_url = "https://api.stlouisfed.org/fred"
        return self._session.get(f"{base_url}/{endpoint}&api_key={API_KEY}")

    def get_sp500(self, start_date: dt.datetime, end_date: dt.datetime) -> list[dict]:
        # For sake of this example, let's say this API only allows us to get 30 days of data per request.
        # Many APIs have limitations, so we're creating an artificial one here.

        start_date = start_date.replace(day=1)  # always use first day of the month for simplicity
        end_date = end_date.replace(day=31)  # always use month end for simplicity
        date_diff = rd(end_date, start_date)
        months = date_diff.years * 12 + date_diff.months + 1

        result: list[dict] = []
        for m in range(months):
            tmp_start = start_date + rd(months=m)
            tmp_end = tmp_start + rd(day=31)
            r = self._get(
                f"series/observations?series_id=SP500&frequency=d&observation_start={tmp_start.strftime('%Y-%m-%d')}&observation_end={tmp_end.strftime('%Y-%m-%d')}&file_type=json"
            )
            result.append(json.loads(r.text))

        return result


def print_json(data: dict) -> None:
    print(json.dumps(data, indent=4))  # noqa: T201


def main() -> None:
    if not API_KEY:
        raise ImportError("FRED API key is missing. Create a .env file containing a key named FRED_API.")

    c = SyncClient(API_KEY)
    start_date = dt.datetime(2025, 1, 1)
    end_date = dt.datetime(2025, 12, 31)

    start_time = perf_counter()
    data = c.get_sp500(start_date, end_date)
    print_json(data)
    end_time = perf_counter()
    print(  # noqa: T201
        f"`requests` took: {end_time - start_time:.1f} seconds to download data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}."
    )


if __name__ == "__main__":
    main()
