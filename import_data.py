import json
from pymongo import MongoClient

# Connect to the local MongoDB instance
client = MongoClient('localhost', 27017)
db = client.musiclibrary  # Ensure this matches your database name in MongoDB Compass

# Load JSON data from the specified path
json_file_path = r'D:\Proiect Darwin\data.json'

with open(json_file_path, 'r', encoding='utf-8') as file:
    data = json.load(file)

# Insert data into the collections
for artist_data in data:
    artist = {"name": artist_data["name"]}
    db.artists.insert_one(artist)
    
    for album_data in artist_data["albums"]:
        album = {
            "title": album_data["title"],
            "artist": artist_data["name"],
            "description": album_data["description"]
        }
        db.albums.insert_one(album)
        
        for song_data in album_data["songs"]:
            song = {
                "title": song_data["title"],
                "album": album_data["title"],
                "artist": artist_data["name"],
                "length": song_data["length"]
            }
            db.songs.insert_one(song)

print("Data imported successfully!")