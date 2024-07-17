import React from 'react';
import SongsList from './SongsList'; 

const AlbumsList = ({ albums }) => (
  <div>
    {albums.map(album => (
      <div key={album.title}>
        <h3>{album.title}</h3>
        <p>{album.description}</p>
        {album.songs && album.songs.length > 0 && (
          <SongsList songs={album.songs} />
        )}
      </div>
    ))}
  </div>
);

export default AlbumsList;