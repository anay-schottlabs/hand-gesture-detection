import cv2
import mediapipe

# Set up camera
capture = cv2.VideoCapture(0)

# Set up hands
mediapipeHands = mediapipe.solutions.hands
mediapipeDraw = mediapipe.solutions.drawing_utils
hands = mediapipeHands.Hands()

while True:
    # Get the current frame of the camera feed
    success, image = capture.read()
    # Convert image to RGB
    imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

    # Draw landmarks on each hand in the image
    results = hands.process(imageRGB)
    if results.multi_hand_landmarks:
        for handLandmark in results.multi_hand_landmarks:
            mediapipeDraw.draw_landmarks(image, handLandmark, mediapipeHands.HAND_CONNECTIONS)

    # Display the image with the hands
    cv2.imshow("Image", image)
    cv2.waitKey(1)
