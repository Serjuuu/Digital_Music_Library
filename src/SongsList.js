import React from 'react';
import styles from './App.module.css'; // Ensure correct path to your CSS module

const SongsList = ({ songs }) => (
  <ul>
    {songs.map((song, index) => (
      <li key={index} className={styles.songItem}>
        {song.title} - {song.artist} ({song.length})
      </li>
    ))}
  </ul>
);

export default SongsList;