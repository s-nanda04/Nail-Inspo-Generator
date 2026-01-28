import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import requests
from io import BytesIO
import random
from config import UNSPLASH_API_KEY

# creates a blueprint for the app
class NailInspirationApp:
  def __init__(self, root):

    #stores the window to use it later
    self.root = root

    #sets the title of the window
    self.root.title("Seasonal Nail Inspiration")

    #sets the size of the window
    self.root.geometry("800x900")

    #sets the background colr to be gray
    self.root.configure(bg='#f5f5f5')

    #search terms for each season that will be entered to the database to search for an inspiration picture
    self.season_terms = {
      'summer': ['summer', 'tropical', 'beach'],
      'fall': ['autumn', 'fall', 'burgundy', 'warm color'],
      'winter': ['winter', 'holiday', 'snowflake', 'festive'],
      'spring': ['spring', 'floral', 'pastel', 'garden']
    }

    self.UNSPLASH_API_KEY = UNSPLASH_API_KEY

    self.setup_ui()

  def setup_ui(self):
    title = tk.Label(
        self.root,
        text="Seasonal Nail Inspiration",
        font=('Arial', 24, 'bold'),
        bg='#f5f5f5',
        fg='#333'
    )
    title.pack(pady=20)

    # Instructions for the user
    instructions = tk.Label(
        self.root,
        text="Choose a season to get a nail inspiration picture!",
        font=('Arial', 12),
        bg='#f5f5f5',
        fg='#666'
    )
    instructions.pack(pady=10)

    # Holds all season buttons in a row
    button_frame = tk.Frame(self.root, bg='#f5f5f5')
    button_frame.pack(pady=20)

    self.image_frame = tk.Frame(self.root, bg='white', relief='solid', borderwidth=2)
    self.image_frame.pack(pady=20, padx=40, fill='both', expand=True)

    # The color and emoji for each button of each season
    seasons = {
      'Summer': {'color': '#FF6B6B', 'emoji': '☀️'},
      'Fall': {'color':'#FF8C00', 'emoji': '🍂'},
      'Winter': {'color': '#4682B4', 'emoji': '❄️'},
      'Spring': {'color': '#98D8C8', 'emoji': '🌸'}
    }

    # Loop through the seasons and make a button for each one of them
    for season, info in seasons.items():
      btn = tk.Button(
          button_frame,
          text=info['emoji'] + " " + season,
          font=('Arial', 14, 'bold'),
          bg=info['color'],
          fg='white',
          width=12,
          height=2,
          relief='raised',
          cursor='hand2',
          command=lambda s=season.lower(): self.get_nail_inspo(s)
      )
      btn.pack(side='left', padx=10)

    self.image_label = tk.Label(
        self.image_frame,
        text="Click a button to see an inspiration from that season",
        font=('Arial', 14),
        bg='white',
        fg='#999'
    )
    self.image_label.pack(expand=True)

    self.credit_label = tk.Label(
        self.root,
        text="",
        font=('Arial', 9),
        bg='#f5f5f5',
        fg='#666'
    )
    self.credit_label.pack(pady=10)

  def get_nail_inspo(self, season):
    self.image_label.config(text=f"Loading {season} inspiration...")
    self.root.update()
    try:
      #pick a random search term
      search_term = random.choice(self.season_terms[season]) + " nail art manicure"

      url = "https://api.unsplash.com/photos/random"
      params = {
        'query': search_term,
        'client_id': self.UNSPLASH_API_KEY,
        'orientation': 'portrait'
      }

      #send a request to Unsplash
      response = requests.get(url, params=params)
      response.raise_for_status()

      #get the photo data from the API
      data = response.json()
      image_url = data['urls']['regular']
      photographer = data['user']['name']

      #download the image
      img_response = requests.get(image_url)
      img_response.raise_for_status()

      img = Image.open(BytesIO(img_response.content))

      img.thumbnail((700, 600), Image.Resampling.LANCZOS)

      photo = ImageTk.PhotoImage(img)

      self.image_label.config(image=photo, text="")
      self.image_label.image = photo

      self.credit_label.config(text=f"Photo by {photographer} on Unsplash")

    except requests.exceptions.RequestException as e:
      messagebox.showerror("Error", f"failed to fetch image: {str(e)}")
      self.image_label.config(text="Failed to load the image.")
    except Exception as e:
      messagebox.showerror("Error", f"Error occured: {str(e)}")
      self.image_label.config(text="An error occurred")

def main():
  root = tk.Tk()
  app = NailInspirationApp(root)
  root.mainloop()

if __name__ == "__main__":
  main()
