import asyncio
import datetime as dt
import json
from functools import partial
from time import perf_counter
from typing import Any

import dotenv
import httpx
from dateutil.relativedelta import relativedelta as rd

API_KEY = dotenv.get_key(".env", key_to_get="FRED_API")


class AsyncClient:
    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self._client = httpx.AsyncClient(base_url="https://api.stlouisfed.org/fred", params={"api_key": self.api_key})

    async def _get(self, params: dict, endpoint: str) -> dict:
        r: httpx.Response = await self._client.get(params=params, url=endpoint)
        return json.loads(r.text)

    async def get_sp500(self, start_date: dt.datetime, end_date: dt.datetime) -> list[dict]:
        # For sake of this example, let's say this API only allows us to get 30 days of data per request.
        # Many APIs have limitations, so we're creating an artificial one here.

        start_date = start_date.replace(day=1)  # always use first day of the month for simplicity
        end_date = end_date.replace(day=31)  # always use month end for simplicity
        date_diff = rd(end_date, start_date)
        months = date_diff.years * 12 + date_diff.months + 1

        # generate list of query parameters
        all_params = [
            {
                "series_id": "SP500",
                "frequency": "d",
                "observation_start": (start_date + rd(months=m)).strftime("%Y-%m-%d"),
                "observation_end": (start_date + rd(months=m, day=31)).strftime("%Y-%m-%d"),
                "file_type": "json",
            }
            for m in range(months)
        ]

        fn = partial(self._get, endpoint="series/observations")

        result = await asyncio.gather(*map(fn, all_params))

        return result


def print_json(data: Any) -> None:  # noqa: ANN401
    print(json.dumps(data, indent=4))  # noqa: T201


async def main() -> None:
    if not API_KEY:
        raise ImportError("FRED API key is missing. Create a .env file containing a key named FRED_API.")

    c = AsyncClient(API_KEY)
    start_date = dt.datetime(2025, 1, 1)
    end_date = dt.datetime(2025, 12, 31)

    start_time = perf_counter()
    data = await c.get_sp500(start_date, end_date)
    print_json(data)
    end_time = perf_counter()
    print(  # noqa: T201
        f"`httpx` took: {end_time - start_time:.1f} seconds to download data from {start_date.strftime('%Y-%m-%d')} to {end_date.strftime('%Y-%m-%d')}."
    )


if __name__ == "__main__":
    asyncio.run(main())
