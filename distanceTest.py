#import packages
#using the triangle similarity
#reference https://www.pyimagesearch.com/2015/01/19/find-distance-camera-objectmarker-using-python-opencv/


# # install opencv "pip install opencv-python"
# import cv2

# # distance from camera to object(face) measured
# # centimeter
# Known_distance = 10

# # width of face in the real world or Object Plane
# # centimeter
# Known_width = 5

# # Colors
# GREEN = (0, 255, 0)
# RED = (0, 0, 255)
# WHITE = (255, 255, 255)
# BLACK = (0, 0, 0)

# # defining the fonts
# fonts = cv2.FONT_HERSHEY_COMPLEX

# # face detector object
# face_detector = cv2.CascadeClassifier("haarcascade_frontalface_default.xml")

# # focal length finder function
# def Focal_Length_Finder(measured_distance, real_width, width_in_rf_image):

# 	# finding the focal length
# 	focal_length = (width_in_rf_image * measured_distance) / real_width
# 	return focal_length

# # distance estimation function
# def Distance_finder(Focal_Length, real_face_width, face_width_in_frame):

# 	distance = (real_face_width * Focal_Length)/face_width_in_frame

# 	# return the distance
# 	return distance


# def face_data(image):

# 	face_width = 0 # making face width to zero

# 	# converting color image ot gray scale image
# 	gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 	# detecting face in the image
# 	faces = face_detector.detectMultiScale(gray_image, 1.3, 5)

# 	# looping through the faces detect in the image
# 	# getting coordinates x, y , width and height
# 	for (x, y, h, w) in faces:

# 		# draw the rectangle on the face
# 		cv2.rectangle(image, (x, y), (x+w, y+h), GREEN, 2)

# 		# getting face width in the pixels
# 		face_width = w

# 	# return the face width in pixel
# 	return face_width


# # reading reference_image from directory
# ref_image = cv2.imread("2ft.png")

# # find the face width(pixels) in the reference_image
# ref_image_face_width = face_data(ref_image)

# # get the focal by calling "Focal_Length_Finder"
# # face width in reference(pixels),
# # Known_distance(centimeters),
# # known_width(centimeters)
# Focal_length_found = Focal_Length_Finder(
# 	Known_distance, Known_width, ref_image_face_width)

# print(Focal_length_found)

# # show the reference image
# cv2.imshow("ref_image", ref_image)



# # initialize the camera object so that we
# # can get frame from it
# cap = cv2.VideoCapture(0)

# # looping through frame, incoming from
# # camera/video
# while True:

# 	# reading the frame from camera
# 	_, frame = cap.read()

# 	# calling face_data function to find
# 	# the width of face(pixels) in the frame
# 	face_width_in_frame = face_data(frame)

# 	# check if the face is zero then not
# 	# find the distance
# 	if face_width_in_frame != 0:
	
# 		# finding the distance by calling function
# 		# Distance distance finder function need
# 		# these arguments the Focal_Length,
# 		# Known_width(centimeters),
# 		# and Known_distance(centimeters)
# 		Distance = Distance_finder(
# 			Focal_length_found, Known_width, face_width_in_frame)

# 		# draw line as background of text
# 		cv2.line(frame, (30, 30), (230, 30), RED, 32)
# 		cv2.line(frame, (30, 30), (230, 30), BLACK, 28)

# 		# Drawing Text on the screen
# 		cv2.putText(
# 			frame, f"Distance: {round(Distance,2)} CM", (30, 35),
# 		fonts, 0.6, GREEN, 2)

# 	# show the frame on the screen
# 	cv2.imshow("frame", frame)

# 	# quit the program if you press 'q' on keyboard
# 	if cv2.waitKey(1) == ord("q"):
# 		break

# # closing the camera
# cap.release()

# # closing the the windows that are opened
# cv2.destroyAllWindows()














































# from imutils import paths
# import numpy as np
# import imutils
# import cv2



# def distance_to_camera(knownWidth, focalLength, perWidth):
#     #return the distance from the marker to the camera
#     return (knownWidth*focalLength)/perWidth

# # Define webcam used
# webcam = cv2.VideoCapture(0, cv2.CAP_DSHOW)


# while(True):
#     # Grabbing frame from webcam
#     _, frame = webcam.read()

#     # Apply Grayscale
#     grayscale = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

#     # Apply Gaussian Blur
#     blur = cv2.GaussianBlur(grayscale, (9,9), 0)

#     # Create Mask/Threshold
#     threshold = cv2.adaptiveThreshold(blur, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 23, 3)

#     # Find contours
#     contours = cv2.findContours(threshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
#     contours = imutils.grab_contours(contours)
    
#     # Loop for all contours
#     contnum = 0
#     objectID = 0
#     for c in contours:
#         area = cv2.contourArea(c)
#         # Only display contour for those having an area threshold of > 1000
#         if area > 2500:
#             contnum += 1
#             M = cv2.moments(c)
#             try:
#                 cX = int(M["m10"] / M["m00"])
#                 cY = int(M["m01"] / M["m00"])
#             except:
#                 print("Contour not found!")

#             cv2.drawContours(frame, [c], -1, (0, 255, 0), 2)
#             cv2.circle(frame, (cX, cY), 7, (0,0,0), -1)
#             cv2.putText(frame, "ID: " + str(objectID), (cX - 23, cY - 20), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,0), 2)
#             cv2.putText(frame, "Location: ({}, {})".format(cX, cY), (450, 450), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255,255,255), 2)

#             objectID += 1

#     cv2.imshow("test",threshold)
#     cv2.imshow("test2",frame)

#     if cv2.waitKey(1) & 0xFF == ord('q'):
#         break


# # Safely close all windows
# webcam.release()
# cv2.destroyAllWindows()    

