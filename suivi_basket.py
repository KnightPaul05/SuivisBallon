# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 16:46:35 2025

@author: aurel
"""

import cv2
import numpy as np

# Initialisation du filtre de Kalman
kalman = cv2.KalmanFilter(4, 2)  # 4 variables d'état (x, y, dx, dy), 2 mesures (x, y)
kalman.measurementMatrix = np.array([[1, 0, 0, 0],
                                     [0, 1, 0, 0]], np.float32)
kalman.transitionMatrix = np.array([[1, 0, 1, 0],
                                    [0, 1, 0, 1],
                                    [0, 0, 1, 0],
                                    [0, 0, 0, 1]], np.float32)
kalman.processNoiseCov = np.eye(4, dtype=np.float32) * 0.03

# Position initiale
true_x, true_y = 200, 200
predictions = []
measurements = []

# Création de l'affichage
frame = np.zeros((400, 400, 3), dtype=np.uint8)

for i in range(100):
    # Simulation du mouvement avec du bruit
    true_x += np.random.randint(-5, 6)
    true_y += np.random.randint(-5, 6)
    meas = np.array([[np.float32(true_x)], [np.float32(true_y)]])

    # Prédiction du filtre de Kalman
    prediction = kalman.predict()
    kalman.correct(meas)
    
    # Sauvegarde des valeurs
    measurements.append((true_x, true_y))
    predictions.append((int(prediction[0]), int(prediction[1])))
    
    # Affichage
    frame.fill(0)
    for j in range(len(measurements)):
        cv2.circle(frame, measurements[j], 2, (0, 255, 0), -1)  # Mesures en vert
        cv2.circle(frame, predictions[j], 2, (0, 0, 255), -1)  # Prédictions en rouge
    
    cv2.imshow("Kalman Filter", frame)
    if cv2.waitKey(100) == ord('q'):
        break

cv2.destroyAllWindows()