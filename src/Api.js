const API_URL = 'http://localhost:5000/api';

export const fetchArtists = async () => {
    try {
        const response = await fetch(`${API_URL}/artists`);
        if (!response.ok) {
            throw new Error(`Failed to fetch artists: ${response.statusText}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error('Error fetching artists:', error);
        throw error; // Re-throw the error to be handled by the caller
    }
};

export const fetchAlbumsByArtist = async (artistName) => {
    try {
        const response = await fetch(`${API_URL}/albums/${artistName}`);
        if (!response.ok) {
            throw new Error(`Failed to fetch albums for ${artistName}: ${response.statusText}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`Error fetching albums for ${artistName}:`, error);
        throw error; // Re-throw the error to be handled by the caller
    }
};

export const fetchSongsByAlbum = async (albumName) => {
    try {
        const response = await fetch(`${API_URL}/songs/${albumName}`);
        if (!response.ok) {
            throw new Error(`Failed to fetch songs for ${albumName}: ${response.statusText}`);
        }
        const data = await response.json();
        return data;
    } catch (error) {
        console.error(`Error fetching songs for ${albumName}:`, error);
        throw error; // Re-throw the error to be handled by the caller
    }
};