import React from 'react';
import { Slider } from 'primereact/slider';

const PopularitySlider = ({ popularity, setPopularity }) => (
    <div className="p-field p-3">
        <label htmlFor="popularity">Popularity: </label>
        <Slider id="popularity" value={popularity} onChange={(e) => setPopularity(e.value)} />
    </div>
);

export default PopularitySlider;