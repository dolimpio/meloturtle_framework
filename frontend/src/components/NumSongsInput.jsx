import React from 'react';
import { InputNumber } from 'primereact/inputnumber';

const NumSongsInput = ({ numSongs, setNumSongs }) => (
    <div className="p-field p-3">
        <label htmlFor="numSongs">Number of Songs: </label>
        <InputNumber id="numSongs" value={numSongs} onValueChange={(e) => setNumSongs(e.value)} />
    </div>
);

export default NumSongsInput;