import cv2
import mediapipe
import json
import fastdtw
import threading

# A class to recognize gestures
class GestureRecognizer:
    def __init__(self, detection_confidence, tracking_confidence):
        # Define the mediapipe utilities for hands and drawing utilities
        self.mediapipe_hands = mediapipe.solutions.hands
        self.mediapipe_draw = mediapipe.solutions.drawing_utils
        # Define a single mediapipe hand and provide the detection and tracking confidence specified
        self.hands = self.mediapipe_hands.Hands(max_num_hands=1, min_detection_confidence=detection_confidence, min_tracking_confidence=tracking_confidence)
    
    # Process the hands in an image
    def process_hands_from_image(self, image):
        # Convert the image to RGB format so that the hands can be processed
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # Process the hands and get the landmarks
        processed_hands = self.hands.process(image_rgb).multi_hand_landmarks
        return processed_hands
    
    def get_hand_landmarks_from_image(self, image):
        # Process the hands from the image
        processed_hands = self.process_hands_from_image(image)
        # A list of the hand landmarks
        hand_landmarks = []
        # Check if any hands were actually in the image
        if processed_hands:
            # Get the landmarks of the first processed hand
            processed_hand = processed_hands[0]
            # The values to center the x and y coordinates
            x_to_center = None
            y_to_center = None
            # Loop through each landmark in the hand
            for index, landmark in enumerate(processed_hand.landmark):
                # Get the height and width of the image
                height, width, _ = image.shape
                # Get the center points of the image
                center_x = width / 2
                center_y = height / 2
                # Convert the floating point landmark positions into pixel values
                x_pos = int(landmark.x * width)
                y_pos = int(landmark.y * height)
                # Check if this is the first landmark of the hand
                if index == 0:
                    # Determine the values needed to center the x and y positions of the landmark
                    x_to_center = center_x - x_pos
                    y_to_center = center_y - y_pos
                # Apply the centering values to the x and y positions of each landmark
                x_pos += x_to_center
                y_pos += y_to_center
                # Add the pixel landmark positions to the list of landmarks
                hand_landmarks.append([x_pos, y_pos])
        return hand_landmarks
    
    # Draw the landmarks and hand connections on an image
    def draw_hands_on_image(self, image):
        # Process the hands from the image
        processed_hands = self.process_hands_from_image(image)
        # Check if any hands were actually in the image
        if processed_hands:
            # Get the landmarks of the first processed hand
            processed_hand = processed_hands[0]
            # Draw the landmarks on the hand
            self.mediapipe_draw.draw_landmarks(image, processed_hand, self.mediapipe_hands.HAND_CONNECTIONS)
        return image
    
    # Take an image and save it to a JSON file
    def save_image_as_training_data(self, image, gesture_name, training_file_name):
        # Extract hand landmarks from the provided image
        hand_landmarks = self.get_hand_landmarks_from_image(image)
        # Check if any hands were actually in the image
        if len(hand_landmarks) > 0:
            # Open the training file and add the data to it
            with open(training_file_name, "r+") as training_data_file:
                # Read the existing training data
                training_data = json.load(training_data_file)
                # Clear the original training data now that it has been read
                training_data_file.seek(0)
                training_data_file.write("")
                # Add the new data
                training_data.append({
                    "name": gesture_name,
                    "landmarks": hand_landmarks
                })
                # Write the changes to the training data to the file
                json.dump(training_data, training_data_file, indent=4)
    
    # Take an image and identify which gesture it is
    def recognize_gesture_in_image(self, image, training_file_name, min_match_threshold):
        # Extract hand landmarks from the provided image
        hand_landmarks = self.get_hand_landmarks_from_image(image)
        # Check if any hands were actually in the image
        if len(hand_landmarks) > 0:
            # Open the training file and read the data
            with open(training_file_name, "r") as training_data_file:
                # Read the existing training data
                training_data = json.load(training_data_file)
                # A list to store the cost to align each training gesture to the current one
                gesture_costs = []
                # Loop over each gesture saved in the training data
                for gesture in training_data:
                    # Use dynamic time warping to find the cost to align a gesture's landmarks to the current gesture's landmarks
                    cost, _ = fastdtw.fastdtw(hand_landmarks, gesture["landmarks"])
                    # Add the cost and name of the gesture
                    gesture_costs.append({
                        "name": gesture["name"],
                        "cost": cost
                    })
                # The gesture from the training data that is the most similar to the current gesture
                try:
                    most_similar_gesture = gesture_costs[0]
                    # Loop over the cost of each gesture
                    for gesture_cost in gesture_costs:
                        # If the new cost is less than the least cost, it becomes the least cost
                        if gesture_cost["cost"] < most_similar_gesture["cost"]:
                            most_similar_gesture = gesture_cost
                    # If the most similar gesture meets the minimum match threshold provided, return its name
                    if most_similar_gesture["cost"] <= min_match_threshold:
                        return most_similar_gesture["name"], "A match was found."
                except:
                    return "None", "No training data was provided."
        # If there was either no hand in the image or the most similar gesture didn't meet the threshold, return nothing
        return "None", "No hands were present in the image."

