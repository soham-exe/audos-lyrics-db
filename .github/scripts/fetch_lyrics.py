import sys
import json
import requests
import os

def fetch_lyrica(title, artist):
    try:
        resp = requests.get("https://wilooper-lyrica.hf.space/lyrics/", params={
            "artist": artist,
            "song": title,
            "timestamps": "true"
        }, timeout=15)
        
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success":
                lyrics = data.get("data", {}).get("lyrics", "")
                if lyrics:
                    return lyrics
    except Exception as e:
        print(f"[Error] Exception occurred: {e}")
    return None

if __name__ == "__main__":
    title_artist = sys.argv[1]
    try:
        title, artist = title_artist.split(" - ", 1)
    except:
        print("Invalid title format. Expected 'Title - Artist'")
        sys.exit(0)

    title = title.strip()
    artist = artist.strip()
    key = f"{title.lower()}|{artist.lower()}"

    # 1. Load the existing DB
    try:
        with open("lyrics_db.json", "r") as f:
            db = json.load(f)
    except:
        db = {}

    # 2. Check if it already exists
    if key in db:
        print(f"ALREADY_EXISTS: Lyrics for '{title}' are already in the database.")
        sys.exit(0) # Exit cleanly, the YAML will handle closing the issue

    # 3. If not, fetch it
    print(f"Searching for: '{title}' by '{artist}'")
    lyrics = fetch_lyrica(title, artist)

    if lyrics:
        db[key] = lyrics
        with open("lyrics_db.json", "w") as f:
            json.dump(db, f, indent=2)
        print(f"Success! Lyrics added to DB under key: {key}")
    else:
        print("Could not fetch lyrics automatically. The database was not updated.")
        sys.exit(1) # Exit with error so the Action fails visibly