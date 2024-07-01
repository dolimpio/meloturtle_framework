import React from 'react';
import { Card } from 'primereact/card';
import { Button } from 'primereact/button';

const ModelCard = ({ model }) => {

    const footer = (
        <span>
            <Button label="Learn More" icon="pi pi-info" className="p-button-secondary" style={{ marginRight: '0.5em' }} />
        </span>
    );

    return (
        <Card title={model.name} subTitle={`Version: ${model.version}`} style={{ width: '100%', marginBottom: '2em',  background: "#17212f"}} footer={footer}>
            <p>{model.description}</p>
        </Card>
    );
};
 export default ModelCard;

