# Music Recommendation Program

A GUI-based music recommendation system that suggests songs based on audio-feature similarity and visualizes their relationships using a graph.

The project was developed as part of a 4-person team project using Python.

## Features

- Accepts a song title and artist through a Tkinter graphical interface
- Identifies the genre of the selected song
- Builds a graph containing songs from the same genre
- Calculates similarity between songs using normalized audio features
- Returns the top 5 most similar songs
- Displays an interactive-style similarity graph showing relationships between the selected song and its closest neighbours
- Handles invalid song inputs and allows users to retry
- Generates recommendations in a separate thread to prevent the GUI from freezing

## Recommendation Method

The program compares songs using the following audio features:

- Danceability
- Energy
- Speechiness
- Acousticness
- Instrumentalness
- Liveness
- Valence
- Tempo

These features are normalized using min-max normalization.

Each song is represented as a vertex in a graph. Similarity between two songs is calculated using the dot product of their normalized feature vectors.

An edge is created between two songs when their similarity score is greater than `0.7`.

For a selected song, the program ranks its neighbouring songs by similarity score and returns the top 5 recommendations.

## Graph Visualization

The recommendation graph is built using a custom `MusicGraph` class and converted into a NetworkX graph for visualization.

The selected song is displayed alongside its most similar neighbouring songs using Matplotlib.

## Technologies

- Python
- Tkinter
- Pandas
- NumPy
- NetworkX
- Matplotlib
- Threading

## Project Structure

### `main.py`
Contains the graphical user interface and manages user input, loading screens, recommendation display, and graph visualization.

### `recommender.py`
Loads and processes the music dataset, normalizes audio features, identifies song genres, builds genre-specific graphs, and generates recommendations.

### `music_graph.py`
Implements the graph data structure used to represent songs and their similarities, including vertices, weighted edges, recommendation ranking, and NetworkX visualization.

## Running the Program

Ensure the required libraries are installed and that `dataset.csv` is located in the project directory.

Run:

```bash
python main.py
