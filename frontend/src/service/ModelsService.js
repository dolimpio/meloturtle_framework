import { meloturtle_api } from '../provider/AuthProvider';

const BASE_URL = '/models';

const ModelsService = {
    getModels: async () => {
        try {
            const response = await meloturtle_api.get(`${BASE_URL}/`);
            return response;
        } catch (error) {
            console.error("Error fetching models", error);
            throw error;
        }
    },

    getModelNames: async () => {
        try {
            const response = await meloturtle_api.get(`${BASE_URL}/names`);
            return response;
        } catch (error) {
            console.error("Error fetching model names", error);
            throw error;
        }
    },

    getModelByName: async (modelName) => {
        try {
            const response = await meloturtle_api.get(`${BASE_URL}/${modelName}`);
            return response;
        } catch (error) {
            console.error(`Error fetching model ${modelName}`, error);
            throw error;
        }
    },

};

export default ModelsService;
