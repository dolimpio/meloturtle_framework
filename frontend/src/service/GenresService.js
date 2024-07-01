import { meloturtle_api } from '../provider/AuthProvider';

const BASE_URL = '/genres';

const GenresService = {
    getGenres: async () => {
        try {
            const response = await meloturtle_api.get(`${BASE_URL}/`);
            return response;
        } catch (error) {
            console.error("Error fetching genres", error);
            throw error;
        }
    },
};

export default GenresService;