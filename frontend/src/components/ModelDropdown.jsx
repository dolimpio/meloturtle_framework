import React from 'react';
import { Dropdown } from 'primereact/dropdown';

const ModelDropdown = ({ selectedModel, setSelectedModel, models }) => (
    <div className="p-field p-3">
        <label htmlFor="model">Model: </label>
        <Dropdown id="model" value={selectedModel} options={models} optionLabel="name" onChange={(e) => setSelectedModel(e.value)} placeholder="Select a model" />
    </div>
);

export default ModelDropdown;