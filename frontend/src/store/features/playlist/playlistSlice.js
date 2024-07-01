import { createSlice } from '@reduxjs/toolkit';

const initialState = {
  generated_playlist: null,
};

const playlistSlice = createSlice({
  name: 'playlist',
  initialState,
  reducers: {
    setPlaylist: (state, action) => {
      state.generated_playlist = action.payload;
    },
    clearPlaylist: (state) => {
      state.generated_playlist = null;
    },
  }
});

export const { setPlaylist, clearPlaylist } = playlistSlice.actions;
export default playlistSlice.reducer;
