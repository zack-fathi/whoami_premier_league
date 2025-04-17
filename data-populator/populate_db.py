import os
import json
import time
import requests
import psycopg
from concurrent.futures import ThreadPoolExecutor, as_completed

# Config
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "whoami_db")
DB_USER = os.getenv("DB_USER", "whoami_user")
DB_PASS = os.getenv("DB_PASS", "whoami_password")
TRANSFERMARKT_API_URL = os.getenv("TRANSFERMARKT_API_URL", "http://transfermarkt-api:8000")

# DB setup
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
        image_url      TEXT,
        stats          JSONB,
        transfers      JSONB,
        achievements   JSONB
    );
    """
    with psycopg.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    ) as conn:
        conn.execute(create_table_sql)
        print("Table created.")

# Insert into DB
def insert_players(player_data):
    query = """
    INSERT INTO players (
        id, club, name, position, foot, date_of_birth, age, height,
        market_value, nationality, image_url, stats, transfers, achievements
    )
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (id) DO UPDATE SET
        club = EXCLUDED.club,
        name = EXCLUDED.name,
        position = EXCLUDED.position,
        foot = EXCLUDED.foot,
        date_of_birth = EXCLUDED.date_of_birth,
        age = EXCLUDED.age,
        height = EXCLUDED.height,
        market_value = EXCLUDED.market_value,
        nationality = EXCLUDED.nationality,
        image_url = EXCLUDED.image_url,
        stats = EXCLUDED.stats,
        transfers = EXCLUDED.transfers,
        achievements = EXCLUDED.achievements;
    """
    with psycopg.connect(
        host=DB_HOST, port=DB_PORT, dbname=DB_NAME, user=DB_USER, password=DB_PASS
    ) as conn:
        conn.autocommit = True
        with conn.cursor() as cur:
            cur.execute("TRUNCATE TABLE players;")
            for p in player_data:
                try:
                    cur.execute(query, (
                        p["id"], p["club"], p["name"], p["position"], p["foot"],
                        p["date_of_birth"], p["age"], p["height"],
                        p["market_value"], p["nationality"], p["image_url"],
                        json.dumps(p["stats"]), json.dumps(p["transfers"]),
                        json.dumps(p["achievements"])
                    ))
                    print(f"Inserted {p['id']} - {p['name']}")
                except Exception as e:
                    print(f"DB insert error for {p['id']}: {e}")

# Threaded fetch
def fetch_player_data(player_dict, club):
    pid = player_dict["id"]
    try:
        profile = requests.get(f"{TRANSFERMARKT_API_URL}/players/{pid}/profile").json()
        stats = requests.get(f"{TRANSFERMARKT_API_URL}/players/{pid}/stats").json().get("stats", [])
        transfers = requests.get(f"{TRANSFERMARKT_API_URL}/players/{pid}/transfers").json().get("transfers", [])
        achievements = requests.get(f"{TRANSFERMARKT_API_URL}/players/{pid}/achievements").json().get("achievements", [])
        
        nationality = profile.get("citizenship", [])
        return {
            "id": pid,
            "club": club["name"],
            "name": profile.get("name"),
            "position": profile.get("position", {}).get("main"),
            "foot": profile.get("foot"),
            "date_of_birth": profile.get("dateOfBirth"),
            "age": profile.get("age"),
            "height": profile.get("height"),
            "market_value": profile.get("marketValue"),
            "nationality": ", ".join(nationality) if isinstance(nationality, list) else nationality,
            "image_url": profile.get("imageUrl"),
            "stats": stats,
            "transfers": transfers,
            "achievements": achievements
        }
    except Exception as e:
        print(f"Failed to fetch data for {pid}: {e}")
        return None

# Main logic
def main():
    create_table_if_not_exists()
    time.sleep(5)

    resp = requests.get(f"{TRANSFERMARKT_API_URL}/competitions/GB1/clubs").json()
    clubs = {c["id"]: c for c in resp.get("clubs", [])}

    all_players = []
    for club_id, club in clubs.items():
        pdata = requests.get(f"{TRANSFERMARKT_API_URL}/clubs/{club_id}/players").json()
        players = pdata.get("players", [])

        print(f"Fetching {len(players)} from {club['name']}")

        with ThreadPoolExecutor(max_workers=6) as executor:
            futures = [executor.submit(fetch_player_data, p, club) for p in players]
            for future in as_completed(futures):
                result = future.result()
                if result:
                    all_players.append(result)

    print(f"Total players fetched: {len(all_players)}")
    insert_players(all_players)

if __name__ == "__main__":
    main()
