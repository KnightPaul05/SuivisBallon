# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 21:54:46 2025

@author: aurel
"""

import cv2 as cv
import sys
import time

def redefinition_frame(frame_rate,video_path):
    cap = cv.VideoCapture(video_path)
        
    # Définir le FPS
    fps = frame_rate
    # intervalle de temps entre 2 frames
    gap = 1/fps
    # début de la mesure de temps de la vidéo
    start = time.time()
    # nombre de frames
    count = 0

    while True:
        # lecture d'une frame
        ret, frame = cap.read()
        if not ret:
            print("Fin de la vidéo.")
            break
        
        # calcul du temps à attendre pour afficher la prochaine frame
        frame_delay = int((start + count * gap - time.time()) * 1000)
        if cv.waitKey(max(frame_delay, 1)) == ord('q'):
            break
        
        # affichage de la frame
        cv.imshow("Video", frame)
        
        count += 1
        
    cv.destroyAllWindows()

if __name__ == '__main__':
    lancer_video = redefinition_frame(100,"Stephen Curry vs Klay Thompson in 2015 3 Point contest.mp4")