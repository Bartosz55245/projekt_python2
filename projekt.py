import numpy as np
import pandas as pd
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import tkinter as tk
from tkinter import messagebox

#funckja do rekomendacji filmów
def recommend_movies():
    movie_name = movie_name_entry.get()
    find_close_match = difflib.get_close_matches(movie_name, alltitle_list)
    if not find_close_match:
        messagebox.showinfo("Info", "Nie znaleziono żadnych dopasowań.")
    else:
        close_match = find_close_match[0]
        movie_index = movies_data[movies_data.title == close_match]["index"].values[0]
        wynik_podobienstwa = list(enumerate(podobienstwo[movie_index]))
        sorted_podobienstwo = sorted(wynik_podobienstwa, key=lambda x: x[1], reverse=True)

        recommendations = []
        i = 1
        for movie in sorted_podobienstwo:
            index = movie[0]
            title_index = movies_data[movies_data.index == index]["title"].values[0]
            if i < 11:
                recommendations.append(f"{i}. {title_index}")
                i += 1

        recommendations_text.set("\n".join(recommendations))

#wczytanie danych z pliku csv
movies_data = pd.read_csv('movies.csv')

#wybranie potrzebnych informacji
selected_features = ["genres", "keywords", "tagline", "cast", "director"]
for feature in selected_features:
    movies_data[feature] = movies_data[feature].fillna("")

combined_features = movies_data["genres"] + " " + movies_data["keywords"] + " " + movies_data["tagline"] + " " + movies_data["cast"] + " " + movies_data["director"]

#stworzenie wektorów liczb
vectorizer = TfidfVectorizer()
feature_vectors = vectorizer.fit_transform(combined_features)

#podobienstwo kosinusowe
podobienstwo = cosine_similarity(feature_vectors)

#lista wszystkich tytułów
alltitle_list = movies_data["title"].tolist()

#stworzenie interfejsu
root = tk.Tk()

root.title("System Polecania Filmów")
root.geometry("500x400")
tk.Label(root, text="Podaj nazwę ulubionego filmu:", font=('Arial', 18)).pack(pady=15)

movie_name_entry = tk.Entry(root, width=50)
movie_name_entry.pack(pady=10)

recommend_button = tk.Button(root, text="Rekomenduj filmy", command=recommend_movies)
recommend_button.pack(pady=10)

recommendations_text = tk.StringVar()
recommendations_label = tk.Label(root, textvariable=recommendations_text, justify="left")
recommendations_label.pack(pady=20)

root.mainloop()
