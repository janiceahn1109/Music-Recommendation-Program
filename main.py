"""main.py

This module contains the MusicRecommenderApp class for a GUI-based song recommender system.
Users can input a song and artist to generate recommendations and visualize a similarity graph.
"""
import tkinter as tk
from tkinter import ttk
import threading
import python_ta
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from recommender import MusicRecommender


class MusicRecommenderApp(tk.Tk):
    """Graphical User Interface for the Music Recommender System.

    This application allows users to input a song and artist, receive song recommendations,
    and view a similarity graph using a graphical interface.

    Instance Attributes:
    - song_name: The name of the song entered by the user.
    - artist_name: The name of the artist entered by the user.
    - recommender: An instance of the MusicRecommender class that handles song recommendation logic.
    - graph_fig: A matplotlib Figure displaying the song similarity graph.
    - song_entry: The input widget where users enter the song name.
    - artist_entry: The input widget where users enter the artist name.
    - progress_bar: A progress bar widget displayed while recommendations are being generated.
    """

    song_name: str | None
    artist_name: str | None
    recommender: MusicRecommender
    graph_fig: any
    song_entry: tk.Entry
    artist_entry: tk.Entry
    progress_bar: ttk.Progressbar

    def __init__(self) -> None:
        """Initialize the main application window."""
        super().__init__()
        self.title("Music Recommender")
        self.geometry("1600x1000")
        self.configure(bg="black")

        self.song_name = None
        self.artist_name = None
        self.recommender = MusicRecommender("dataset.csv")
        self.graph_fig = None

        self.show_front_page()

    def clear_screen(self) -> None:
        """Clear all widgets from the screen."""
        for widget in self.winfo_children():
            widget.destroy()

    def show_front_page(self) -> None:
        """Display the front page of the application."""

        self.clear_screen()
        frame = tk.Frame(self, width=99999, height=10, background='#62c21f', pady=10)
        frame.pack(pady=(10, 10))

        title = tk.Label(self, text="Spotify Music Recommender", font=("Arial", 80, 'bold'), fg="#62c21f", bg='black',
                         anchor=tk.CENTER)
        title.pack(pady=(250, 0))

        start_button = tk.Button(self, text="Click to Start!", command=self.show_song_input_page,
                                 font=("Arial", 40, 'bold'))
        start_button.pack(pady=(100, 0))

        frame = tk.Frame(self, width=99999, height=10, background='#62c21f', pady=10)
        frame.pack(padx=10, pady=190)

    def show_song_input_page(self) -> None:
        """Display input prompt for the song name."""
        self.clear_screen()

        frame = tk.Frame(self, width=99999, height=10, background='#62c21f', pady=10)
        frame.pack(padx=10, pady=10)

        label = tk.Label(self, text="Input Your Song", font=("Arial", 40), fg="white", bg="black", borderwidth=10)
        label.pack(pady=(300, 0))

        self.song_entry = tk.Entry(self, font=("Arial", 30), bg="gray20", fg="white", relief="solid",
                                   bd=2, insertbackground="white")
        self.song_entry.pack(pady=10)
        self.song_entry.focus_set()

        submit_button = tk.Button(self, text="Next", command=self.show_artist_input_page, font=("Arial", 20),
                                  bg="gray", fg="#1DB954")
        submit_button.pack(pady=20)

    def show_artist_input_page(self) -> None:
        """Display input prompt for the artist name."""

        self.song_name = self.song_entry.get()
        self.clear_screen()

        frame = tk.Frame(self, width=99999, height=10, background='#62c21f', pady=10)
        frame.pack(padx=10, pady=10)

        label = tk.Label(self, text="Input Your Artist", font=("Arial", 40), fg="white", bg="black", borderwidth=10)
        label.pack(pady=(300, 0))

        self.artist_entry = tk.Entry(self, font=("Arial", 30), bg="gray20", fg="white", relief="solid",
                                     bd=2, insertbackground="white")
        self.artist_entry.pack(pady=10)
        self.artist_entry.focus_set()

        submit_button = tk.Button(self, text="Generate", command=self.show_loading_page, font=("Arial", 20),
                                  bg="gray", fg="#1DB954")
        submit_button.pack(pady=20)

    def show_loading_page(self) -> None:
        """Display a loading page while recommendations are being generated."""
        self.artist_name = self.artist_entry.get()
        self.clear_screen()
        self.progress_bar = ttk.Progressbar(self, orient="horizontal", length=500, mode="indeterminate")
        self.progress_bar.pack(pady=(350, 0))
        self.progress_bar.start()
        tk.Label(self, text="Generating...", font=("Arial", 40), fg="#1DB954", bg="black").pack(pady=30)
        threading.Thread(target=self.generate_recommendations).start()

    def generate_recommendations(self) -> None:
        """Generate music recommendations in a separate thread."""
        recs = self.recommender.get_recommendations(self.song_name, self.artist_name)
        graph = self.recommender.music_graph
        self.after(0, lambda: self.set_and_show_graph(graph, self.song_name, recs))

    def set_and_show_graph(self, graph: any, focus_song: str, recommendations: list[str] | str) -> None:
        """Set the graph figure and display the results page."""
        if graph:
            self.graph_fig = graph.get_figure(focus_song=focus_song, limit=10)
        else:
            self.graph_fig = None
        self.show_recommendations_page(recommendations)

    def show_recommendations_page(self, recommendations: list[str] | str) -> None:
        """Display the list of recommended songs and the similarity graph."""
        self.clear_screen()
        if recommendations == "Invalid Song Input":
            tk.Label(self, text="Invalid Song Input. Please try again.",
                     font=("Arial", 40), fg="red", bg="black").pack(pady=300)
            tk.Button(self, text="Try Again", command=self.show_song_input_page,
                      font=("Arial", 30)).pack(pady=40)
            return

        left = tk.Frame(self, bg="black", width=800)
        left.pack(side="left", fill="both", expand=True)
        tk.Label(left, text="TOP 5 SONGS", font=("Arial", 60), fg="#62c21f", bg="black").pack(pady=60)
        for i, song in enumerate(recommendations, 1):
            tk.Label(left, text=f"{i}. {song}", font=("Arial", 30), fg="white", bg="black").pack(pady=10)

        right = tk.Frame(self, bg="black", width=800)
        right.pack(side="right", fill="both", expand=True)
        tk.Label(right, text="SONG SIMILARITY GRAPH", font=("Arial", 40), fg="#62c21f", bg="black").pack(pady=30)
        if self.graph_fig:
            canvas = FigureCanvasTkAgg(self.graph_fig, master=right)
            canvas.draw()
            canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
        # Referenced ChatGPT for the show_recommendations_page() for help displaying the graph in the program


if __name__ == "__main__":
    app = MusicRecommenderApp()
    app.mainloop()

    python_ta.check_all(config={
        'extra-imports': ['tkinter', 'tkinter.ttk', 'threading', 'time',
                          'matplotlib.backends.backend_tkagg', 'main', 'recommender'],
        'allowed-io': ['__main__'],
        'max-line-length': 120
    })
