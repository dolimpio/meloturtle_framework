import React from 'react';
import { Card } from 'primereact/card';
import { ScrollPanel } from 'primereact/scrollpanel';
import '../styles/GenreSelection.css';

const GenreSelection = ({ genres, genreColors, selectedGenres, toggleGenreSelection }) => (
    <div className="p-field p-3">
        <Card subTitle="Choose a max of 5 genres:" className='genre-card'>
            <ScrollPanel style={{ width: '100%', height: '100px', marginTop: '10px' }}>
                <div id="genres" className="genre-container">
                    {genres.map((genre, index) => (
                        <div key={index}
                            className={`genre-box ${selectedGenres.includes(genre) ? 'selected' : ''}`}
                            style={{ backgroundColor: genreColors[genre] }}
                            onClick={() => toggleGenreSelection(genre)}>
                            {genre}
                        </div>
                    ))}
                </div>
            </ScrollPanel>
        </Card>
    </div>
);

export default GenreSelection;