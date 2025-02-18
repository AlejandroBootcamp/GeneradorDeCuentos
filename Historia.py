import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import requests
from io import BytesIO


class Historia:
    def __init__(self, image_url, historia):
        try:
            response = requests.get(image_url)
            response.raise_for_status()  # Lanza un error si el request falla
            image_data = BytesIO(response.content)
            try:
                self.image = Image.open(image_data)
            except Exception as e:
                print(f"Error opening image: {e}")
                return
        except requests.RequestException as e:
            print(f"Error downloading image: {e}")
            return

        # Crear ventana antes de descargar la imagen
        self.root = tk.Tk()
        self.root.title("Story Generator")

        # Redimensionar sin modificar la imagen original
        resized_image = self.image.resize((400, 300), Image.LANCZOS)
        self.image_tk = ImageTk.PhotoImage(resized_image)

        # Mostrar imagen en la ventana
        label_image = tk.Label(self.root, image=self.image_tk)
        label_image.pack(pady=10)

        # Mostrar texto de la historia
        label_text = tk.Label(self.root, text=historia, font=("Arial", 14), wraplength=400, justify="center")
        label_text.pack(pady=10)

        # Agregar botón de salida
        exit_button = tk.Button(self.root, text="Cerrar", command=self.root.quit)
        exit_button.pack(pady=10)

        # Iniciar la ventana
        self.root.mainloop()