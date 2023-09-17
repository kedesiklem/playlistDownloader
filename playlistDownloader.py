#!/usr/bin/env python3
import os
import tkinter as tk
from tkinter import messagebox
from pytube import YouTube, Playlist
from concurrent.futures import ThreadPoolExecutor


class VideoSelectorApp:
    def __init__(self, root, video_urls, download_path):
        self.root = root
        self.root.title("Sélection des vidéos YouTube")

        self.download_path = download_path
        self.video_urls = video_urls
        self.selected_videos = []

        self.create_ui()

    def create_ui(self):
        self.label = tk.Label(self.root, text="Sélectionnez les vidéos à conserver:")
        self.label.pack(pady=10)

        self.scrollbar = tk.Scrollbar(self.root, orient=tk.VERTICAL)
        self.video_listbox = tk.Listbox(
            self.root,
            selectmode=tk.MULTIPLE,
            yscrollcommand=self.scrollbar.set,
            width=40,
            height=10,
        )
        self.scrollbar.config(command=self.video_listbox.yview)
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.video_listbox.pack(fill=tk.BOTH, expand=True)

        self.load_video_titles()

        self.select_button = tk.Button(
            self.root, text="Lancer le téléchargement", command=self.show_summary
        )
        self.select_button.pack(pady=10)

        self.select_all_button = tk.Button(
            self.root, text="Sélectionner tout", command=self.select_all
        )
        self.select_all_button.pack(pady=10)

        self.audio_only_var = tk.BooleanVar()
        self.audio_only_checkbox = tk.Checkbutton(
            self.root,
            text="Télécharger seulement l'audio",
            variable=self.audio_only_var,
        )
        self.audio_only_checkbox.pack()

    def load_video_titles(self):
        print("Récupération des noms des vidéos...")

        def fetch_video_title(index, url):  # Inversez l'ordre des arguments
            try:
                video = YouTube(url)
                print(
                    f"\tNoms des vidéos récupérés ({index + 1}/{len(self.video_urls)})"
                )
                return index, f"{video.title}"  # Retournez l'index en plus du titre
            except Exception as e:
                print(
                    f"Erreur lors de la récupération des informations pour l'URL {url}: {str(e)}"
                )
                return index, None  # Retournez l'index en cas d'erreur

        with ThreadPoolExecutor() as executor:
            # Utilisez une fonction lambda pour mapper les URL et les index
            results = executor.map(
                lambda args: fetch_video_title(*args),
                ((i, url) for i, url in enumerate(self.video_urls)),
            )

        for index, result in results:
            if result:
                self.video_listbox.insert(tk.END, f"{index + 1}. {result}")

        print("---")

    def show_summary(self):
        print("Préparation du récapitulatif")
        self.selected_videos = [
            self.video_urls[index] for index in self.video_listbox.curselection()
        ]

        if self.selected_videos:
            total_size_bytes = 0
            selected_video_names = []

            print("\tRécupération des tailles de fichier")
            for i, video_url in enumerate(self.selected_videos):
                try:
                    video = YouTube(video_url)

                    if self.audio_only_var.get():
                        video_stream = video.streams.filter(only_audio=True).first()
                    else:
                        video_stream = video.streams.filter(
                            progressive=True, file_extension="mp4"
                        ).first()

                    if video_stream:
                        video_size_bytes = video_stream.filesize
                        total_size_bytes += video_size_bytes
                        selected_video_names.append(
                            f"{video.title} ({human_readable_size(video_size_bytes)})"
                        )
                        print(
                            f"\t\tInfos vidéos récupérées ({i+1}/{len(self.selected_videos)})"
                        )
                    else:
                        print(f"Aucun flux trouvé pour '{video.title}'.")
                except Exception as e:
                    print(
                        f"Erreur lors de la récupération des informations pour l'URL {video_url}: {str(e)}"
                    )

            total_size_readable = human_readable_size(total_size_bytes)

            summary_text = "Vidéos sélectionnées : \n" + "\n".join(selected_video_names)
            summary_text += (
                f"\n\nTaille totale du téléchargement : {total_size_readable}"
            )

            summary_window = tk.Toplevel(self.root)
            summary_window.title("Récapitulatif")

            # Create a Text widget for the summary with vertical scrolling
            summary_text_widget = tk.Text(summary_window, wrap=tk.WORD)
            summary_text_widget.pack(padx=10, pady=10, fill=tk.BOTH, expand=True)

            # Insert the summary text into the Text widget
            summary_text_widget.insert(tk.END, summary_text)

            confirm_button = tk.Button(
                summary_window,
                text="Confirmer la sélection",
                command=self.confirm_and_download,
            )
            confirm_button.pack(pady=10)
            print("---")
        else:
            messagebox.showwarning(
                "Avertissement", "Veuillez sélectionner au moins une vidéo."
            )

    def select_all(self):
        self.video_listbox.select_set(0, tk.END)

    def confirm_and_download(self):
        # Fermer la fenêtre de récapitulatif
        self.root.winfo_children()[-1].destroy()  # Détruire la dernière fenêtre
        # Appeler la fonction de téléchargement pour les vidéos sélectionnées
        audio_only = self.audio_only_var.get()
        for url in self.selected_videos:
            download_video(
                url, destination_path=self.download_path, audio_only=audio_only
            )


