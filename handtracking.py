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
        # Convert the image to RGB format so that the hands can be processed
        imageRGB = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        return self.hands.process(imageRGB).multi_hand_landmarks                                                                                                                                                      

    # If there are hands in an image, draw the landmarks on the image
    def drawHandsOnImage(self, image):
        handLandmarks = self.getHandLandmarksFromImage(image)
        if handLandmarks:
            for handLandmark in handLandmarks:
                # Draw the identified hand on the image
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
        chosenHandPositions = self.getHandLandmarkPositions(image, handIndex)
        if chosenHandPositions:
            # Get the height and width
            height, width, _ = image.shape
            # Get the center positions
            centerX = width / 2
            centerY = height / 2
            # Determine the change to reach the center positions
            xModifierToCenter = centerX - chosenHandPositions[landmarkToCenter]["x"]
            yModifierToCenter = centerY - chosenHandPositions[landmarkToCenter]["y"]
            # Apply the change to each hand landmark position
            for landmark in chosenHandPositions:
                landmark["x"] += xModifierToCenter
                landmark["y"] += yModifierToCenter
        return chosenHandPositions
    
    # Get the relative positions of the landmarks of a hand in a given image
    def getRelativeHandPositions(self, image, handIndex, landmarkToCenter):
        chosenHandPositions = self.getHandLandmarkPositions(image, handIndex)
        if chosenHandPositions:
            # Determine the chosen landmark
            chosenLandmark = chosenHandPositions[landmarkToCenter]
            # Find the change to convert the positions to relative positions
            xToRelative = chosenLandmark["x"]
            yToRelative = chosenLandmark["y"]
            # Apply the change to each hand landmark position
            for landmark in chosenHandPositions:
                landmark["x"] -= xToRelative
                landmark["y"] -= yToRelative
        return chosenHandPositions

    # Get the positions of landmarks in an image
    def getHandLandmarkPositions(self, image, handIndex):
        landmarks = []
        chosenHand = self.getHandLandmarksFromImage(image)
        if chosenHand:
            chosenHand = chosenHand[handIndex]
            for index, landmark in enumerate(chosenHand.landmark):
                # Get the height and width of the image
                height, width, _ = image.shape;
                # Convert the landmark positions to pixel values
                xPos = int(landmark.x * width)
                yPos = int(landmark.y * height)
                # Add the pixel landmark positions to an array and add the index of the landmark
                landmarks.append({
                    "index": index,
                    "x": xPos,
                    "y": yPos,
                })
        return landmarks
