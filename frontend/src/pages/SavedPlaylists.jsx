import React, { useState, useEffect, useRef, useCallback } from 'react';

import { Card } from 'primereact/card';
import { Message } from 'primereact/message';
import { InputText } from 'primereact/inputtext';
import { Button } from 'primereact/button';
import { useAuth } from "../provider/AuthProvider";
import { useToast } from '../provider/ToastProvider';

import Playlist from '../components/Playlist';
import LoadingSpinner from '../components/LoadingSpinner';

import PlaylistService from '../service/PlaylistService.js';
import '../styles/SavedPlaylists.css';


const SavedPlaylists = () => {
    const [playlists, setPlaylists] = useState([]);
    const [loading, setLoading] = useState(false);
    const [page, setPage] = useState(1);
    const [hasMore, setHasMore] = useState(true);

    const [searchTerm, setSearchTerm] = useState('');
    const { token, isTokenSet } = useAuth();

    const { showToast } = useToast();

    const fetchPlaylists = async (reset = false) => {
        if (loading || (!hasMore && !reset)) return;
        setLoading(true);
        try {
            const fetched_playlists = await PlaylistService.getSavedPlaylist(page);
            const newPlaylists = fetched_playlists.data.playlists;
            console.log("These are the user's playlists: " + newPlaylists);
            setPlaylists((prevPlaylists) => reset ? newPlaylists : [...prevPlaylists, ...newPlaylists]);
            setHasMore(newPlaylists.length > 0)
        } catch (error) {
            console.error('Error fetching playlists:', error);
            showToast({ severity: 'error', summary: 'Error', detail: 'Failed to fetch playlists. Please try again later.', life: 3000 });
        } finally {
            setLoading(false);
        }
    };

    const fetchSearchedPlaylists = async () => {

        setLoading(true);
        try {
            const fetched_playlists = await PlaylistService.getSearchPlaylist(searchTerm);
            const newPlaylists = fetched_playlists.data.playlists;
            console.log("These are the user's playlists: " + newPlaylists);
            setPlaylists(newPlaylists);
            setHasMore(false);
        } catch (error) {
            console.error('Error fetching playlists:', error);
            showToast({ severity: 'error', summary: 'Error', detail: 'Failed to fetch playlists. Please try again later.', life: 3000 });
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        if (isTokenSet) {
            if (searchTerm) {
                fetchSearchedPlaylists()
            } else {
                fetchPlaylists(page === 1);
            }
        }


    }, [token, page, searchTerm, isTokenSet]);

    useEffect(() => {
        if (!searchTerm) {
            setHasMore(true);
            setPage(1);
            setPlaylists([]);
            // fetchPlaylists(true);
        }

    }, [searchTerm]);

    const handleScroll = () => {
        const { scrollTop, clientHeight, scrollHeight } =
            document.documentElement;
        if (scrollTop + clientHeight >= scrollHeight && !loading && hasMore && !searchTerm) {
            setPage((prevPage) => prevPage + 1);
        }
    }

    useEffect(() => {
        window.addEventListener('scroll', handleScroll);
        return () => window.removeEventListener('scroll', handleScroll);
    }, []);


    const handleSearch = (event) => {
        if (event) event.preventDefault();
        if (searchTerm.trim() === '') {
            handleClearSearch();
        } else {
            setPage(1);
            setHasMore(false);

        }
    };

    const handleClearSearch = () => {
        setSearchTerm('');
        setPage(1);
        setPlaylists([]);
        setHasMore(true);
        fetchPlaylists(true);
    };

    const deletePlaylist = async (spotifyId) => {
        try {
            const response = await PlaylistService.deletePlaylist(spotifyId);
            setPlaylists(playlists.filter(playlist => playlist.context.spotify_id !== spotifyId));
            showToast({ severity: 'success', summary: 'Success', detail: 'Playlist deleted successfully.', life: 3000 });
        } catch (error) {
            console.error('Error deleting playlist:', error);
            showToast({ severity: 'error', summary: 'Error', detail: 'Failed to delete playlist. Please try again later.', life: 3000 });
        }
    };

    const renderContent = () => {
        if (playlists.length > 0) {
            return (
                <div className='playlists-container'>
                    <div className='playlist-row'>
                        {playlists &&
                            playlists.map((playlist) => <Playlist key={playlist.context.spotify_id} playlist={playlist} onDelete={deletePlaylist} showDelete={true} />)}
                    </div>
                    {loading && <LoadingSpinner/>}
                    {!hasMore && <p className="no-more-data">No more playlist...... Make some more!</p>}
                </div>
            );
        }
        return (
            <div className="no-playlists-container">
                <Card className="info-card">
                    <Message severity="info" text="There are no playlists available." />
                </Card>
            </div>
        );
    };

    return (
        <div className="saved-playlists">
            {playlists.length > 0 && <h3> Total number of playlists: {playlists.length} </h3>}
            <div className="search-bar">
                <InputText
                    placeholder="Search Playlists"
                    value={searchTerm}
                    onChange={(e) => setSearchTerm(e.target.value)}
                    onKeyDown={(e) => {
                        if (e.key === 'Enter') {
                            handleSearch(e);
                        }
                    }
                    }
                    style={{ flex: "1" }}
                />
                <Button icon="pi pi-times" onClick={handleClearSearch} className="p-button-secondary" />
                <Button icon="pi pi-search" onClick={handleSearch} />
            </div>
            {renderContent()}
        </div>
    );
};

export default SavedPlaylists;
