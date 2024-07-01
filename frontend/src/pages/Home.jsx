import React from 'react';
import { useNavigate } from "react-router-dom";
import { Button } from 'primereact/button';
import { Card } from 'primereact/card';

import '../styles/Home.css'; // Make sure to create and import this CSS file
import Workout from '../assets/situations/workout-img.png'
import Party from '../assets/situations/party-img.png'
import Focus from '../assets/situations/focus-img.png'

const Home = () => {
    const navigate = useNavigate();

    const situations = [
        { title: 'Workout', imgSrc: Workout },
        { title: 'Party', imgSrc: Party },
        { title: 'Focus', imgSrc: Focus }
    ];

    return (
        <div className="home-container grid grid-nogutter surface-0 text-800">
            <div className="col-12 md:col-6 text-center md:text-left flex align-items-center justify-content-center">
                <section>
                    <h1 className="block font-bold mb-1">Get recommendations</h1>
                    <h2 className="text-primary font-bold mb-3">you want</h2>
                    <p className="mt-0 mb-4 text-700 line-height-3">
                        Describe what you need and ee will do the rest!
                        Get your playlist exactly how you want it.
                    </p>
                    <Button label="Try it out" type="button" className="mr-3 p-button-raised p-button-primary p-button-lg" onClick={() => { navigate('/generator') }} />
                </section>
            </div>
            <div className="col-12 md:col-6 overflow-hidden hero-image-container">
                <img
                    src="https://images.pexels.com/photos/1618606/pexels-photo-1618606.jpeg"
                    alt="hero-1"
                    className="hero-image"
                />
            </div>
            <div className="col-12 situations-container">
                <h2 className="text-4xl font-bold mb-3 text-center">Generate Playlists for Every Occasion</h2>
                <div className="situations-grid">
                    {situations.map((situation, index) => (
                        <Card key={index} className="situation-item">
                            <img src={situation.imgSrc} alt={situation.title} className="situation-image" />
                            <p className="situation-title">{situation.title}</p>
                        </Card>
                    ))}
                </div>
            </div>
        </div>
    );
}

export default Home;
