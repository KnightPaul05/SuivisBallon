# -*- coding: utf-8 -*-
"""
Created on Wed Mar  5 21:54:46 2025

@author: aurel
"""

import cv2 as cv
import sys
import time

cap = cv.VideoCapture('IMG_1984.mov')

# Vérifiez si la vidéo est ouverte correctement
if not cap.isOpened():
    print("Erreur lors de l'ouverture du fichier vidéo")
    sys.exit()
    
# Définir le FPS
fps = 30
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