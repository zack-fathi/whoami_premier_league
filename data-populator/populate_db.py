import os
import psycopg
import requests
import time
import json

##############################
# Environment / Config
##############################

DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "whoami_db")
DB_USER = os.getenv("DB_USER", "whoami_user")
DB_PASS = os.getenv("DB_PASS", "whoami_password")
TRANSFERMARKT_API_URL = os.getenv("TRANSFERMARKT_API_URL", "http://transfermarkt-api:8000")

##############################
# 1) Create table if not exists
##############################

def create_table_if_not_exists():
    time.sleep(10)
    create_table_sql = """
    CREATE TABLE IF NOT EXISTS players (
        id             TEXT PRIMARY KEY,
        club           TEXT,
        name           TEXT,
        position       TEXT,
        foot           TEXT,
        date_of_birth  DATE,
        age            INT,
        height         INT,
        market_value   BIGINT,
        nationality    TEXT,
        stats          JSONB,
        transfers      JSONB
    );
    """

    with psycopg.connect(
        host=DB_HOST,
        port=DB_PORT,
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASS
    ) as conn:
        conn.execute(create_table_sql)
        print("Table 'players' created (if not exists).")

##############################
# 2) API Helper Functions
##############################

def get_competition_clubs(competition_id):
    """Fetches all clubs in a competition from the Transfermarkt API."""
    url = f"{TRANSFERMARKT_API_URL}/competitions/{competition_id}/clubs"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    print(f"Error fetching clubs for competition {competition_id}: {response.status_code}")
    return None

def get_club_players(club_id):
    """Fetches club data (players) from the Transfermarkt API."""
    url = f"{TRANSFERMARKT_API_URL}/clubs/{club_id}/players"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    print(f"Error fetching club {club_id}: {response.status_code}")
    return None

def get_player_stats(player_id):
    """Fetches player stats from the Transfermarkt API."""
    url = f"{TRANSFERMARKT_API_URL}/players/{player_id}/stats"
    response = requests.get(url)
    if response.status_code == 200:
        # This endpoint returns JSON with a "stats" key containing a list of competition stats
        return response.json().get('stats', [])
    print(f"Error fetching player {player_id}: {response.status_code}")
    return None

def get_player_transfers(player_id):
    """Fetches player transfer history from the Transfermarkt API."""
    url = f"{TRANSFERMARKT_API_URL}/players/{player_id}/transfers"
    response = requests.get(url)
    if response.status_code == 200:
        # This endpoint returns JSON with a "transfers" key containing a list of transfer records
        return response.json().get('transfers', [])
    print(f"Error fetching player {player_id} transfers: {response.status_code}")
    return None

##############################
# 3) Insert / Upsert Data
##############################

