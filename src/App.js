import React, { useState, useEffect } from 'react';
import axios from 'axios';
import ArtistsList from './ArtistsList';
import AlbumsList from './AlbumsList';
import SongsList from './SongsList';
import styles from './App.module.css';

function App() {
  const [searchQuery, setSearchQuery] = useState('');
  const [searchResults, setSearchResults] = useState({ artists: [], albums: [], songs: [] });
  const [suggestions, setSuggestions] = useState([]);
  const [error, setError] = useState(null);

  const handleSearch = async () => {
    try {
      const trimmedQuery = searchQuery.trim().replace(/\s+/g, ' '); // Trim and replace multiple spaces with a single space
      const response = await axios.get(`http://localhost:5000/api/search?q=${encodeURIComponent(trimmedQuery)}`);
      setSearchResults(response.data || { artists: [], albums: [], songs: [] });
      setSuggestions([]);
      setError(null);
    } catch (error) {
      console.error('Error fetching search results:', error);
      setError('Failed to fetch search results. Please try again later.');
      setSearchResults({ artists: [], albums: [], songs: [] });
    }
  };

  const fetchSuggestions = async (query) => {
    try {
      const response = await axios.get(`http://localhost:5000/api/suggestions?q=${encodeURIComponent(query)}`);
      setSuggestions(response.data.suggestions || []);
    } catch (error) {
      console.error('Error fetching suggestions:', error);
      setSuggestions([]);
    }
  };

  useEffect(() => {
    if (searchQuery) {
      fetchSuggestions(searchQuery);
    } else {
      setSuggestions([]);
    }
  }, [searchQuery]);

  const handleClear = () => {
    setSearchQuery('');
    setSearchResults({ artists: [], albums: [], songs: [] });
    setSuggestions([]);
    setError(null);
  };

  return (
    <div className={styles.appContainer}>
      <h1 className={styles.appTitle}>Sergiulica's Playlist</h1>
      <div>
        <input
          type="text"
          value={searchQuery}
          onChange={(e) => setSearchQuery(e.target.value)}
          placeholder="Search..."
          className={styles.searchInput}
        />
        <button onClick={handleSearch} className={styles.searchButton}>Search</button>
        <button onClick={handleClear} className={`${styles.searchButton} ${styles.clearButton}`}>Clear</button>
      </div>
      {/* Error Handling */}
      {error && <p className={styles.error}>{error}</p>}
      {/* Autocomplete suggestions */}
      {suggestions.length > 0 && (
        <ul className={styles.suggestionsList}>
          {suggestions.map((suggestion, index) => (
            <li
              key={index}
              className={styles.suggestionItem}
              onClick={() => setSearchQuery(suggestion.title)}
            >
              {suggestion.type === 'artist' ? suggestion.title : `${suggestion.title} - ${suggestion.artist}`}
            </li>
          ))}
        </ul>
      )}
      {/* Display search results */}
      <div>
        {searchResults.artists && searchResults.artists.length > 0 && (
          <div>
            <h2>Artists</h2>
            <ArtistsList artists={searchResults.artists} className={styles.artistsList} />
          </div>
        )}
        {searchResults.albums && searchResults.albums.length > 0 && (
          <div>
            <h2>Albums</h2>
            <AlbumsList albums={searchResults.albums} className={styles.albumsList} />
          </div>
        )}
        {searchResults.songs && searchResults.songs.length > 0 && (
          <div>
            <h2>Songs</h2>
            <SongsList songs={searchResults.songs} className={styles.songsList} />
          </div>
        )}
        {/* No Results Found */}
        {searchQuery && !searchResults.artists.length && !searchResults.albums.length && !searchResults.songs.length && (
          <p className={styles.noResults}>No results found.</p>
        )}
      </div>
    </div>
  );
}

export default App;