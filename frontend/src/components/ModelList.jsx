import React from 'react';
import ModelCard from '../components/ModelCard.jsx';

const ModelList = ({ models }) => {
    return (
        <div className="p-grid p-nogutter p-justify-center">
            {models && models.length > 0 ? (
                models.map((model, index) => (
                    <div className="p-col-12 p-md-6 p-lg-4" key={index}>
                        <ModelCard model={model} />
                    </div>
                ))
            ) : (
                <p>No models available at the moment.</p>
            )}
        </div>
    );
};

export default ModelList;
