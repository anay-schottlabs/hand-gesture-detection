import cv2
import handtracking

cameraWidth = 1080
cameraHeight = 720
loopDelay = 2

capture = cv2.VideoCapture(0)
capture.set(3, cameraWidth)
capture.set(1, cameraHeight)

while True:
    handFinder = handtracking.handDetector(4, 0.7, 0.5)
    image = capture.read()[1]
    hands = handFinder.getHandLandmarksFromImage(image)

    fistClenchDistanceThreshold = 20
    indexClenched = False
    middleClenched = False
    ringClenched = False
    pinkyClenched = False
    thumbClenched = False
    rightHand = False
    if (hands != None):
        for i in range(len(hands)):
            hand = handFinder.findHandLandmarkPositions(image, i)
            try:
                if (hand[8]["y"] > hand[7]["y"] > hand[6]["y"]):
                    indexClenched = True
                if (hand[12]["y"] > hand[11]["y"] > hand[10]["y"]):
                    middleClenched = True
                if (hand[16]["y"] > hand[15]["y"] > hand[14]["y"]):
                    ringClenched = True
                if (hand[20]["y"] > hand[19]["y"] > hand[18]["y"]):
                    pinkyClenched = True
                if (hand[20]["x"] < hand[4]["x"]):
                    rightHand = True
                if (hand[3]["y"] < hand[2]["y"] and ((not rightHand and (hand[4]["x"] > hand[3]["x"])) or (rightHand and (hand[4]["x"] < hand[3]["x"])))):
                    thumbClenched = True
                if (indexClenched and middleClenched and ringClenched and pinkyClenched and thumbClenched):
                    cv2.circle(image, (hand[11]["x"], hand[11]["y"]), 100, (0, 0, 255))
            except:
                break

    cv2.imshow("Image", handFinder.detectHands(image))
    cv2.waitKey(loopDelay)
