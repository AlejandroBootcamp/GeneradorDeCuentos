import tkinter as tk
from tkinter import Label
from PIL import Image, ImageTk
import requests
from io import BytesIO


class Historia:
    def __init__(self, image_urls, historias):
        self.root = tk.Tk()
        self.root.title("Story Generator")

        # Crear un contenedor para las historias
        frame = tk.Frame(self.root)
        frame.pack(padx=20, pady=20)

        # Iterar sobre las imágenes e historias
        for i, (image_url, historia) in enumerate(zip(image_urls, historias)):
            try:
                response = requests.get(image_url)
                response.raise_for_status()
                image_data = BytesIO(response.content)
                image = Image.open(image_data)

                # Redimensionar imagen sin modificar la original
                resized_image = image.resize((300, 200), Image.LANCZOS)
                image_tk = ImageTk.PhotoImage(resized_image)

                # Mostrar imagen en la ventana
                label_image = tk.Label(frame, image=image_tk)
                label_image.image = image_tk  # Mantener referencia para evitar que se borre
                label_image.grid(row=i, column=0, padx=10, pady=10)

                # Mostrar texto de la historia
                label_text = tk.Label(frame, text=historias[i], font=("Arial", 12), wraplength=300, justify="left")
                label_text.grid(row=i, column=1, padx=10, pady=10)

            except requests.RequestException as e:
                print(f"Error downloading image {i}: {e}")
            except Exception as e:
                print(f"Error opening image {i}: {e}")

        # Agregar botón de salida
        exit_button = tk.Button(self.root, text="Cerrar", command=self.root.quit)
        exit_button.pack(pady=10)

        # Iniciar la ventana
        self.root.mainloop()
