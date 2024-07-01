import React, { useState, useEffect, useRef, useCallback } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch } from 'react-redux';
import { useCookies } from 'react-cookie';

import { useAuth } from "../provider/AuthProvider";
import { useToast } from '../provider/ToastProvider';


import ModelsService from '../service/ModelsService';

import { Card } from 'primereact/card';
import { Button } from 'primereact/button';
import { ProgressSpinner } from 'primereact/progressspinner';
import ModelList from '../components/ModelList.jsx'

const RedirectHandler = () => {
    // Uses cookie to set user so next actions can use token
    const [cookies] = useCookies(['ml-auth-jwt']);
    const { setToken, isTokenSet } = useAuth();

    const [loading, setLoading] = useState(true);
    const [localModels, setLocalModels] = useState(null);
    const { showToast } = useToast();

    const navigate = useNavigate();


    const fetchModels = async () => {
        setLoading(true);
        try {
            const response = await ModelsService.getModels();
            setLocalModels(response.data)

        } catch (error) {
            showToast({ severity: 'error', summary: 'Error', detail: 'Error fetching models. Please try again later.', life: 3000 });
            console.error('Error fetching models:', error);
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        setLoading(true);

        const token = cookies["ml-auth-jwt"];
        console.log("Cookie token: ", token);
        if (token) {
            setToken(token);
            console.log("Token set: ", token);
        } else {
            showToast({ severity: 'warn', summary: 'Warning', detail: 'No token found. Redirecting to login.', life: 3000 });
            navigate('/login'); // Redirect to login page if no token is found
            return;
        }
        setLoading(false);


    }, [cookies, setToken, navigate]);


    useEffect(() => {
        if (isTokenSet) {
            console.log("Token is set, fetching models...");
            fetchModels();
        }
    }, [isTokenSet]);

    return (
        <div className="p-grid p-justify-center p-align-center" style={{ minHeight: '100vh', padding: '2rem' }}>
            <div className="p-col-12 p-md-8">
                <Card title="Welcome!">
                    {loading ? (
                        <div className="p-text-center">
                            <h2>Logging you in...</h2>
                            <p>Please wait a moment.</p>
                            <ProgressSpinner />
                        </div>
                    ) : (
                        <div>
                            <h1>Recommender Models</h1>
                            {localModels ? (
                                <ModelList models={localModels} />
                            ) : (
                                <p>No models available. Please try again later.</p>
                            )}
                            <div>
                                <p>You are now logged in, if you want to know more about us and the models:</p>
                                <Button label="Explore!" icon="pi pi-arrow-right" className="p-button-success" onClick={() => navigate('/about')} />
                                <Button label="Go straight to the action!" icon="pi pi-arrow-right" className="p-button-success" onClick={() => navigate('/generator')} />
                            </div>
                        </div>
                    )}
                </Card>
            </div>
        </div>
    );
};

export default RedirectHandler;
