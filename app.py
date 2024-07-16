from flask import Flask, request, jsonify
from flask_cors import CORS
from flask_pymongo import PyMongo
from bson.objectid import ObjectId

app = Flask(__name__)
app.config["MONGO_URI"] = "mongodb://localhost:27017/musiclibrary"
mongo = PyMongo(app)
CORS(app)

# Routes for artists
@app.route('/api/artists', methods=['GET'])
def get_artists():
    try:
        artists = mongo.db.artists.find()
        artists_list = [{'_id': str(artist['_id']), 'name': artist['name']} for artist in artists]
        return jsonify(artists_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Routes for albums
@app.route('/api/albums', methods=['GET'])
def get_albums():
    try:
        albums = mongo.db.albums.find()
        albums_list = [{'_id': str(album['_id']), 'title': album['title'], 'description': album['description']} for album in albums]
        return jsonify(albums_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Routes for songs
@app.route('/api/songs', methods=['GET'])
def get_songs():
    try:
        songs = mongo.db.songs.find()
        songs_list = [{
            '_id': str(song['_id']),
            'title': song['title'],
            'length': song['length'],
            'album': song['album']  # Assuming album is the name of the album
        } for song in songs]
        return jsonify(songs_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Route for searching
@app.route('/api/search', methods=['GET'])
def search():
    try:
        query = request.args.get('q')

        if not query:
            # If query is empty, return an empty response
            return jsonify({'artists': [], 'albums': [], 'songs': []}), 200

        # Search for artists
        artists = list(mongo.db.artists.find({'name': {'$regex': query, '$options': 'i'}}))
        artists_with_albums = []
        for artist in artists:
            albums = list(mongo.db.albums.find({'artist': artist['name']}))
            artist_data = {
                '_id': str(artist['_id']),
                'name': artist['name'],
                'albums': [{
                    '_id': str(album['_id']),
                    'title': album['title'],
                    'description': album.get('description', '')
                } for album in albums]
            }
            artists_with_albums.append(artist_data)

        # Search for albums
        albums = list(mongo.db.albums.find({'title': {'$regex': query, '$options': 'i'}}))
        albums_with_songs = []
        for album in albums:
            songs = list(mongo.db.songs.find({'album': album['title']}))
            album_data = {
                '_id': str(album['_id']),
                'title': album['title'],
                'description': album.get('description', ''),
                'songs': [{
                    '_id': str(song['_id']),
                    'title': song['title'],
                    'length': song['length'],
                    'artist': song['artist']
                } for song in songs]
            }
            albums_with_songs.append(album_data)

        # Search for songs
        songs = list(mongo.db.songs.find({'title': {'$regex': query, '$options': 'i'}}))
        songs_data = [{
            '_id': str(song['_id']),
            'title': song['title'],
            'length': song['length'],
            'album': song['album'],
            'artist': song['artist']
        } for song in songs]

        # Construct the response JSON
        response = {
            'artists': artists_with_albums,
            'albums': albums_with_songs,
            'songs': songs_data
        }

        return jsonify(response), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Route for autocomplete suggestions
@app.route('/api/suggestions', methods=['GET'])
def suggestions():
    try:
        query = request.args.get('q')
        if not query:
            return jsonify({'suggestions': []}), 200

        # Search for suggestions
        suggestions = []

        # Search for artists suggestions
        artists = list(mongo.db.artists.find({'name': {'$regex': query, '$options': 'i'}}).limit(5))
        for artist in artists:
            suggestions.append({'title': artist['name'], 'type': 'artist'})

        # Search for albums suggestions
        albums = list(mongo.db.albums.find({'title': {'$regex': query, '$options': 'i'}}).limit(5))
        for album in albums:
            suggestions.append({'title': album['title'], 'artist': album['artist'], 'type': 'album'})

        # Search for songs suggestions
        songs = list(mongo.db.songs.find({'title': {'$regex': query, '$options': 'i'}}).limit(5))
        for song in songs:
            suggestions.append({'title': song['title'], 'artist': song['artist'], 'album': song['album'], 'type': 'song'})

        return jsonify({'suggestions': suggestions}), 200

    except Exception as e:
        return jsonify({'error': str(e)}), 400

# Welcome route
@app.route('/')
def home():
    return "Welcome to the Digital Music Library API!"

if __name__ == '__main__':
    app.run(debug=True)