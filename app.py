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
        app.logger.info('Fetching artists...')
        artists = mongo.db.artists.find()
        artists_list = [{'_id': str(artist['_id']), 'name': artist['name']} for artist in artists]
        app.logger.info(f'Found {len(artists_list)} artists')
        return jsonify(artists_list)
    except Exception as e:
        app.logger.error(f'Error fetching artists: {str(e)}')
        return jsonify({'error': 'Internal Server Error'}), 500

@app.route('/api/artists', methods=['POST'])
def add_artist():
    try:
        name = request.json['name']
        artist_id = mongo.db.artists.insert_one({'name': name}).inserted_id
        return jsonify({'_id': str(artist_id), 'name': name}), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/artists/<id>', methods=['GET'])
def get_artist(id):
    try:
        artist = mongo.db.artists.find_one({'_id': ObjectId(id)})
        if artist:
            return jsonify({'_id': str(artist['_id']), 'name': artist['name']}), 200
        else:
            return jsonify({'message': 'Artist not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/artists/<id>', methods=['PUT'])
def update_artist(id):
    try:
        name = request.json['name']
        mongo.db.artists.update_one({'_id': ObjectId(id)}, {'$set': {'name': name}})
        return jsonify({'_id': id, 'name': name}), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/artists/<id>', methods=['DELETE'])
def delete_artist(id):
    try:
        result = mongo.db.artists.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 1:
            return jsonify({'message': 'Artist deleted'}), 200
        else:
            return jsonify({'message': 'Artist not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Routes for Albums
@app.route('/api/albums', methods=['GET'])
def get_albums():
    try:
        albums = mongo.db.albums.find()
        albums_list = [{'_id': str(album['_id']), 'title': album['title'], 'description': album['description']} for album in albums]
        return jsonify(albums_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/albums', methods=['POST'])
def add_album():
    try:
        title = request.json['title']
        description = request.json.get('description', '')
        artist_name = request.json['artist_name']  
        
        
        artist = mongo.db.artists.find_one({'name': artist_name})
        
        if not artist:
            # If artist not found, return an error message
            return jsonify({'error': f'Artist with name {artist_name} not found'}), 404
        
        
        album_id = mongo.db.albums.insert_one({
            'title': title,
            'artist': artist_name,
            'description': description
        }).inserted_id
        
        
        return jsonify({
            '_id': str(album_id),
            'title': title,
            'artist': artist_name,
            'description': description
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/albums/<album_id>', methods=['GET'])
def get_album(album_id):
    try:
        print(f"Fetching album with id: {album_id}")
        album = mongo.db.albums.find_one({'_id': ObjectId(album_id)})

        if album:
            response = {
                '_id': str(album['_id']),
                'title': album['title'],
                'description': album['description'],
                'artist': album['artist']
            }
            return jsonify(response), 200
        else:
            return jsonify({'message': f'Album not found with id {album_id}'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/albums/<id>', methods=['PUT'])
def update_album(id):
    try:
        title = request.json['title']
        description = request.json.get('description', '')
        artist_name = request.json['artist_name']  

        
        artist = mongo.db.artists.find_one({'name': artist_name})

        if not artist:
            return jsonify({'error': f'Artist with name {artist_name} not found'}), 404

        mongo.db.albums.update_one(
            {'_id': ObjectId(id)},
            {'$set': {'title': title, 'description': description, 'artist': artist_name}}
        )

        return jsonify({
            '_id': id,
            'title': title,
            'artist': artist_name,
            'description': description
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/albums/<id>', methods=['DELETE'])
def delete_album(id):
    try:
        result = mongo.db.albums.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 1:
            return jsonify({'message': 'Album deleted'}), 200
        else:
            return jsonify({'message': 'Album not found'}), 404
    except Exception as e:
        return jsonify({'error': str(e)}), 400


# Routes for Songs
@app.route('/api/songs', methods=['GET'])
def get_songs():
    try:
        songs = mongo.db.songs.find()
        songs_list = [{
            '_id': str(song['_id']),
            'title': song['title'],
            'length': song['length'],
            'album': song['album'] 
        } for song in songs]
        return jsonify(songs_list), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/songs', methods=['POST'])
def add_song():
    try:
        title = request.json['title']
        length = request.json['length']
        album_name = request.json['album_name']  
        artist_name = request.json['artist_name']  

        album = mongo.db.albums.find_one({'title': album_name})
        
        if not album:
            return jsonify({'error': f'Album with title {album_name} not found'}), 404
        
        if album['artist'] != artist_name:
            return jsonify({'error': f'Album {album_name} does not belong to artist {artist_name}'}), 400

        song_id = mongo.db.songs.insert_one({
            'title': title,
            'album': album_name,
            'artist': artist_name,
            'length': length
        }).inserted_id
        
        return jsonify({
            '_id': str(song_id),
            'title': title,
            'album': album_name,
            'artist': artist_name,
            'length': length
        }), 201
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/songs/<song_id>', methods=['GET'])
def get_song(song_id):
    try:
        print(f"Fetching song with id: {song_id}")
        song = mongo.db.songs.find_one({'_id': ObjectId(song_id)})

        if song:
            response = {
                '_id': str(song['_id']),
                'title': song['title'],
                'length': song['length'],
                'album': song['album'],
                'artist': song['artist']
            }
            return jsonify(response), 200
        else:
            return jsonify({'message': f'Song not found with id {song_id}'}), 404

    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/songs/<id>', methods=['PUT'])
def update_song(id):
    try:
        title = request.json['title']
        length = request.json['length']
        album_name = request.json['album_name'] 
        artist_name = request.json['artist_name'] 

        album = mongo.db.albums.find_one({'title': album_name})

        if not album:
            return jsonify({'error': f'Album with title {album_name} not found'}), 404
        
        if album['artist'] != artist_name:
            return jsonify({'error': f'Album {album_name} does not belong to artist {artist_name}'}), 400

        mongo.db.songs.update_one({'_id': ObjectId(id)}, {'$set': {
            'title': title,
            'album': album_name,
            'artist': artist_name,
            'length': length
        }})

        return jsonify({
            '_id': id,
            'title': title,
            'album': album_name,
            'artist': artist_name,
            'length': length
        }), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 400

@app.route('/api/songs/<id>', methods=['DELETE'])
def delete_song(id):
    try:
        result = mongo.db.songs.delete_one({'_id': ObjectId(id)})
        if result.deleted_count == 1:
            return jsonify({'message': 'Song deleted'}), 200
        else:
            return jsonify({'message': 'Song not found'}), 404
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