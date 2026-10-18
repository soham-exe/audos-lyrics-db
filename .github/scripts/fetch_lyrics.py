import sys
import json
import requests

def fetch_lyrica(title, artist):
    try:
        resp = requests.get("https://wilooper-lyrica.hf.space/lyrics/", params={
            "artist": artist,
            "song": title,
            "timestamps": "true"
        }, timeout=15)
        
        print(f"[Debug] API Status: {resp.status_code}")
        
        if resp.status_code == 200:
            data = resp.json()
            print(f"[Debug] API Response: {data}")
            
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
        # The issue title is "Song Title - Artist Name"
        title, artist = title_artist.split(" - ", 1)
    except:
        print("Invalid title format. Expected 'Title - Artist'")
        sys.exit(0)

    print(f"Searching for: '{title}' by '{artist}'")
    lyrics = fetch_lyrica(title, artist)

    if lyrics:
        try:
            with open("lyrics_db.json", "r") as f:
                db = json.load(f)
        except:
            db = {}
        
        # Use the exact same key format as the Rust app
        key = f"{title.lower().strip()}|{artist.lower().strip()}"
        db[key] = lyrics
        
        with open("lyrics_db.json", "w") as f:
            json.dump(db, f, indent=2)
        
        print(f"Success! Lyrics added to DB under key: {key}")
    else:
        print("Could not fetch lyrics automatically. The database was not updated.")