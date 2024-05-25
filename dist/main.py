import os
import random
import speech_recognition as sr
from pygame import mixer
import tkinter as tk
import customtkinter as ctk
from tkinter import messagebox
import threading

# Inicjalizacja silnika rozpoznawania mowy (Speech Recognition)
r = sr.Recognizer()

# Ścieżka do folderu z muzyką
music_folder = os.path.join(os.path.expanduser("~"), "MusicAssistant")

# Tworzenie folderu, jeśli nie istnieje
if not os.path.exists(music_folder):
    os.makedirs(music_folder)

# Wczytanie listy piosenek
songs = [song for song in os.listdir(music_folder) if song.endswith('.mp3')]

# Inicjalizacja odtwarzacza muzyki
mixer.init()

# Zmienna do śledzenia trybu odtwarzania i aktualnie odtwarzanej piosenki
play_random = False
current_song_index = 0

# Funkcja do odtwarzania muzyki
def play_music():
    global current_song_index
    if songs:
        mixer.music.load(os.path.join(music_folder, songs[current_song_index]))
        mixer.music.play()
        song_label.configure(text=f"Odtwarzanie: {songs[current_song_index]}")
    else:
        song_label.configure(text="Brak piosenek w folderze MusicAssistant.")

# Funkcja do odtwarzania następnej piosenki
def next_song():
    global current_song_index
    current_song_index = (current_song_index + 1) % len(songs)
    play_music()

# Funkcja do odtwarzania poprzedniej piosenki
def previous_song():
    global current_song_index
    current_song_index = (current_song_index - 1) % len(songs)
    play_music()

# Funkcja do zatrzymania odtwarzania
def pause_music():
    mixer.music.pause()

# Funkcja do wznowienia odtwarzania
def unpause_music():
    mixer.music.unpause()

# Funkcja do odtwarzania tej samej piosenki
def play_same_song():
    play_music()

# Funkcja do nasłuchiwania komend głosowych
def listen_command():
    while True:
        with sr.Microphone() as source:
            print("Podaj komendę: ")
            audio = r.listen(source)
            try:
                command = r.recognize_google(audio, language='en-EN')
                print(f"Rozpoznano komendę: {command}")
            except sr.UnknownValueError:
                print("Nie rozpoznano komendy.")
                continue
            
            if "okay music" in command.lower():
                listen_for_music_commands()

# Funkcja do nasłuchiwania komend muzycznych
def listen_for_music_commands():
    with sr.Microphone() as source:
        print("Nasłuchiwanie komend muzycznych: ")
        audio = r.listen(source)
        try:
            command = r.recognize_google(audio, language='en-EN')
            print(f"Rozpoznano komendę: {command}")
        except sr.UnknownValueError:
            messagebox.showerror("Błąd", "Nie rozpoznano komendy.")
            return

    global play_random, current_song_index

    if "play" in command.lower():
        play_music()
    elif "next" in command.lower():
        next_song()
    elif "previous" in command.lower():
        previous_song()
    elif "play random" in command.lower():
        play_random = True
        current_song_index = random.randint(0, len(songs) - 1)
        play_music()
    elif "play normal" in command.lower():
        play_random = False
        current_song_index = 0
        play_music()
    elif "pause" in command.lower() or "music stop" in command.lower():
        pause_music()
    elif "resume" in command.lower():
        unpause_music()
    elif "again" in command.lower():
        play_same_song()
    elif command.lower() == "exit":
        root.quit()

# Tworzenie GUI
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("dark-blue")

root = ctk.CTk()
root.title("Music Assistant")
root.geometry("600x400")  # Zmieniona wielkość okna

# Dodanie ikony
icon_path = "icon.ico"  # Zmień na ścieżkę do swojej ikony
if os.path.exists(icon_path):
    root.iconbitmap(icon_path)

frame = ctk.CTkFrame(master=root)
frame.pack(pady=20, padx=20, fill="both", expand=True)

title_label = ctk.CTkLabel(master=frame, text="Music Assistant", font=("Arial", 20))
title_label.pack(pady=10)

song_label = ctk.CTkLabel(master=frame, text="Brak piosenek w folderze MusicAssistant.", font=("Arial", 14))
song_label.pack(pady=10)

play_button = ctk.CTkButton(master=frame, text="Play", command=play_music)
play_button.pack(pady=5)

next_button = ctk.CTkButton(master=frame, text="Next", command=next_song)
next_button.pack(pady=5)

previous_button = ctk.CTkButton(master=frame, text="Previous", command=previous_song)
previous_button.pack(pady=5)

pause_button = ctk.CTkButton(master=frame, text="Pause", command=pause_music)
pause_button.pack(pady=5)

unpause_button = ctk.CTkButton(master=frame, text="Resume", command=unpause_music)
unpause_button.pack(pady=5)

# Uruchomienie nasłuchiwania komend w osobnym wątku
command_thread = threading.Thread(target=listen_command, daemon=True)
command_thread.start()

root.mainloop()
