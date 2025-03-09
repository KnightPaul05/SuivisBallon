import cv2 as cv
import time
import numpy as np

class VideoPlayer:
    def __init__(self, video_path, frame_rate=30):
        '''
        Initialise le lecteur vidéo avec le chemin de la vidéo et le FPS'''
        
        self.video_path = video_path
        self.frame_rate = frame_rate
        self.cap = cv.VideoCapture(video_path)

        if not self.cap.isOpened():
            raise ValueError(f"Impossible douvrir la vidée : {video_path}")

        self.gap =1/frame_rate
        self.start_time = time.time()
        self.frame_count = 0
        self.previous_frame = None

    
    def process_frame(self, frame):
        '''Applique un traitement pour détecter les mouvements et trouver lobjet le plus rond'''

        gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) # conversion en niveau de gris
        blur = cv.GaussianBlur(gray, (5,5),0) # réduction du bruit

        # on stock la premier frame
        if self.previous_frame is None:
            self.previous_frame = blur
            return frame
        
        # Calcul de la différence absolue entre les frames successives
        frame_diff = cv.absdiff(self.previous_frame, blur)

        # Seuillage pour optenir une image binaire
        _, thresh = cv.threshold(frame_diff, 30, 255, cv.THRESH_BINARY) 

        #Dilatation pour agrandir les zones en mouvement
        kernel = np.ones((5,5), np.uint8)
        dilated = cv.dilate(thresh,kernel, iterations=2)

        #trouver les contoures
        contours, _ = cv.findContours(dilated, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)

        best_circle = None
        best_score = 0

        #Analyse des contours pour trouver les plus rond des ronds
        for  cnt in contours:
            (x,y), radius = cv.minEnclosingCircle(cnt)
            if radius > 10: # On filtre les petits objets
                circle_area = np.pi*(radius**2)
                contour_area = cv.contourArea(cnt)

                if contour_area > 0:
                    circularity = contour_area  / circle_area # Score de circularité

                    if circularity > best_score:
                        best_score = circularity
                        best_circle = (int(x), int(y), int(radius))
        
        # Dessiner le meuilleur cerle détecté
        if best_circle:
            x, y, radius = best_circle
            cv.circle(frame, (x,y), radius, (0,255,0),2)
            cv.putText(frame,"Cercle detecte", (x-20,y-20), cv.FONT_HERSHEY_SIMPLEX, 0.5,(0,255,0),2)

        self.previous_frame = blur
        return frame
    

    def show_frame_difference(self):
        while self.cap.isOpened():
            ret, frame = self.cap.read()
            if not ret:
                print('Fin de la vidéo')
                break
            
            # Appliquer le traitement pour obtenir la différence de frames
            gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)  # Conversion en niveau de gris
            blur = cv.GaussianBlur(gray, (15, 15), 0)  # Réduction du bruit

            # Stocke la première frame
            if self.previous_frame is None:
                self.previous_frame = blur
                cv.imshow("Frame Difference", frame)  # Affiche la frame originale
                continue  # Passe à la prochaine frame

            # Calcul de la différence absolue entre les frames successives
            frame_diff = cv.absdiff(self.previous_frame, blur)

            # Seuillage pour obtenir une image binaire
            _, thresh = cv.threshold(frame_diff, 30, 255, cv.THRESH_BINARY)

            # Affichage de la différence (l'image binaire)
            cv.imshow("Frame Difference", thresh)

            # Met à jour la frame précédente
            self.previous_frame = blur

            if cv.waitKey(30) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv.destroyAllWindows()


    def play(self):
        '''Joue la vidéo à la cadance spécifique.'''
        while True:
            ret, frame = self.cap.read()
            if not ret:
                print("Fin de la vidéo")
                break
        
            #Appliquer le traitement d'image
            processed_frame = self.process_frame(frame)

            #Calcule du temps d'attente pour la prochain frame
            frame_delay = int((self.start_time + self.frame_count*self.gap - time.time())*1000)
            if cv.waitKey(max(frame_delay,1)) == ord('q'):
                break

            cv.imshow("Video Processing", processed_frame)
            self.frame_count += 1
        
        self.cap.release()
        cv.destroyAllWindows()

# if __name__ == '__main__':
#     video = VideoPlayer("Stephen Curry vs Klay Thompson in 2015 3 Point contest.mp4", frame_rate=30)
#     video.play()
            

if __name__ == '__main__':
    video = VideoPlayer("Stephen Curry vs Klay Thompson in 2015 3 Point contest.mp4")  # Instanciation de ta classe
    video.show_frame_difference()  # Lancer l'affichage des différences

