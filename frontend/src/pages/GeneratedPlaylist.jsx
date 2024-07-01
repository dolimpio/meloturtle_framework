import React, { useEffect, useState, useRef } from 'react';
import { useSelector, useDispatch } from 'react-redux';

import { useNavigate } from 'react-router-dom';
import { Button } from 'primereact/button';
import { Card } from 'primereact/card';

import { clearPlaylist } from '../store/features/playlist/playlistSlice';
import Playlist from '../components/Playlist';
import PlaylistService from '../service/PlaylistService';
import '../styles/GeneratedPlaylist.css';
import { useToast } from '../provider/ToastProvider';


const GeneratedPlaylist = () => {
  const playlist = useSelector((state) => state.playlist.generated_playlist);
  const [loading, setLoading] = useState(false);
  const { showToast } = useToast();

  const navigate = useNavigate();
  const dispatch = useDispatch();


  const handleSave = async () => {
    setLoading(true);
    try {
      const playlist_to_save = { ...playlist };
      playlist_to_save.context = { "spotify_id": playlist.context.spotify_id, "created_at": playlist.context.created_at }
      const response = await PlaylistService.savePlaylist(playlist_to_save);
      console.log('Playlist saved:', response.data);
      if (response.status == 200) {
        showToast({ severity: 'success', summary: 'Success', detail: 'Playlist saved successfully!' });

      }
      dispatch(clearPlaylist());
      setLoading(false);
      navigate('/library');
    } catch (error) {
      showToast({ severity: 'error', summary: 'Error', detail: 'Error saving playlist. Please try again later.' });
      console.error('Error saving playlist:', error);
      setLoading(false);
      navigate('/generator');

    } 

  };

  const handleRegenerate = () => {
    navigate('/generator');
  };

  if (!playlist) {
    return (
      <div className="p-m-4">
        <h3>No Playlist Generated</h3>
        <p>Please go back and generate a playlist.</p>
        <Button label="Back to Generator" icon="pi pi-arrow-left" onClick={() => navigate('/generator')} loading={loading} disabled={loading} />
      </div>
    );
  }

  return (
    <div>
      <h2>Generated Playlist</h2>

      <Card style={{ colo: 'white'}}>
        <Playlist index={0} playlist={playlist} showDelete={false} />
        <div className="button-container">
          <Button label="Save Playlist" icon="pi pi-save" onClick={handleSave} className="p-mr-2" loading={loading} />
          <Button label="Regenerate Playlist" icon="pi pi-refresh" onClick={handleRegenerate} />
        </div>
      </Card>
    </div>

  );
};

export default GeneratedPlaylist;