def download_video(
    url, resolution="720p", destination_path="download", audio_only=False
):
    try:

        def progress_function(stream, chunk, bytes_remaining):
            percent = (1 - bytes_remaining / stream.filesize) * 100
            print(f"Downloading... {percent:.2f}% complete", end="\r")

        video = YouTube(url, on_progress_callback=progress_function)

        if audio_only:
            audio_stream = video.streams.filter(only_audio=True).first()
            if audio_stream:
                audio_stream.download(output_path=destination_path)
                audio_filename = audio_stream.default_filename
                mp3_filename = os.path.splitext(audio_filename)[0] + ".mp3"
                os.rename(
                    os.path.join(destination_path, audio_filename),
                    os.path.join(destination_path, mp3_filename),
                )
                print(f"Audio de '{video.title}' a été téléchargé au format MP3.")
            else:
                print(f"Aucun flux audio trouvé pour '{video.title}'.")
        else:
            stream = video.streams.filter(res=resolution).first()
            if stream:
                stream.download(output_path=destination_path)
                print(
                    f"Vidéo '{video.title}' a été téléchargée avec une résolution de {resolution}."
                )
            else:
                print(f"Aucun flux vidéo trouvé pour '{video.title}'.")

    except Exception as e:
        print(
            f"Une erreur s'est produite lors du téléchargement de la vidéo : {str(e)}"
        )


def human_readable_size(size_in_bytes):
    for unit in ["B", "KB", "MB", "GB", "TB"]:
        if size_in_bytes < 1024.0:
            break
        size_in_bytes /= 1024.0
    return f"{size_in_bytes:.2f} {unit}"


def main(playlist_url, download_path):
    try:
        playlist = Playlist(playlist_url)
        video_urls = playlist.video_urls
        if not video_urls:
            print("Aucune vidéo trouvée dans la playlist.")
            return
    except Exception as e:
        print(f"Erreur lors de la récupération de la playlist : {str(e)}")
        return

    root = tk.Tk()
    VideoSelectorApp(root, video_urls, download_path)
    root.geometry("900x600")  # Définir une taille initiale
    root.mainloop()


def get_playlist_info_from_user():
    playlist_url = input("Entrez l'URL de la playlist YouTube : ")
    # download_path = input("Entrez le chemin d'accès pour enregistrer les vidéos : ")
    download_path = "Download"

    return playlist_url, download_path


if __name__ == "__main__":
    playlist_url, download_path = get_playlist_info_from_user()
    main(playlist_url, download_path)