# The path of the file that contains the training data
TRAINING_DATA_FILE_PATH = "data.json"
# The delay of each camera loop in milliseconds
LOOP_DELAY = 2
# The dimensions of the camera
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720
# The minimum confidence required to detect and track hands
DETECTION_CONFIDENCE = 0.7
TRACKING_CONFIDENCE = 0.7
# The minimum threshold for a match for a gesture
MIN_MATCH_THRESHOLD = 1000000

# An event for when an image is captured
image_captured_event = threading.Event()
# An event for when the program should exit
exit_program_event = threading.Event()
# A lock to make sure the image is set safely
set_image_lock = threading.Lock()

# Create a new video capture
capture = cv2.VideoCapture(0)
# Create a gesture recognizer with the detection and tracking confidence
gesture_recognizer = GestureRecognizer(DETECTION_CONFIDENCE, TRACKING_CONFIDENCE)

# Show the camera feed and capture images
def show_camera_feed():
    while True:
        # Use the lock for safety
        with set_image_lock:
            # Make sure that other methods can access the captured image
            global captured_image
            # Capture the image from the camera feed
            _, captured_image = capture.read()
            # Resize the image
            captured_image = cv2.resize(captured_image, (CAMERA_WIDTH, CAMERA_HEIGHT))
            # Draw hands on the image
            captured_image = gesture_recognizer.draw_hands_on_image(captured_image)
            # Display the image in a window
            cv2.imshow("Hand Gesture Recognition", captured_image)
            # Set the event
            image_captured_event.set()
        # Wait for the delay
        key = cv2.waitKey(LOOP_DELAY)
        # Exit the program if the escape key was pressed
        if key == 27:
            exit_program_event.set()
            break
    # Close the window
    cv2.destroyAllWindows()

# Take user input to save gestures as training data and recognize gestures
def handle_user_input():
    # Run this until the program needs to exit
    while not exit_program_event.is_set():
        # Wait for the image to be set
        image_captured_event.wait()
        image_captured_event.clear()
        # Wait for the user to press enter to record the gesture
        input("Press enter to record a gesture: ")
        with set_image_lock:
            # Ask for a gesture name
            gesture_name = input("Enter a name for the gesture to register it, or press enter to identify it: ")
            # If no name was provided, identify the gesture
            if gesture_name == "":
                match, message = gesture_recognizer.recognize_gesture_in_image(captured_image, TRAINING_DATA_FILE_PATH, MIN_MATCH_THRESHOLD)
                print(f"Match: {match}")
                print(f"Message: {message}")
            # If a name was provided, save the gesture to the training file
            else:
                gesture_recognizer.save_image_as_training_data(captured_image, gesture_name, TRAINING_DATA_FILE_PATH)
                print("The data was successfully registered.")

# Set threads
show_camera_feed_thread = threading.Thread(target=show_camera_feed)
handle_user_input_thread = threading.Thread(target=handle_user_input)

# Start the threads
show_camera_feed_thread.start()
handle_user_input_thread.start()

# Join the threads to the main thread
show_camera_feed_thread.join()
handle_user_input_thread.join()
