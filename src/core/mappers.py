from datetime import datetime

from src.core.models import Game


def map_owned_game(data: dict) -> Game:
    last_played = None
    if "rtime_last_played" in data:
        last_played = datetime.fromtimestamp(data["rtime_last_played"])

    return Game(
        appid=data["appid"],
        name=data["name"],
        playtime_minutes=data["playtime_forever"],
        last_played=last_played,
        has_community_stats=data.get("has_community_visible_stats", False),
    )
    
def enrich_game_with_store_data(game: Game, store_data: dict) -> Game:
    """Mutates the Game object with additional data from the Steam Store."""
    if not store_data:
        return game  

    game.developers = store_data.get("developers", [])
    game.publishers = store_data.get("publishers", [])
    
    game.genres = [g.get("description", "") for g in store_data.get("genres", [])]
    game.categories = [c.get("description", "") for c in store_data.get("categories", [])]
    game.header_image = store_data.get("header_image")

    release = store_data.get("release_date", {})
    if not release.get("coming_soon"):
        game.release_date = release.get("date")

    game.is_free = store_data.get("is_free", False)
    if game.is_free:
        game.price = "Free"
        game.discount = 0
    else:
        price = store_data.get("price_overview", {})
        if price:
            # final_formatted will now automatically be in USD (e.g., "$19.99")
            game.price = price.get("final_formatted")
            game.discount = price.get("discount_percent")
        else:
            game.price = "N/A" # For delisted games or games no longer for sale

    return game