"""recommender.py

This module defines the MusicRecommender class, which provides functionality for building a graph of songs
based on audio features and generating music recommendations using song similarity within a genre.
"""

import pandas as pd
from music_graph import MusicGraph


class MusicRecommender:
    """A recommender system that builds a music graph and provides recommendations based on similarity.

    This class reads a dataset of songs, normalizes the features, and provides methods
    to build a graph and recommend similar songs based on a given input.
    Instance Attributes:
    - df: The original pandas DataFrame containing all songs and features from the dataset.
    - normalized_df: A normalized copy of df with selected columns used for similarity comparison.
    - music_graph: A MusicGraph object representing the similarity graph of songs in a genre,
      or None if the graph has not been built yet.
    """

    df: pd.DataFrame
    normalized_df: pd.DataFrame
    music_graph: MusicGraph | None

    def __init__(self, dataset_path: str) -> None:
        """Initialize the recommender system with the dataset located at dataset_path."""
        self.df = pd.read_csv(dataset_path)
        self.music_graph = None

        column_names = ["artists", "track_name", "danceability", "energy", "speechiness",
                        "acousticness", "instrumentalness", "liveness", "valence", "tempo", "track_genre"]

        self.normalized_df = self.df[column_names].copy()
        numerical_cols = ["danceability", "energy", "speechiness",
                          "acousticness", "instrumentalness", "liveness", "valence", "tempo"]

        self.normalized_df[numerical_cols] = (
            self.normalized_df[numerical_cols] - self.normalized_df[numerical_cols].min()
        ) / (
            self.normalized_df[numerical_cols].max() - self.normalized_df[numerical_cols].min()
        )

        self.normalized_df.dropna(inplace=True)

    def find_song_genre(self, song_name: str, artist_name: str) -> str | None:
        """Return the genre of the specified song and artist, or None if not found.

        This function is designed to be called programmatically, not as a doctest.
        """
        for _, row in self.df.iterrows():
            if row["track_name"] == song_name and row["artists"] == artist_name:
                return row["track_genre"]
        return None

    def create_genre_graph(self, genre_name: str) -> MusicGraph:
        """Return a MusicGraph with songs from the specified genre.

        This function is designed to be called programmatically.
        """
        genre_songs = self.normalized_df[self.normalized_df["track_genre"] == genre_name]
        graph = MusicGraph()

        for _, row in genre_songs.iterrows():
            features = row[["danceability", "energy", "speechiness",
                            "acousticness", "instrumentalness", "liveness", "valence", "tempo"]].values
            graph.add_vertex(row["track_name"], features)

        song_list = genre_songs["track_name"].tolist()
        for i in range(len(song_list)):
            for j in range(i + 1, len(song_list)):
                sim = graph.get_similarity_score(song_list[i], song_list[j])
                if sim > 0.7:
                    graph.add_edge(song_list[i], song_list[j], sim)

        return graph

    def get_recommendations(self, song_name: str, artist_name: str, limit: int = 5) -> list[str] | str:
        """Return a list of recommended songs, or a message if input is invalid.

        This function is designed to be called programmatically.
        """
        genre_name = self.find_song_genre(song_name, artist_name)
        if genre_name is None:
            return "Invalid Song Input"

        self.music_graph = self.create_genre_graph(genre_name)
        return self.music_graph.recommend_songs(song_name, limit)


if __name__ == "__main__":
    # Prompt user and run the recommender
    input_song = input("Enter song: ")
    input_artist = input("Enter artist: ")
    recommender = MusicRecommender("dataset.csv")
    found_genre = recommender.find_song_genre(input_song, input_artist)
    if found_genre is None:
        print("Invalid Song Input")
    else:
        print(f"Genre: {found_genre}")
        top_recs = recommender.get_recommendations(input_song, input_artist)
        print("Top Recommendations:")
        for result in top_recs:
            print(f"- {result}")

    import python_ta
    python_ta.check_all(config={
        'extra-imports': ['pandas', 'music_graph'],
        'allowed-io': ['__main__'],
        'max-line-length': 120
    })
