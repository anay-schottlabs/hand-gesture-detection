import cv2
import mediapipe

class handDetector():
    def __init__(self):
        self.mediapipeHands = mediapipe.solutions.hands
        self.mediapipeDraw = mediapipe.solutions.drawing_utils
        self.hands = self.mediapipeHands.Hands()

    def getHandLandmarksFromImage(self, image):
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return self.hands.process(imageRGB).multi_hand_landmarks
    
    def detectHands(self, image):
        handLandmarks = self.getHandLandmarksFromImage(image)
        if handLandmarks:
            for handLandmark in handLandmarks:
                self.mediapipeDraw.draw_landmarks(image, handLandmark, self.mediapipeHands.HAND_CONNECTIONS)
        return image
    
    def findHandLandmarkPositions(self, image, handIndex):
        landmarks = []
        chosenHand = self.getHandLandmarksFromImage(image)
        if chosenHand:
            chosenHand = chosenHand[handIndex]
            for index, landmark in enumerate(chosenHand.landmark):
                width = image.shape[1]
                height = image.shape[0]
                xPos = int(landmark.x * width)
                yPos = int(landmark.y * height)
                landmarks.append((index, xPos, yPos))
        return landmarks


# Set up camera
capture = cv2.VideoCapture(0)

while True:
    handFinder = handDetector()
    image = capture.read()[1]
    print(handFinder.findHandLandmarkPositions(image, 0))
    cv2.imshow("Image", handFinder.detectHands(image))
    cv2.waitKey(1)
