from tqdm import tqdm

from src.core.mappers import map_owned_game, enrich_game_with_store_data
from src.api.steam_api import SteamClient
from src.api.steam_store import SteamStoreClient
from src.export.exporter import export_to_csv, export_to_excel  
from src.db.database import save_games_to_db

def main():
    api_client = SteamClient()
    store_client = SteamStoreClient()

    print("Resolving Vanity URL...")
    steam_id = api_client.resolve_vanity()

    print(f"Fetching games for SteamID: {steam_id}...")
    raw_games = api_client.get_owned_games(steam_id)

    games = [map_owned_game(game) for game in raw_games]
    print(f"Found {len(games)} games.\n")

    print("Enriching game data from Steam Store (using cache)...")
    for game in tqdm(games, desc="Processing Library", unit="game"):
        store_data = store_client.get_app_details(game.appid)
        enrich_game_with_store_data(game, store_data)
        
    print("\nEnrichment complete. Exporting data...")
    
    # Export CSV
    csv_path = "output/library.csv"
    export_to_csv(games, csv_path)
    print(f"✓ CSV exported to {csv_path}")
    
    # Export Excel
    excel_path = "output/library.xlsx"
    export_to_excel(games, excel_path)
    print(f"✓ Excel exported to {excel_path}")
    
    print("\nInjecting data into local SQLite database...")
    save_games_to_db(games)
    print("✓ Database updated successfully (library.db)")


if __name__ == "__main__":
    main()