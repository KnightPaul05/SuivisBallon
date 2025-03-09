import cv2
import tkinter as tk
from tkinter import filedialog, messagebox
from controle_video import redefinition_frame

#vidéo d'origine pour ne pas avoir a chercher une vidéo à chaque fois
video_origin = "Stephen Curry vs Klay Thompson in 2015 3 Point contest.mp4"

def play_video(video_path):
    """Lit et affiche la vidéo avec openCV"""

    # Ici il faut ajouter le programmme d'aurelien pour ajouter le frameret

    lancer_video = redefinition_frame(100,video_path)


def open_file_dialog():
    '''demande la sélection de vidéo'''
    file_path = filedialog.askopenfilename(
        title="Choisir la vidéo",
        filetype=[("fichier vidéo","*.mp4;*.avi;*.mov;*.mkv")]
    )
    
    if file_path:
        play_video(file_path)

def ask_video_choice():
    '''Deùande à l'utilisateur s'il veut choisir une vidéo.'''
    root = tk.Tk()
    root.withdraw() 

    response = messagebox.askyesno("Choix de la vidéo","Voulez-vous choisir une autre vidéo")

    if response:
        open_file_dialog()
    else:
     play_video(video_origin)

if __name__ == '__main__':
    ask_video_choice()