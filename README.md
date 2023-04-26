# Music Discovery

Find the top songs and albums from your favorite artist, as well as related artist.

## Table of Contents

- [Music Discovery](#music-discovery)
  - [Table of Contents](#table-of-contents)
  - [Features](#features)
  - [Installation](#installation)
  - [Usage](#usage)
  - [License](#license)

## Features

This is a web application that allows users to search for Spotify artists and see their top songs, albums, and related artists. It uses the Spotify Web API to fetch the artist information and render it on the web page using Jinja2 templates, Flask, and Python.

## Installation

To run this application on your local machine, follow these steps:

Clone this repository: git clone https://github.com/your-username/spotify-artist-search.git
Install the dependencies: pip install -r requirements.txt
Set the environment variables SPOTIFY_CLIENT_ID and SPOTIFY_CLIENT_SECRET with your Spotify Web API client ID and client secret.
Run the server: python app.py
Open http://localhost:5000 in your web browser to access the application.

## Usage

On the home page, type the name of your favorite artist in the search box and click "Search". The application will display the artist's top songs, albums, and related artists. You can click on the song and album names to go to their corresponding pages on Spotify. You can also click on the related artist names to search for them and see their information.

## License

This project is licensed under the MIT License - see the LICENSE file for details.