def insert_player_data_to_db(player_data):
    """
    Inserts/updates player data into the 'players' table, including stats as JSON.
    """
    print("Starting database update...")

    insert_query = """
        INSERT INTO players (
            id,
            club,
            name,
            position,
            foot,
            date_of_birth,
            age,
            height,
            market_value,
            nationality,
            stats,
            transfers
        )
        VALUES (%s, %s,  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        ON CONFLICT (id)
        DO UPDATE
            SET club = EXCLUDED.club,
                name = EXCLUDED.name,
                position = EXCLUDED.position,
                foot = EXCLUDED.foot,
                date_of_birth = EXCLUDED.date_of_birth,
                age = EXCLUDED.age,
                height = EXCLUDED.height,
                market_value = EXCLUDED.market_value,
                nationality = EXCLUDED.nationality,
                stats = EXCLUDED.stats
    """

    try:
        with psycopg.connect(
            host=DB_HOST,
            port=DB_PORT,
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASS
        ) as conn:
            # Enable autocommit to avoid having to manually call commit()
            conn.autocommit = True
            with conn.cursor() as cur:
                for player_id, p_data in player_data.items():
                    basic_info = p_data.get("data", {})
                    if not basic_info:
                        print(f"No basic info for player {player_id}; skipping insert.")
                        continue

                    # Extract basic fields
                    p_id = basic_info.get("id")
                    club = p_data.get("club")
                    name = basic_info.get("name")
                    position = basic_info.get("position")
                    foot = basic_info.get("foot")
                    date_of_birth = basic_info.get("dateOfBirth")  # Expecting 'YYYY-MM-DD'
                    age = basic_info.get("age")
                    height = basic_info.get("height")
                    market_value = basic_info.get("marketValue")

                    # nationality might be a list (e.g., ["Brazil", "Portugal"])
                    nationality = basic_info.get("nationality", [])
                    nationality_str = ", ".join(nationality) if isinstance(nationality, list) else str(nationality)

                    # Stats as JSON (list of dicts)
                    stats_list = p_data.get("stats", [])
                    stats_json = json.dumps(stats_list)

                    # transfers as JSON (list of dicts)
                    transfers_list = p_data.get("transfers", [])
                    transfers_json = json.dumps(transfers_list)

                    try:
                        cur.execute(
                            insert_query,
                            (
                                p_id,
                                club,
                                name,
                                position,
                                foot,
                                date_of_birth,
                                age,
                                height,
                                market_value,
                                nationality_str,
                                stats_json,
                                transfers_json
                            )
                        )
                        print(f"Inserted/updated player {p_id}.")
                    except Exception as e:
                        print(f"Error inserting player {p_id}: {e}")

    except Exception as e:
        print("Error connecting to the database or running the query:", e)

    print("Database update completed.")


##############################
# 4) Main
##############################

def main():
    # 1) Create table (if it doesn't exist yet)
    create_table_if_not_exists()

    time.sleep(5)  # Wait for everything to be ready (if needed)

    # 2) Fetch all clubs in the Premier League (GB1)
    resp = get_competition_clubs("GB1")
    if not resp:
        print("No competition data found. Exiting.")
        return

    clubs = resp.get("clubs", [])
    clubs = {club["id"]: club for club in clubs}
    club_ids = clubs.keys()
    print(f"Found {len(club_ids)} clubs in competition GB1.")

    # Dictionary to store all players data
    # Format: { player_id: { "data": {...}, "stats": [...] }, ... }
    player_data = {}

    # 3) Fetch each club's players, then each player's stats
    for club_id in club_ids:
        club_data = get_club_players(club_id)
        if not club_data:
            continue

        players_list = club_data.get("players", [])
        print(f"Club {club_id} has {len(players_list)} players.")

        # For each player
        for player_dict in players_list:
            player_id = player_dict["id"]  # e.g., "238223"

            # Ensure a dict entry exists for this player
            if player_id not in player_data:
                player_data[player_id] = {}

            # Store "basic" data
            player_data[player_id]["data"] = player_dict

            # Fetch stats
            stats = get_player_stats(player_id)
            # print(stats if stats else f"No stats found for player {player_id}")
            player_data[player_id]["stats"] = stats if stats else []

            transfers = get_player_transfers(player_id)
            # print(transfers if transfers else f"No transfers found for player {player_id}")
            player_data[player_id]["transfers"] = transfers if transfers else []

            # add the players current club
            player_data[player_id]["club"] = clubs[club_id]

            print(f"Player {player_id} -> Found {len(player_data[player_id]['stats'])} stats entries.")

    print("Done fetching all player data and stats.")

    # 4) Insert/Upsert into DB
    print("Total players collected:", len(player_data))
    for pid, pdata in list(player_data.items())[:3]:
        print(f"Player ID: {pid}, Data: {pdata.get('data')}, Stats count: {len(pdata.get('stats', []))}")

    insert_player_data_to_db(player_data)

    print("All done!")

##############################
# Entry Point
##############################

if __name__ == "__main__":
    main()
