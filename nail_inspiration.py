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
      'summer': ['summer nails', 'tropical nail art', 'beach nails'],
      'fall': ['autumn nails', 'fall nail art', 'burgundy nails', 'cozy nails'],
      'winter': ['winter nails', 'holiday nail art', 'snowflake nails', 'festive nails'],
      'spring': ['spring nails', 'floral nail art', 'pastel nails', 'garden nails']
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

