# 🎶 Meloturtle
## Playlist Recommendation Framework for Spotify

Welcome to the repository for the Bachelor's Final Project: "Meloturtle: Playlist Recommendation Framework for Spotify". This project aims to develop a prototype framework that aggregates multiple recommendation systems for playlist generation using Spotify's API, allowing users to customize their recommendations through natural language descriptions.

## 📋 Table of Contents

- [Introduction](#introduction)
- [Features](#features)
- [Architecture](#architecture)
- [Prerequisites](#prerequisites)
- [Usage](#usage)
- [Contributing](#contributing)
- [License](#license)
- [Contact](#contact)

## 🌟 Introduction

In this project, we aim to create a prototype framework that combines various recommendation systems to generate playlists on Spotify. The primary objective is to enable users to tailor their recommendations by describing their desired moods and emotions in text, improving the recommendation quality.

## ✨ Features

- 🎵 **Text based Recommendations:** Users can describe their desired moods and emotions to generate tailored playlists.
- 🧩 **Multiple Recommendation Systems:** Integration of various recommendation models. Also pwith the possibility of adding more.
- 👤 **User Management:** Handling and storage of user data and generated playlists.
- 🔄 **Spotify API Integration:** Integration with Spotify's API for data exchange and playlist management.
- 🖥️ **User-Friendly Interface:** An intuitive UI for easy user interaction and customization.

## 🏛️ Architecture

The framework's architecture is designed to be modular and extensible, ensuring easy integration of current and future recommendation systems. Below is a high-level overview of the architecture:

![Architecture Diagram](link-architecture-diagram)

## ⚙️ Prerequisites

1. **Have docker installed locally:** Follow the instructions from the official documentation: https://docs.docker.com/get-docker/

2. **Set up Spotify Developer Account:** Follow the instructions from Spotify: https://developer.spotify.com/documentation/web-api. 
You will need to get the values for:
   - SPOTIFY_CLIENT_ID
   - SPOTIFY_CLIENT_SECRET
   - REDIRECT_URI

The REDIRECT_URI should be: 
```
http://localhost:8000/api/auth/callback
```
⚠️ Follow only if you want to use the ChatGPT recommendation model:
2. **Set up OpenAI API Account:** Follow the instructions from the link: https://help.openai.com/en/articles/4936850-where-do-i-find-my-openai-api-key. 
You will need to get the values for:
   - CHATGTP_SECRET

⚠️ Follow only if you want to use the Moodika recommendation model:
You will need to get the values for:
   - CHATGTP_SECRET
   - CLIENT_ID = 
   - CLIENT_SECRET = 
   - REDIRECT_URI =
   - SPOTIPY_CLIENT_ID =
   - SPOTIPY_CLIENT_SECRET =

You can fin these inside:
```bash
meloturtle_framework/backend/backend/services/recommendations_manager/recommendation_models/moodika/model_a/config.py
``` 

## 🚀 Usage

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/dolimpio/meloturtle_framework.git
   ```
2. **Go to the backend project directory:**
   ```bash
   cd meloturtle_framework/backend
   ```
3. **Set Up Environment Variables:** Inside the backend directory, you should find a `.env` file. Add the data from Spotify's Web API and OpenAI API to these variables. Make sure to add the BACKEND_ prefix before each variable. e.g:
   ```env
   BACKEND_SPOTIFY_CLIENT_ID=your_client_id
   BACKEND_SPOTIFY_CLIENT_SECRET=your_client_secret
   BACKEND_SCOPE=your_neccessary_scopes
   BACKEND_REDIRECT_URI=your_selected_redirect_uri
   BACKEND_CHATGTP_SECRET=your_chatgpt_secret
   ```
4. **Go to the deploy project directory:**
   ```bash
   cd ..
   cd deploy
   ```
5. **Run the Docker Compose:**
   ```bash
   docker compose up --build
   ```
6. **Access the User Interface:**
   - Open your web browser and go to `http://localhost:3000`.

7. **Sign in with Spotify:**
   - Users need to authenticate with their Spotify account to use the recommendation features. Use the ‘Singin’ button on the navbar and then the ‘Login with Spotify’ button to Login.

8. **Describe your Playlist:**
   - After logging, click on the ‘Generator’ option in the navbar. Once in the generation page, input your desired moods and emotions in the text box to generate a playlist with the parameters you want.

9. **Manage Playlists:**
   - You can save your playlist with the ‘Save’ button at the preview of a playlist after a generation request was sent. View, edit, and manage your generated playlists within the user interface at the ‘Library’ section in the navbar.

## 🤝 Contributing or using the project
Please feel free to use any code from this repository.

## License
This project has an MIT license, check it under LICENSE.

## 📬 Contact

For any questions or feedback, please contact:
- **dolimpio**
- **GitHub:** [dolimpio](https://github.com/dolimpio)
- **LinkedIn:** [David](https://www.linkedin.com/in/david-olimpio-silva/)

If you are interested in the Ninja Turtle images, please visit: https://www.artstation.com/mattwessel