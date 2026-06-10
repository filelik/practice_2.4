"""Задача 2. GUI-приложение случайных фото котов и собак."""

import io
import tkinter as tk
from tkinter import ttk, messagebox

import requests
from PIL import Image, ImageTk

CAT_API = "https://api.thecatapi.com/v1/images/search"
DOG_API = "https://dog.ceo/api/breeds/image/random"


class AnimalApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Случайные коты и собаки")
        self.geometry("720x620")
        self.current_image = None

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Получить кота", command=self.get_cat).pack(side="left", padx=10)
        ttk.Button(button_frame, text="Получить собаку", command=self.get_dog).pack(side="left", padx=10)

        self.status = ttk.Label(self, text="Нажмите кнопку для загрузки изображения.")
        self.status.pack(pady=5)

        self.image_label = ttk.Label(self)
        self.image_label.pack(fill="both", expand=True, padx=10, pady=10)

    def get_cat(self):
        try:
            response = requests.get(CAT_API, timeout=10)
            response.raise_for_status()
            image_url = response.json()[0]["url"]
            self.load_image(image_url, "Кот загружен.")
        except (requests.RequestException, KeyError, IndexError, ValueError) as error:
            messagebox.showerror("Ошибка", f"Не удалось получить кота: {error}")

    def get_dog(self):
        try:
            response = requests.get(DOG_API, timeout=10)
            response.raise_for_status()
            image_url = response.json()["message"]
            self.load_image(image_url, "Собака загружена.")
        except (requests.RequestException, KeyError, ValueError) as error:
            messagebox.showerror("Ошибка", f"Не удалось получить собаку: {error}")

    def load_image(self, image_url, success_text):
        try:
            response = requests.get(image_url, timeout=15)
            response.raise_for_status()
            image = Image.open(io.BytesIO(response.content))
            image.thumbnail((650, 500))
            self.current_image = ImageTk.PhotoImage(image)
            self.image_label.config(image=self.current_image)
            self.status.config(text=success_text)
        except Exception as error:
            messagebox.showerror("Ошибка", f"Не удалось загрузить изображение: {error}")


if __name__ == "__main__":
    AnimalApp().mainloop()
