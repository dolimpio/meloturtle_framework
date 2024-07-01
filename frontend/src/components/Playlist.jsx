import React from 'react';
import { Card } from 'primereact/card';
import { Button } from 'primereact/button';

import '../styles/Playlist.css';

const Playlist = ({ playlist, onDelete, showDelete }) => {
    // Check if playlist data is available
    if (!playlist || !playlist.config || !playlist.context) {
        return (
            <Card key={playlist.context.spotify_id} title="No Data Available" style={{ marginBottom: '1em', textAlign: 'center' }}>
                <p>Sorry, no playlist data is available at the moment.</p>
            </Card>
        );
    }
    // Format the creation date to be more human-readable
    const formattedDate = new Date(playlist.context.created_at).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: 'numeric',
        minute: 'numeric'
    });
    return (
        <Card key={playlist.context.spotify_id} title={`Prompt: ${playlist.prompt}`} className="playlist-card">
            <div className="playlist-info">
                <div className="playlist-details">
                    <p><strong>Model:</strong> {playlist.config.model}</p>
                    <p><strong>Popularity:</strong> {playlist.config.popularity}</p>
                    <p><strong>Number of Songs:</strong> {playlist.config.num_songs}</p>
                    <p><strong>Creation Date:</strong> {formattedDate}</p>
                </div>
                <div className="playlist-embed">
                    <iframe
                        className="responsive-iframe"
                        allowFullScreen
                        allow="encrypted-media; fullscreen; picture-in-picture"
                        loading="lazy"
                        src={`https://open.spotify.com/embed/playlist/${playlist.context.spotify_id}`}
                        title={`Spotify Playlist - ${playlist.prompt}`}
                    ></iframe>
                </div>
            </div>
            <div className='playlist-footer'>
                {showDelete && (
                    <div className="button-wrapper">
                        <Button
                            label="Delete"
                            icon="pi pi-trash"
                            onClick={() => onDelete(playlist.context.spotify_id)}
                            className="p-button-danger custom-delete-button"
                        />
                    </div>
                )}
                    <div className="selected-genres">
                        {playlist.config.genres.map((genre, index) => (
                            <div key={index} className="genre-tag">
                                {genre}
                            </div>
                        ))}
                    </div>

            </div>

        </Card>
    );
};

export default Playlist;

