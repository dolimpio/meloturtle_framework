import React from 'react';
import { ProgressSpinner } from 'primereact/progressspinner';
import '../styles/LoadingSpinner.css';

const LoadingSpinner = () => (
    <div className="loading-spinner">
        <h2>Loading...</h2>
        <div className='spinner-container'>
            <ProgressSpinner />
        </div>
    </div>
);

export default LoadingSpinner;