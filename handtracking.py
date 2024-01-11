import cv2
import mediapipe

# A class to detect, track, and mark hands in images
class HandDetector:
    def __init__(self, maxHands, detectionConfidence, trackingConfidence):
        self.mediapipeHands = mediapipe.solutions.hands
        self.mediapipeDraw = mediapipe.solutions.drawing_utils
        self.hands = self.mediapipeHands.Hands(max_num_hands = maxHands, min_detection_confidence=detectionConfidence, min_tracking_confidence=trackingConfidence)

    # Get the data for the landmarks of hands in an image
    def getHandLandmarksFromImage(self, image):
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return self.hands.process(imageRGB).multi_hand_landmarks                                                                                                                                                      

    # If there are hands in an image, draw the landmarks on the image
    def drawHandsOnImage(self, image):
        handLandmarks = self.getHandLandmarksFromImage(image)
        if handLandmarks:
            for handLandmark in handLandmarks:
                self.mediapipeDraw.draw_landmarks(image, handLandmark, self.mediapipeHands.HAND_CONNECTIONS)
        return image

    # Check how many hands are in an image
    def getHandCountInImage(self, image):
        hands = self.getHandLandmarksFromImage(image)
        if (hands):
            return len(hands)
        return 0

    # Center a specific hand in an image and return the new landmark positions
    def centerHandPositions(self, image, handIndex, landmarkToCenter):
        chosenHandPositions = self.getHandLandmarksFromImage(image, handIndex)
        height, width = image.shape
        centerX = width / 2
        centerY = height / 2
        xModifierToCenter = centerX - chosenHandPositions[landmarkToCenter].x
        yModifierToCenter = centerY - chosenHandPositions[landmarkToCenter].y
        if chosenHandPositions:
            for landmark in chosenHandPositions:
                landmark.x += xModifierToCenter
                landmark.y += yModifierToCenter
        return chosenHandPositions

    # Get the positions of landmarks in an image
    def getHandLandmarkPositions(self, image, handIndex):
        landmarks = []
        chosenHand = self.getHandLandmarksFromImage(image)
        if chosenHand:
            chosenHand = chosenHand[handIndex]
            for index, landmark in enumerate(chosenHand.landmark):
                height, width = image.shape;
                xPos = int(landmark.x * width)
                yPos = int(landmark.y * height)
                landmarks.append({
                    "index": index,
                    "x": xPos,
                    "y": yPos,
                })
        return landmarks
