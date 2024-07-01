import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { useDispatch, useSelector } from 'react-redux';
import { useAuth } from "../provider/AuthProvider";
import { useToast } from '../provider/ToastProvider';

import PlaylistService from '../service/PlaylistService.js';
import GenresService from '../service/GenresService.js';
import ModelsService from '../service/ModelsService.js';


import { setPlaylist, clearPlaylist } from '../store/features/playlist/playlistSlice';

import LoadingSpinner from '../components/LoadingSpinner';
import PlaylistForm from '../components/PlaylistForm';
import ModelList from '../components/ModelList';
import { Card } from 'primereact/card';


import '../styles/Generator.css'

const Generator = () => {
    const [prompt, setPrompt] = useState('');
    const [selectedModel, setSelectedModel] = useState(null);
    const [localModels, setLocalModels] = useState(null);
    const [numSongs, setNumSongs] = useState(10);
    const [popularity, setPopularity] = useState(50);
    const [selectGenres, setSelectGenres] = useState(false);
    const [selectedGenres, setSelectedGenres] = useState([]);
    const [genreColors, setGenreColors] = useState({});
    const [genres, setGenres] = useState([]);
    const [loading, setLoading] = useState(true);
    const playlist = useSelector((state) => state.playlist.generated_playlist);
    const { showToast } = useToast();
    const { token, isTokenSet } = useAuth();
    const navigate = useNavigate();
    const dispatch = useDispatch();

    const fetchGenres = async () => {
        setLoading(true);
        try {
            const response = await GenresService.getGenres();

            setGenres(response.data);
            setGenreColors(generateGenreColors(response.data));
        } catch (error) {
            showToast({ severity: 'error', summary: 'Error', detail: 'Error fetching genres. Please try again later.', life: 3000 });
            console.error('Error fetching genres:', error);
        } finally {
            setLoading(false);
        }
    };

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
        if (isTokenSet) {
            fetchGenres();
            if (!localModels) {
                fetchModels();
            }
        }

        if (playlist && localModels && genres) {
            setPrompt(playlist.prompt);
            const foundModel = localModels.find(model => model.name === playlist.config.model);
            if (foundModel) {
                setSelectedModel(foundModel);
            }
            if (Boolean(playlist.config.generate_genres)) {
                setSelectGenres(Boolean(playlist.config.generate_genres));
                setSelectedGenres(playlist.config.genres);
            } else {
                setSelectGenres(Boolean(playlist.config.generate_genres));
                setSelectedGenres([]);
            }
            setNumSongs(playlist.config.num_songs);
            setPopularity(playlist.config.popularity);
        }
        setLoading(false);


    }, [playlist, localModels, token, isTokenSet]);
    const addPlaylist = (playlist) => {
        return (dispatch, getState) => {
            const stateBefore = getState();
            console.log(`Playlist before: ${stateBefore.playlist}`);
            dispatch(setPlaylist(playlist));
            const stateAfter = getState();
            console.log(`Playlist after: ${stateAfter.playlist}`);
        }
    }

    const handleSubmit = () => {
        if (!prompt.trim()) {
            showToast({ severity: 'warn', summary: 'Validation Error', detail: 'Please enter a prompt before submitting.', life: 3000 });
            return;
        }

        if (!selectedModel) {
            showToast({ severity: 'warn', summary: 'Validation Error', detail: 'Please select a model before submitting.', life: 3000 });
            return;
        }

        if (numSongs <= 0) {
            showToast({ severity: 'warn', summary: 'Validation Error', detail: 'Please select a number of songs greater than 0.', life: 3000 });
            return;
        }

        if (selectGenres && (selectedGenres.length < 1 || selectedGenres.length > 5)) {
            showToast({ severity: 'warn', summary: 'Validation Error', detail: 'Please select at least 1 a maximum of 5 music genres.', life: 3000 });
            return;
        }


        setLoading(true);

        const requestData = {
            prompt: prompt,
            config: {
                model: selectedModel.name,
                num_songs: numSongs,
                genres: selectedGenres,
                popularity: popularity,
                generate_genres: selectGenres ? 'true' : 'false'

            },
            context: {}
        };

        PlaylistService.generatePlaylist(requestData)
            .then(response => {
                console.log('Generated playlist:', response.data);
                dispatch(addPlaylist(response.data));
                setLoading(false);
                navigate('/generated-playlist');
            })
            .catch(error => {
                setLoading(false);
                showToast({ severity: 'error', summary: 'Error', detail: 'Error generating playlist. Please try again later.', life: 3000 });
                console.error('Error generating playlist:', error);

            });
    };

    const selectRandomColor = () => {
        const colors = [
            "#357ABD", "#3367D6", "#2A56C6", "#1A45B8", "#EA4335", "#D93025",
            "#C5221F", "#B31B1A", "#A61A18", "#FBBC05", "#F8A602", "#F29900",
            "#E48D00", "#D78200", "#34A853", "#2D8C47", "#26813F", "#1E7335",
            "#17662C", "#4AAFCD", "#5AB75C", "#FAA632", "#DA4F4A", "#8B4513",
            "#FF8C00", "#8A2BE2", "#00CED1", "#FF1493", "#00FA9A", "#FFD700",
            "#4B0082", "#FF4500", "#2E8B57"
        ];
        const randomIndex = Math.floor(Math.random() * colors.length);
        return colors[randomIndex];
    }

    const generateGenreColors = (genreList) => {
        const colors = {};
        genreList.forEach(genre => {
            colors[genre] = selectRandomColor();
        });
        return colors;
    };

    const toggleGenreSelection = (genre) => {
        if (selectedGenres.includes(genre)) {
            setSelectedGenres(selectedGenres.filter(g => g !== genre));
        } else if (selectedGenres.length < 5) {
            setSelectedGenres([...selectedGenres, genre]);
        }
    };

    if (loading) {
        return <LoadingSpinner />;
    }

    return (
        <>
            <div className="generator-container">
                <div className="form-container">
                    <PlaylistForm
                        prompt={prompt}
                        setPrompt={setPrompt}
                        selectedModel={selectedModel}
                        setSelectedModel={setSelectedModel}
                        models={localModels}
                        numSongs={numSongs}
                        setNumSongs={setNumSongs}
                        popularity={popularity}
                        setPopularity={setPopularity}
                        selectGenres={selectGenres}
                        setSelectGenres={setSelectGenres}
                        genres={genres}
                        genreColors={genreColors}
                        selectedGenres={selectedGenres}
                        toggleGenreSelection={toggleGenreSelection}
                        handleSubmit={handleSubmit}
                    />
                </div>
            </div>
            <div className="p-grid p-justify-center p-align-center " style={{ padding: '0.5rem', width: '90%' }}>
                <div className="p-col-12 p-md-8">
                    <Card title="Information about the Recommender Models">

                        <div>
                            {loading ?
                                (<LoadingSpinner />) :
                                (<div>
                                    {localModels ? (
                                        <ModelList models={localModels} />
                                    ) : (
                                        <p>No models available. Please try again later.</p>
                                    )}
                                </div>)
                            }
                        </div>
                    </Card>
                </div>
            </div>
        </>


    );
}

export default Generator;
