import { meloturtle_api } from '../provider/AuthProvider';

const BASE_URL = '/playlists';

const PlaylistService = {
    generatePlaylist: async (data) => {
        try {
            const response = await meloturtle_api.post(`${BASE_URL}/generate`, data);
            return response;
        } catch (error) {
            console.error('Error generating playlist:', error);
            throw error;
        }
    },
    savePlaylist: async (playlist) => {
        try {
            const response = await meloturtle_api.post(`${BASE_URL}/save`, playlist);
            return response;
        } catch (error) {
            console.error('Error saving playlist:', error);
            throw error;
        }
    },
    getSavedPlaylist: async (page) => {
        try {
            const response = await meloturtle_api.get(`${BASE_URL}/`, {
                params: { page }
            });
            return response;
        } catch (error) {
            console.error('Error fetching saved playlists:', error);
            throw error;
        }
    },
    getSearchPlaylist: async (searchTerm) => {
        try {
            const response = await meloturtle_api.get(`${BASE_URL}/search`, {
                params: { searchTerm }
            });
            return response;
        } catch (error) {
            console.error('Error searching playlists:', error);
            throw error;
        }
    },
    deletePlaylist: async (spotifyId) => {
        try {
            const response = await meloturtle_api.delete(`${BASE_URL}/${spotifyId}`);
            return response;
        } catch (error) {
            console.error('Error deleting playlist:', error);
            throw error;
        }
    }
};

export default PlaylistService;
