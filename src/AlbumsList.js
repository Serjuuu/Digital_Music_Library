import React from 'react';
import SongsList from './SongsList'; // Adjust import path as necessary

const AlbumsList = ({ albums }) => (
  <div>
    {albums.map(album => (
      <div key={album.title}>
        <h3>{album.title}</h3>
        <p>{album.description}</p>
        {/* Ensure songs exist before rendering SongsList */}
        {album.songs && album.songs.length > 0 && (
          <SongsList songs={album.songs} />
        )}
      </div>
    ))}
  </div>
);

export default AlbumsList;