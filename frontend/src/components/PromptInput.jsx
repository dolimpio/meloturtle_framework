import React from 'react';
import { InputText } from 'primereact/inputtext';

const PromptInput = ({ prompt, setPrompt }) => (
    <div className="p-field p-3">
        <label htmlFor="prompt">Prompt: </label>
        <InputText id="prompt" value={prompt} onChange={(e) => setPrompt(e.target.value)} placeholder="Write your promp" />
    </div>
);

export default PromptInput;