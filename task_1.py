"""Задача 1. GUI-приложение погоды через OpenWeatherAPI."""

import io
import os
import tkinter as tk
from tkinter import ttk, messagebox

import requests
from PIL import Image, ImageTk

WEATHER_URL = "https://api.openweathermap.org/data/2.5/weather"
ICON_URL = "https://openweathermap.org/img/wn/{icon}@2x.png"


class WeatherApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Погода OpenWeather")
        self.geometry("480x390")
        self.icon_image = None

        frame = ttk.Frame(self)
        frame.pack(fill="x", padx=15, pady=15)

        ttk.Label(frame, text="Город:").grid(row=0, column=0, sticky="w")
        self.city_entry = ttk.Entry(frame, width=30)
        self.city_entry.grid(row=0, column=1, padx=5, pady=5)
        self.city_entry.insert(0, "Tomsk")

        ttk.Label(frame, text="API key:").grid(row=1, column=0, sticky="w")
        self.key_entry = ttk.Entry(frame, width=30, show="*")
        self.key_entry.grid(row=1, column=1, padx=5, pady=5)
        self.key_entry.insert(0, os.getenv("OPENWEATHER_API_KEY", ""))

        ttk.Button(frame, text="Показать погоду", command=self.load_weather).grid(row=2, column=0, columnspan=2, pady=10)

        self.result_label = ttk.Label(self, text="Введите город и API key.", font=("Arial", 13), justify="center")
        self.result_label.pack(pady=15)

        self.icon_label = ttk.Label(self)
        self.icon_label.pack(pady=5)

        ttk.Label(
            self,
            text="API key можно получить на сайте openweathermap.org.\nТакже можно задать переменную окружения OPENWEATHER_API_KEY.",
            justify="center",
        ).pack(pady=10)

    def load_weather(self):
        city = self.city_entry.get().strip()
        api_key = self.key_entry.get().strip()
        if not city:
            messagebox.showwarning("Ошибка", "Введите название города.")
            return
        if not api_key:
            messagebox.showwarning("Ошибка", "Введите API key OpenWeatherAPI.")
            return

        try:
            response = requests.get(
                WEATHER_URL,
                params={"q": city, "appid": api_key, "units": "metric", "lang": "ru"},
                timeout=10,
            )
            data = response.json()
            if response.status_code != 200:
                messagebox.showerror("Ошибка", data.get("message", "Не удалось получить погоду."))
                return

            temp = data["main"]["temp"]
            feels_like = data["main"]["feels_like"]
            description = data["weather"][0]["description"]
            icon = data["weather"][0]["icon"]
            self.result_label.config(
                text=f"Город: {data.get('name', city)}\nТемпература: {temp:.1f} °C\nОщущается как: {feels_like:.1f} °C\nПогода: {description}"
            )
            self.load_icon(icon)
        except (requests.RequestException, KeyError, ValueError) as error:
            messagebox.showerror("Ошибка", f"Не удалось обработать данные погоды: {error}")

    def load_icon(self, icon_code):
        try:
            icon_response = requests.get(ICON_URL.format(icon=icon_code), timeout=10)
            icon_response.raise_for_status()
            image = Image.open(io.BytesIO(icon_response.content)).resize((100, 100))
            self.icon_image = ImageTk.PhotoImage(image)
            self.icon_label.config(image=self.icon_image)
        except Exception as error:
            self.icon_label.config(image="")
            messagebox.showwarning("Иконка", f"Не удалось загрузить иконку погоды: {error}")


if __name__ == "__main__":
    WeatherApp().mainloop()
