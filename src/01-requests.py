import json

import dotenv
import requests
from requests.adapters import HTTPAdapter, Retry

API_KEY = dotenv.get_key(".env", key_to_get="FRED_API")


def make_session(num_retries: int = 5) -> requests.Session:
    s = requests.Session()
    retries = Retry(total=num_retries, backoff_factor=1)
    s.mount("https://", HTTPAdapter(max_retries=retries))

    return s


def _get(endpoint: str, session: requests.Session) -> requests.Response:
    base_url = "https://api.stlouisfed.org/fred"
    return session.get(f"{base_url}/{endpoint}&api_key={API_KEY}")


def print_json(data: dict) -> None:
    print(json.dumps(data, indent=4))  # noqa: T201


def get_sp500(session: requests.Session) -> dict:
    r = _get("series/observations?series_id=SP500&frequency=d&limit=10&file_type=json", session)

    return json.loads(r.text)


def main() -> None:
    if not API_KEY:
        raise ImportError("FRED API key is missing. Create a .env file containing a key named FRED_API.")

    s = make_session()
    data = get_sp500(s)
    print_json(data)


if __name__ == "__main__":
    main()
