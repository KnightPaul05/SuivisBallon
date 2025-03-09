# -*- coding: utf-8 -*-
"""
Created on Sun Mar  9 16:46:35 2025

@author: aurel
"""

import cv2
import numpy as np

# Initialisation du filtre de Kalman (4 états, 2 mesures, 2 entrées de contrôle)
kalman = cv2.KalmanFilter(6, 2)

# Position initiale de la balle
x, y = 250, 100
#vx, vy = np.random.randint(-3, 3), 0  # Vitesse initiale
vx, vy = 3, 3
ax, ay = 0, 0.5

# Définir l’état initial de la balle
kalman.statePost = np.array([[x], [y], [0], [0], [0], [0]], dtype=np.float32)

# États : [x, y, vx, vy]
dt = 1
kalman.transitionMatrix = np.array([
    [1, 0, dt, 0, 0.5 * dt**2, 0],  # x = x + vx*dt
    [0, 1, 0, dt, 0, 0.5 * dt**2],  # y = y + vy*dt
    [0, 0, 1, 0, dt, 0],  # vx = vx
    [0, 0, 0, 1, 0, dt],   # vy = vy
    [0, 0, 0, 0, 1, 0],
    [0, 0, 0, 0, 0, 1]
    ], np.float32)

# Matrice de mesure (on observe seulement x et y)
kalman.measurementMatrix = np.array([
    [1, 0, 0, 0, 0, 0],
    [0, 1, 0, 0, 0, 0]
], np.float32)

# Incertitude initiale
kalman.errorCovPost = np.eye(6, dtype=np.float32) * 1

# Matrice de bruit du processus
kalman.processNoiseCov = np.eye(6, dtype=np.float32) * 0.01

# Incertitude de mesure
kalman.measurementNoiseCov =np.eye(2, dtype=np.float32) * 100

predicted_points = []
canvas = np.zeros((500, 500, 3), dtype=np.uint8)

while True:
    # Mise à jour de la vraie dynamique (avec gravité)
    vx += ax * dt
    vy += ay * dt
    x += vx + 0.5 * ax * dt**2
    y += vy + 0.5 * ay * dt**2

    # Gestion des rebonds
    if y > 480:  # Sol
        y = 480
        vy = -vy * 0.8  # Perte d'énergie
        vx = vx * 0.95
    if x < 20 or x > 480:  # Bords
        vx = -vx * 0.9  # Rebond horizontal

    true_pos = np.array([x, y], dtype=np.float32)

    # Ajout d'une mesure bruitée
    measurement = (true_pos + np.random.randn(2) * 3).reshape(2, 1).astype(np.float32)
    
    # Prédiction avec prise en compte de l'accélération
    prediction = kalman.predict()
    predicted_points.append((int(prediction[0][0]), int(prediction[1][0])))
    
    # Correction avec la mesure
    kalman.correct(measurement)

    # Dessin
    canvas[:] = 0
    cv2.circle(canvas, (int(measurement[0][0]), int(measurement[1][0])), 5, (0, 255, 0), -1)  # Mesure (vert)
    cv2.circle(canvas, (int(prediction[0][0]), int(prediction[1][0])), 5, (0, 0, 255), -1)  # Prédiction (rouge)

    # Tracé des prédictions passées
    for p in predicted_points:
        cv2.circle(canvas, p, 2, (0, 0, 255), -1)

    cv2.imshow("Kalman Ball Tracking", canvas)

    if cv2.waitKey(30) == ord('q'):  # Sortie avec ESC
        break

cv2.destroyAllWindows()
