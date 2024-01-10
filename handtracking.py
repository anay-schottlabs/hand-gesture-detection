import cv2
import mediapipe

# A class to detect, track, and mark hands in images
class HandDetector:
    def __init__(self, maxHands, detectionConfidence, trackingConfidence):
        self.mediapipeHands = mediapipe.solutions.hands
        self.mediapipeDraw = mediapipe.solutions.drawing_utils
        self.hands = self.mediapipeHands.Hands(max_num_hands = maxHands, min_detection_confidence=detectionConfidence, min_tracking_confidence=trackingConfidence)

    # Get the landmarks of hands in an image
    def getHandLandmarksFromImage(self, image):
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return self.hands.process(imageRGB).multi_hand_landmarks                                                                                                                                                      

    def detectHands(self, image):
        handLandmarks = self.getHandLandmarksFromImage(image)
        if handLandmarks:
            for handLandmark in handLandmarks:
                self.mediapipeDraw.draw_landmarks(image, handLandmark, self.mediapipeHands.HAND_CONNECTIONS)
        return image
    
    def getHandCountInImage(self, image):
        hands = self.getHandLandmarksFromImage(image)
        if (hands):
            return len(hands)
        return 0

    def getHandLandmarkPositions(self, image, handIndex):
        landmarks = []
        chosenHand = self.getHandLandmarksFromImage(image)
        if chosenHand:
            chosenHand = chosenHand[handIndex]
            for _, landmark in enumerate(chosenHand.landmark):
                height, width = image.shape;
                xPos = int(landmark.x * width)
                yPos = int(landmark.y * height)
                landmarks.append({
                    "x": xPos,
                    "y": yPos,
                })
        return landmarks
