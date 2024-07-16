const API_URL = 'http://localhost:5000/api';

export const fetchArtists = async () => {
    const response = await fetch(`${API_URL}/artists`);
    const data = await response.json();
    return data;
};

export const fetchAlbumsByArtist = async (artistName) => {
    const response = await fetch(`${API_URL}/albums/${artistName}`);
    const data = await response.json();
    return data;
};

export const fetchSongsByAlbum = async (albumName) => {
    const response = await fetch(`${API_URL}/songs/${albumName}`);
    const data = await response.json();
    return data;
};