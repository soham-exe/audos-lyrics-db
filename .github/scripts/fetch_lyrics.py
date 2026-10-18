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
        }, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            if data.get("status") == "success":
                return data["data"]["lyrics"]
    except:
        pass
    return None

if __name__ == "__main__":
    title_artist = sys.argv[1]
    try:
        title, artist = title_artist.split(" - ", 1)
    except:
        print("Invalid title format")
        sys.exit(0)

    print(f"Searching for: {title} by {artist}")
    lyrics = fetch_lyrica(title, artist)

    if lyrics:
        with open("lyrics_db.json", "r") as f:
            db = json.load(f)
        
        # Use a unique key
        key = f"{title.lower().strip()}|{artist.lower().strip()}"
        db[key] = lyrics
        
        with open("lyrics_db.json", "w") as f:
            json.dump(db, f, indent=2)
        
        print(f"Success! Lyrics added to DB.")
    else:
        print("Could not fetch lyrics automatically.")
        # Optionally leave the issue open for manual review