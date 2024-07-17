import React from 'react';
import AlbumsList from './AlbumsList';

const ArtistsList = ({ artists }) => (
  <div>
    {artists.map(artist => (
      <div key={artist._id}>
        <h2>{artist.name}</h2>
        <AlbumsList albums={artist.albums} /> {/* Display albums first */}
      </div>
    ))}
  </div>
);

export default ArtistsList;