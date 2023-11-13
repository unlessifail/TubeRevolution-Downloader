import os
import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk
from pytube import YouTube
from pytube.exceptions import RegexMatchError
from moviepy.editor import VideoFileClip

class TubeRevolution:
    def __init__(self, master):
        self.master = master
        self.master.title("TubeRevolution Downloader")
        self.master.geometry("900x540")
        self.master.configure(bg='#eb4034')

        self.create_widgets()

    def create_widgets(self):
        # Criação dos widgets
        self.url_label = tk.Label(self.master, bg="yellow", text="URL do YouTube:")
        self.url_label.pack()

        self.url_entry = tk.Entry(self.master, width=40)
        self.url_entry.pack()

        self.format_label = tk.Label(self.master, bg="yellow", text="Baixar como:")
        self.format_label.pack()

        self.format_var = tk.StringVar()
        self.format_var.set("mp4")

        # Adicionando "wav" à lista de opções
        self.format_options = ["mp3", "mp4", "wav", "avi"]
        self.format_menu = tk.OptionMenu(self.master, self.format_var, *self.format_options)
        self.format_menu.pack()

        # Carregar a imagem 'icon.png'
        script_dir = os.path.dirname(os.path.abspath(__file__))
        icon_path = os.path.join(script_dir, "icon.png")

        try:
            icon = Image.open(icon_path)
            icon = ImageTk.PhotoImage(icon)
            self.icon_label = tk.Label(self.master, image=icon, bg='#eb4034')
            self.icon_label.image = icon
            self.icon_label.place(x=50, y=100)

        except FileNotFoundError:
            print("Arquivo 'icon.png' não encontrado.")

        self.status_label = tk.Label(self.master, text="Aguardando", font=("Arial", 12), bg='#eb4034')
        self.status_label.pack()

        self.progress_bar = ttk.Progressbar(self.master, orient=tk.HORIZONTAL, length=400, mode='determinate')
        self.progress_bar.pack()

        self.download_button = tk.Button(self.master, bg="yellow", text="Baixar", command=self.download)
        self.download_button.pack()

    def on_progress(self, stream, chunk, remaining):
        file_size = stream.filesize
        downloaded = file_size - remaining
        progress = downloaded / file_size * 100.0
        self.progress_bar['value'] = progress
        self.master.update()

    def download(self):
        url = self.url_entry.get()
        format_option = self.format_var.get()
        download_path = os.path.join(os.path.expanduser("~"), "Desktop")

        try:
            yt = YouTube(url)

            if format_option == "mp3":
                audio_stream = yt.streams.filter(only_audio=True).first()
                self.download_stream(audio_stream, download_path, f"{yt.title}.mp3")
            elif format_option == "mp4":
                video_stream = yt.streams.filter(file_extension='mp4', progressive=True).first()
                self.download_stream(video_stream, download_path, f"{yt.title}.mp4")
            elif format_option == "wav":
                audio_stream = yt.streams.filter(only_audio=True).first()
                self.download_stream(audio_stream, download_path, f"{yt.title}.wav")
            elif format_option == "avi":
                video_stream = yt.streams.filter(file_extension='mp4', progressive=True).first()
                self.download_stream(video_stream, download_path, f"{yt.title}.avi")
            else:
                print("Formato não suportado.")

        except RegexMatchError:
            print("URL do YouTube inválida.")
        except Exception as e:
            print(f"Erro: {str(e)}")

    def download_stream(self, stream, download_path, filename):
        if stream:
            self.progress_bar['value'] = 0
            self.status_label.config(text="Progresso: 0%")
            self.master.update()

            self.progress_bar['value'] = 20
            stream.download(download_path)

            original_filepath = os.path.join(download_path, stream.default_filename)
            converted_filepath = os.path.join(download_path, filename)

            if self.format_var.get() == 'avi':
                # Convertendo para AVI
                video_clip = VideoFileClip(original_filepath)
                video_clip.write_videofile(converted_filepath, codec='libx264', audio_codec='aac', threads=4, preset='ultrafast')
                video_clip.close()
                os.remove(original_filepath)
            else:
                os.rename(original_filepath, converted_filepath)

            self.progress_bar['value'] = 100
            self.status_label.config(text="Download concluído!")

            # Remover a barra de progresso após 10 segundos
            self.master.after(10000, lambda: self.progress_bar.pack_forget())

        else:
            print(f"Nenhuma stream encontrada para o formato {self.format_var.get()}.")

if __name__ == "__main__":
    root = tk.Tk()
    app = TubeRevolution(root)
    root.mainloop()
