import os
import psycopg
import requests
import schedule
import time

# Load environment variables
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "5432")
DB_NAME = os.getenv("DB_NAME", "whoami_db")
DB_USER = os.getenv("DB_USER", "whoami_user")
DB_PASS = os.getenv("DB_PASS", "whoami_password")
TRANSFERMARKT_API_URL = os.getenv("TRANSFERMARKT_API_URL", "http://transfermarkt-api:8000")

# Notes
# PREMIER LEAGUE HAS ID "GB1"

# fetch all teams in the premier league
# GET /competitions/GB1/clubs
# clubs = resp.get("clubs") # clubs is a list of dictionaries in the json resp
# club_ids = [club["id"] for club in clubs]
# GET /clubs/{club_id}/players
# "players": [
#     {
#       "id": "238223",
#       "name": "Ederson",
#       "position": "Goalkeeper",
#       "dateOfBirth": "1993-08-17",
#       "age": 31,
#       "nationality": [
#         "Brazil",
#         "Portugal"
#       ],
#       "height": 188,
#       "foot": "left",
#       "joinedOn": "2017-07-01",
#       "signedFrom": "SL Benfica",
#       "contract": "2026-06-30",
#       "marketValue": 30000000
#     }, ...]


def get_competition_clubs(competition_id):
    """Fetches all clubs in a competition from the Transfermarkt API."""

    url = f"{TRANSFERMARKT_API_URL}/competitions/{competition_id}/clubs"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching clubs for competition {competition_id}: {response.status_code}")
        return None

def get_club_players(club_id):
    """Fetches club data from the Transfermarkt API."""

    url = f"{TRANSFERMARKT_API_URL}/clubs/{club_id}/players"
    response = requests.get(url)

    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching club {club_id}: {response.status_code}")
        return None

def get_player_stats(player_id):
    """Fetches player data from the Transfermarkt API."""
    url = f"{TRANSFERMARKT_API_URL}/players/{player_id}/stats"
    
    response = requests.get(url)
    if response.status_code == 200:
        print(response.json()['stats'])
        return response.json()
    else:
        print(f"Error fetching player {player_id}: {response.status_code}")
        return None
    

# def get_player_data(player_id):
#     """Fetches player data from the Transfermarkt API."""
#     url = f"{TRANSFERMARKT_API_URL}/players/{player_id}"
#     headers = {"Authorization": f"Bearer {TRANSFERMARKT_API_KEY}"}
#     response = requests.get(url, headers=headers)

#     if response.status_code == 200:
#         return response.json()
#     else:
#         print(f"Error fetching player {player_id}: {response.status_code}")
#         return None

# def update_database():
#     """Updates player data in the Postgres database."""
#     print("Starting database update...")
#     conn = psycopg2.connect(
#         host=DB_HOST,
#         port=DB_PORT,
#         dbname=DB_NAME,
#         user=DB_USER,
#         password=DB_PASS
#     )
#     conn.autocommit = True
#     cur = conn.cursor()

#     # List of player IDs to update (this should ideally be dynamic)
#     player_ids = [1, 2, 3]  # Example

#     for player_id in player_ids:
#         data = get_player_data(player_id)
#         if data:
#             cur.execute("""
#                 INSERT INTO players (id, name, nationality, position, current_team, total_goals, total_assists, total_appearances)
#                 VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
#                 ON CONFLICT (id)
#                 DO UPDATE SET 
#                     name = excluded.name,
#                     nationality = excluded.nationality,
#                     position = excluded.position,
#                     current_team = excluded.current_team,
#                     total_goals = excluded.total_goals,
#                     total_assists = excluded.total_assists,
#                     total_appearances = excluded.total_appearances;
#             """, (
#                 data["id"],
#                 data["name"],
#                 data["nationality"],
#                 data["position"],
#                 data["current_team"],
#                 data["total_goals"],
#                 data["total_assists"],
#                 data["total_appearances"]
#             ))

#     cur.close()
#     conn.close()
#     print("Database update completed.")

# # Schedule the update to run daily at 3 AM
# schedule.every().day.at("03:00").do(update_database)

if __name__ == "__main__":
    
    resp = get_competition_clubs("GB1")
    clubs = resp.get("clubs")
    club_ids = [club["id"] for club in clubs]
    players = []
    for club_id in club_ids:
        data = get_club_players(club_id)
        data = [id for id in data["players"]]
        players.append(data)   

    player_data = []  
    for id in players:
        player_data.append(get_player_stats(id))
    print("Done")
    
    # schedule.run_pending()
    # time.sleep(60)  # Check every minute
