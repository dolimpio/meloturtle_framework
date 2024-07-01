// PlaylistForm.jsx
import React from 'react';
import PromptInput from './PromptInput';
import ModelDropdown from './ModelDropdown';
import NumSongsInput from './NumSongsInput';
import PopularitySlider from './PopularitySlider';
import GenreSelection from './GenreSelection';
import { Checkbox } from 'primereact/checkbox';
import { Button } from 'primereact/button';
import { Card } from 'primereact/card';
import '../styles/PlaylistForm.css'

const PlaylistForm = ({
    prompt, setPrompt, selectedModel, setSelectedModel, models, numSongs, setNumSongs,
    popularity, setPopularity, selectGenres, setSelectGenres, genres, genreColors,
    selectedGenres, toggleGenreSelection, handleSubmit
}) => {
    const generate_button = (
        <>
            <Button className="generate-button" label="Generate playlist" icon="pi pi-check" onClick={handleSubmit} style={{margin: "0rem"}}/>
        </>
    )

    return (
        < div className="p-col-12 p-md-6" >
            <Card title="Generate your Playlist:" footer={generate_button} style={{marginBottom: "0rem"}}>
                <PromptInput prompt={prompt} setPrompt={setPrompt} />
                <ModelDropdown selectedModel={selectedModel} setSelectedModel={setSelectedModel} models={models} />
                <NumSongsInput numSongs={numSongs} setNumSongs={setNumSongs} />
                <PopularitySlider popularity={popularity} setPopularity={setPopularity} />
                <div className="p-field-checkbox p-3">
                    <Checkbox inputId="selectGenres" checked={selectGenres} onChange={(e) => setSelectGenres(e.checked)} />
                    <label htmlFor="selectGenres"> Select music genres myself</label>
                </div>
                {selectGenres && <GenreSelection genres={genres} genreColors={genreColors} selectedGenres={selectedGenres} toggleGenreSelection={toggleGenreSelection} />}
            </Card>
        </div >
    )

};

export default PlaylistForm;
