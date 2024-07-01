import React from 'react';
import { Button } from 'primereact/button';
import { Card } from 'primereact/card';
import { useNavigate } from 'react-router-dom';
import '../styles/ErrorPage.css';

const ErrorPage = () => {
    const navigate = useNavigate();

    return (
        <div className="error-element">
            <Card title="Oops! Something went wrong" subTitle="An unexpected error has occurred">
                <Button label="Go to Home" icon="pi pi-home" onClick={() => {navigate('/')}} />
            </Card>
        </div>
    );
};

export default ErrorPage;
