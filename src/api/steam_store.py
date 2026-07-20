import json
import time
from pathlib import Path
from requests.exceptions import HTTPError
from tqdm import tqdm

from src.api.http_client import HttpClient


class SteamStoreClient(HttpClient):
    BASE_URL = "https://store.steampowered.com/api"
    CACHE_DIR = Path("cache")
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.CACHE_DIR.mkdir(exist_ok=True)
    
    def get_app_details(self, appid: int) -> dict:
        cache_file = self.CACHE_DIR / f"{appid}.json"

        if cache_file.exists():
            with open(cache_file, "r", encoding="utf-8") as f:
                return json.load(f)

        # Retry logic for 429 Too Many Requests
        max_retries = 3
        for attempt in range(max_retries):
            try:
                data = self.get(
                    f"{self.BASE_URL}/appdetails",
                    params={
                        "appids": appid,
                        "cc": "us"  # Ensures pricing is in USD
                    },
                )
                break  # Exit the loop if the request is successful
                
            except HTTPError as e:
                if e.response.status_code == 429:
                    wait_time = 60 * 2  # Wait 2 minutes
                    tqdm.write(f"\n[Steam Rate Limit] Pausing for {wait_time} seconds before retrying...")
                    time.sleep(wait_time)
                    if attempt == max_retries - 1:
                        raise e  # Fail completely if we run out of retries
                else:
                    raise e  # Re-raise if it's a different HTTP error like 404 or 500

        time.sleep(0.2)
        
        app_data = data.get(str(appid), {})

        result = {}
        if app_data.get("success", False):
            result = app_data.get("data", {})
            
        with open(cache_file, "w", encoding="utf-8") as f:
            json.dump(result, f, ensure_ascii=False, indent=4)
            
        return result