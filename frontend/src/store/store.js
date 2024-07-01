import { configureStore } from '@reduxjs/toolkit';
import playlistReducer from './features/playlist/playlistSlice';

export default configureStore({
    reducer: {
        playlist: playlistReducer,
    }
})