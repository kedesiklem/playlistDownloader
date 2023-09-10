import os
import tkinter as tk
from tkinter import messagebox, ttk
from pytube import YouTube, Playlist
from pytube.streams import Stream


class VideoSelectorApp:
    def __init__(self, root, video_urls):
        self.root = root
        self.root.title("Sélection des vidéos YouTube")

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
            self.root, text="Sélectionner les vidéos", command=self.show_summary
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
        for i, url in enumerate(self.video_urls):
            try:
                video = YouTube(url)
                self.video_listbox.insert(tk.END, f"{i+1}. {video.title}")
                print(f"Noms des vidéos récupérés ({i+1}/{len(self.video_urls)})")
            except Exception as e:
                print(
                    f"Erreur lors de la récupération des informations pour l'URL {url}: {str(e)}"
                )
        print("Récupération des noms des vidéos terminée.")

    def show_summary(self):
        selected_indices = self.video_listbox.curselection()
        if selected_indices:
            self.selected_videos = [
                self.video_urls[index] for index in selected_indices
            ]

            selected_video_names = [
                self.video_listbox.get(index).split(". ", 1)[1]
                for index in selected_indices
            ]
            summary_text = "Vidéos sélectionnées : \n" + "\n".join(selected_video_names)

            summary_window = tk.Toplevel(self.root)
            summary_window.title("Récapitulatif")
            summary_label = tk.Label(summary_window, text=summary_text)
            summary_label.pack(padx=10, pady=10)

            confirm_button = tk.Button(
                summary_window,
                text="Confirmer la sélection",
                command=summary_window.quit,
            )
            confirm_button.pack(pady=10)
        else:
            messagebox.showwarning(
                "Avertissement", "Veuillez sélectionner au moins une vidéo."
            )

    def select_all(self):
        self.video_listbox.select_set(0, tk.END)


def download_video(
    url, resolution="720p", destination_path="download", audio_only=False
):
    try:

        def progress_function(stream, chunk, bytes_remaining):
            percent = (1 - bytes_remaining / stream.filesize) * 100
            print(f"Downloading... {percent:.2f}% complete", end="\r")

        video = YouTube(url, on_progress_callback=progress_function)

        if audio_only:
            # Si l'option "Télécharger seulement l'audio" est sélectionnée,
            # nous utilisons le format audio MP4 pour télécharger uniquement l'audio.
            audio_stream = video.streams.filter(only_audio=True).first()
            if audio_stream:
                audio_stream.download(output_path=destination_path)
                audio_filename = audio_stream.default_filename
                # Renommer le fichier en .mp3
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
    app = VideoSelectorApp(root, video_urls)
    root.geometry("900x600")  # Définir une taille initiale
    root.mainloop()

    print("Vidéos sélectionnées à télécharger :")
    for url in app.selected_videos:
        print(url)

    audio_only = app.audio_only_var.get()

    for url in app.selected_videos:
        download_video(url, destination_path=download_path, audio_only=audio_only)


def get_playlist_info_from_user():
    playlist_url = input("Entrez l'URL de la playlist YouTube : ")
    download_path = input("Entrez le chemin d'accès pour enregistrer les vidéos : ")

    return playlist_url, download_path


# Exemple d'utilisation :
if __name__ == "__main__":
    playlist_url, download_path = get_playlist_info_from_user()
    main(playlist_url, download_path)
