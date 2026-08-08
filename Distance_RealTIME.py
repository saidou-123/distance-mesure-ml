# install opencv "pip install opencv-python" 
import cv2 

# distance de la camera à l'object(face) mesuré 
# centimeter 
Known_distance = 50

# Largeur de la face dans le monde réel ou Plan d’objet 
# centimeter 
Known_width = 14.3

# Couleurs 
GREEN = (0, 255, 0) 
RED = (0, 0, 255) 
WHITE = (255, 255, 255) 
BLACK = (0, 0, 0) 

# definition de la police (type de caractères) 
fonts = cv2.FONT_HERSHEY_COMPLEX 

# face detector object qui charge le fichier XML issu de l'entrainement avec de images positives (images avec visages) et des images négatives (images sans visages)
face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml") 

# fonction de repérage de la distance focale 
def Focal_Length_Finder(measured_distance, real_width, width_in_rf_image): 

	# détermination de la distance focale 
	focal_length = (width_in_rf_image * measured_distance) / real_width 
	return focal_length 

# fonction destimation de la distance 
def Distance_finder(Focal_Length, real_face_width, face_width_in_frame): 

	distance = (real_face_width * Focal_Length)/face_width_in_frame 

	# return la distance 
	return distance 


def face_data(image): 

	face_width = 0 # initialisation de largeur face à zero 

	# convertir l'image couleur en image niveau de gris 
	gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY) 

	# detection de la face dans l'image 
	faces = face_detector.detectMultiScale(gray_image, 1.1, 3) 

	# boucle pour la détection des face dans l'image 
	# récuperer les coordinées x, y , largeur et hauteur 
	for (x, y, w, h) in faces: 

		# dessiner un rectangle sur la face 
		cv2.rectangle(image, (x, y), (x+w, y+h), GREEN, 2) 

		# récuperer les pixels de la largeur de la face 
		face_width = w 

	# return les pixels de la largeur de la face 
	return face_width 


# lire reference_image depuis le répertoire 
ref_image = cv2.imread("Ref_image.png") 

# trouver la largeur de face (pixels) dans la référence_image 
ref_image_face_width = face_data(ref_image) 

# obtenir le focal en appellant "Focal_Length_Finder" 
# largeur de la face (pixels), 
# Known_distance(centimeters), 
# known_width(centimeters) 
Focal_length_found = Focal_Length_Finder( 
	Known_distance, Known_width, ref_image_face_width) 

print(Focal_length_found) 

# montrer l'image de reference 
cv2.imshow("ref_image", ref_image) 

# initialisation de l'objet camera 
# capturer les images via caméra, un chiffre zéro signifie webcam de l'ordinateur sinon si c'est celui d'un téléphone mettre son adresse IP optenu via son appli IP webcam du téléphone après dérarrage de cette appli
cap = cv2.VideoCapture("http://10.16.207.99:8080/video") 

# Boucle à travers le cadre, entrant de 
# camera/video 
while True: 

	# lire le cadre de la caméra 
	_, frame = cap.read() 

	#Fonction d’appel de face_data pour trouver la largeur de la face (pixels) dans le cadre 
	face_width_in_frame = face_data(frame) 

	# vérifier si le visage est différent de zéro 
	if face_width_in_frame != 0: 
		
		# Trouver la distance en appelant la fonction Distance finder 
		# les arguments sont Focal_Length, Known_width(centimeters), Known_distance(centimeters) 
		Distance = Distance_finder( 
			Focal_length_found, Known_width, face_width_in_frame) 

		# Dessiner des lignes comme arrière-plan du texte
		cv2.line(frame, (30, 30), (230, 30), RED, 32) 
		cv2.line(frame, (30, 30), (230, 30), BLACK, 28) 

		# ecrire le texte dans l'écran 
		cv2.putText( 
			frame, f"Distance: {round(Distance,2)} CM", (30, 35), 
		fonts, 0.6, GREEN, 2)

		#Affichage dynamique dans la console
		print(Distance)

	# afficher le cadre dans l'écran 
	cv2.imshow("frame", frame)
	

	# quitter le programme avec la touche 'q' 
	if cv2.waitKey(1) == ord("q"): 
		break

# fermer la camera 
cap.release() 

# fermer les écrans qui étaient ouvert 
cv2.destroyAllWindows()
