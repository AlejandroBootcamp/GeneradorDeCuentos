import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk


import requests
from io import BytesIO
from PIL import Image, ImageTk
import tkinter as tk

class Historia:
    def __init__(self, image_url, historia):
        # Descargar la imagen desde la URL
        response = requests.get(image_url)
        if response.status_code == 200:
            image_data = BytesIO(response.content)  # Convertir a BytesIO
            self.image = Image.open(image_data)  # Abrir con Pillow
        else:
            print("Error al descargar la imagen")
            return

        # Crear ventana
        self.root = tk.Tk()
        self.root.title("Generador de historias")

        # Redimensionar la imagen
        self.image = self.image.resize((400, 300), Image.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(self.image)

        # Crear un Label para la imagen
        label_image = tk.Label(self.root, image=self.image_tk)
        label_image.pack(pady=10)

        # Crear un Label para el texto
        label_text = tk.Label(self.root, text=historia, font=("Arial", 14), wraplength=400, justify="center")
        label_text.pack(pady=10)

        # Mostrar la ventana
        self.root.mainloop()



