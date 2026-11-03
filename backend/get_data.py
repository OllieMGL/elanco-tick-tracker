import os
import time

import requests
from dotenv import load_dotenv

load_dotenv()  
ELANCO_API_URL = os.getenv("ELANCO_API_URL")

MAX_ATTEMPTS = 3
RETRY_WAIT_SECONDS = 2
TIMEOUT_SECONDS = 10


class ElancoAPIError(Exception):
    pass

def get_sightings():
    url = f"{ELANCO_API_URL}/tick-sightings"

    for attempt in range(MAX_ATTEMPTS):
        try:
            response = requests.get(url, timeout=TIMEOUT_SECONDS)
        except requests.RequestException:
            response = None

        if response is not None and response.status_code == 200:
            return response.json()

        # 429 = too many requests && 5xx = Elanco server error ==> give it another go
        if response is not None and response.status_code != 429 and response.status_code < 500:
            raise ElancoAPIError(f"Elanco API returned status {response.status_code}")

        if attempt < MAX_ATTEMPTS - 1:
            time.sleep(RETRY_WAIT_SECONDS)

    raise ElancoAPIError(f"Elanco API unavailable after {MAX_ATTEMPTS} attempts")
