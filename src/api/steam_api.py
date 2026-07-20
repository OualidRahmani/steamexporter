import os

from dotenv import load_dotenv

from src.api.http_client import HttpClient

load_dotenv()


class SteamClient(HttpClient):
    BASE_URL = "https://api.steampowered.com"

    def __init__(self):
        super().__init__()
        
        self.api_key = os.getenv("STEAM_API_KEY")
        self.vanity = os.getenv("STEAM_VANITY")

        if not self.api_key:
            raise ValueError("STEAM_API_KEY is missing from .env")

        if not self.vanity:
            raise ValueError("STEAM_VANITY is missing from .env")

    def resolve_vanity(self):
        data = self.get(
            f"{self.BASE_URL}/ISteamUser/ResolveVanityURL/v1/",
            params={
                "key": self.api_key,
                "vanityurl": self.vanity,
            },
        )

        if data.get("response", {}).get("success") == 1:
            return data["response"]["steamid"]
        
        raise ValueError(f"Failed to resolve vanity URL. Steam response: {data}")

    def get_owned_games(self, steam_id):
        response = self.get(
            f"{self.BASE_URL}/IPlayerService/GetOwnedGames/v1/",
            params={
                "key": self.api_key,
                "steamid": steam_id,
                "include_appinfo": True,
                "include_played_free_games": True,
            },
        )

        return response["response"].get("games", [])