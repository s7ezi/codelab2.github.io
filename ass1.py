import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk 
import requests
import io

class MainPageofAPI:
    def __init__(self, root, start_callback):
        self.root = root
        self.root.title("API Movie Search App - Main Page")

        # Set the window size
        self.root.geometry("800x600")

        image_path = "mov.jpg"
        original_image = Image.open(image_path)

        aspect_ratio = original_image.width / original_image.height

        new_width = int(self.root.winfo_screenwidth())
        new_height = int(new_width / aspect_ratio)

        self.background_image = ImageTk.PhotoImage(original_image.resize((new_width, new_height)))

        self.canvas = tk.Canvas(self.root, width=new_width, height=new_height)
        self.canvas.pack()

        self.canvas.create_image(0, 0, anchor=tk.NW, image=self.background_image)

        welcome_label = tk.Label(self.root, text="Welcome to Cinema Hub X", font=("Poplar Std", 16), bg="white")
        welcome_label.place(relx=0.5, rely=0.1, anchor=tk.CENTER)

        start_button = ttk.Button(self.root, text="Start", command=start_callback)
        start_button.place(relx=0.5, rely=0.5, anchor=tk.CENTER)


class ApiSearchApp:
    def __init__(self, root):
        self.root = root
        self.root.title("API Search App")

        # Set the window size
        self.root.geometry("690x450")

        # Create frame for search entry and search button
        self.search_frame = ttk.Frame(self.root, style='Dark.TFrame')
        self.search_frame.grid(row=0, column=0, padx=10, pady=10)

        # Create frame for displaying API results
        self.result_frame = ttk.Frame(self.root, style='Dark.TFrame')
        self.result_frame.grid(row=1, column=0, padx=10, pady=10)

        # Apply style configuration for the entire app
        self.root.tk_setPalette(background='#000', foreground='#fff', activeBackground='#444', activeForeground='#fff')

        # Apply style configuration for text widgets
        self.root.option_add('*TButton*highlightBackground', '#000')
        self.root.option_add('*TButton*highlightColor', '#000')

        self.create_widgets()

    def create_widgets(self):
        # Configure style for the entire app
        self.style = ttk.Style()
        self.style.configure('Dark.TFrame', background='#000')
        self.style.configure('TButton', background='#444', foreground='#000', borderwidth=0)
        self.style.map('TButton', background=[('active', '#666')])

        # Entry widget for user input in the search frame
        self.search_entry = ttk.Entry(self.search_frame, width=30, style='TEntry')
        self.search_entry.grid(row=0, column=0, padx=10, pady=10)

        # Button to trigger API search in the search frame
        search_button = ttk.Button(self.search_frame, text="Search", command=self.fetch_data, style='TButton')
        search_button.grid(row=0, column=1, padx=10, pady=10)

        # Button for trending movies
        trending_button = ttk.Button(self.search_frame, text="Trending", command=self.fetch_trending, style='TButton')
        trending_button.grid(row=0, column=4, padx=10, pady=10)

        # About button in the search frame
        about_button = ttk.Button(self.search_frame, text="About", command=self.show_about, style='TButton')
        about_button.grid(row=0, column=3, padx=10, pady=10)

        # Home button in the search frame
        home_button = ttk.Button(self.search_frame, text="Home", command=self.go_home, style='TButton')
        home_button.grid(row=0, column=2, padx=10, pady=10)

        # Text widget for displaying API results in the result frame
        self.result_text = tk.Text(self.result_frame, wrap="word", width=80, height=20, background='#000', foreground='#fff')
        self.result_text.grid(row=0, column=0, padx=10, pady=10)

    def fetch_data(self):
        # Get user input from the entry widget
        user_input = self.search_entry.get()

        api_key = "f0c6d98d026e07d9250be25cb0a3a1f8"

        api_url = f"https://api.themoviedb.org/3/search/movie?api_key={api_key}&query={user_input}"

        try:
            response = requests.get(api_url)

            if response.status_code == 200:
                api_data = response.json()

                self.result_text.delete("1.0", tk.END)

                if 'results' in api_data and api_data['results']:
                    # Display details of the first result
                    movie_details = api_data['results'][0]
                    result_text = (
                        f"Title: {movie_details['title']}\n"
                        f"Release Year: {movie_details['release_date'][:4]}\n"
                        f"Overview: {movie_details['overview']}"
                    )
                    self.result_text.insert(tk.END, result_text)
                else:
                    # Display an error message if 'results' key is not present or no results found
                    self.result_text.insert(tk.END, "Error: No results found")
            else:
                # Display an error message if the request was not successful
                self.result_text.insert(tk.END, f"Error: {response.status_code}")
        except Exception as e:
            # Display an error message if an exception occurs during the request
            self.result_text.insert(tk.END, f"Error: {str(e)}")

    def fetch_trending(self):
        # Fetch and display trending movies
        api_key = "f0c6d98d026e07d9250be25cb0a3a1f8"

        trending_url = f"https://api.themoviedb.org/3/trending/all/week?api_key={api_key}"

        try:
            # Make a request to the API for trending movies
            response = requests.get(trending_url)

            if response.status_code == 200:
                trending_data = response.json()

                self.result_text.delete("1.0", tk.END)

                if 'results' in trending_data and trending_data['results']:
                    trending_details = trending_data['results'][0]
                    trending_text = (
                        f"Trending Title: {trending_details['original_title']}\n"
                        f"Release Year: {trending_details['release_date'][:4]}\n"
                        f"Overview: {trending_details['overview']}"
                    )
                    self.result_text.insert(tk.END, trending_text)
                else:
                    self.result_text.insert(tk.END, "Error: No trending results found")
            else:
                # Display an error message if the request was not successful
                self.result_text.insert(tk.END, f"Error: {response.status_code}")
        except Exception as e:
            self.result_text.insert(tk.END, f"Error: {str(e)}")

    def show_search_button(self):
        # Show the search button in the search frame
        search_button = ttk.Button(self.search_frame, text="Search", command=self.fetch_data, style='TButton')
        search_button.grid(row=0, column=1, padx=10, pady=10)

    def hide_search_button(self):
        for widget in self.search_frame.winfo_children():
            widget.destroy()

    def go_home(self):
        self.search_entry.delete(0, tk.END)
        self.result_text.delete("1.0", tk.END)
        # Show the search button after going home
        self.show_search_button()

    def show_about(self):
        about_message = (
            "Its an API search app for Movies.\n"
            "By using this API , user's can search up the movies the user wants.\n"
            "It shows the Movie name, release date, Overview of the movie and Trending movie details as well \n"
            
        )
        self.result_text.delete("1.0", tk.END)
        self.result_text.insert(tk.END, about_message)

def start_app():
    root_main.destroy() 
    root = tk.Tk()
    app = ApiSearchApp(root)
    root.mainloop()

if __name__ == "__main__":
    root_main = tk.Tk()
    main_page = MainPageofAPI(root_main, start_app)
    root_main.mainloop()
