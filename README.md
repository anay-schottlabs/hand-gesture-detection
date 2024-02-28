# Hand Gesture Detection
A basic project for custom hand gesture recognition.

# About the project
As of February 27, 2024, this project has been completed. The dependencies used by this project are listed in the requirements text file, along with the versions that are required. The program has the ability to take pictures of the user's hand and recognize the gestures from a list of gestures trained by the user.

# Using the program
Make sure to set the same TRAINING_DATA_FILE_PATH variable to the same file path as the JSON file which holds your data.

Upon running the program, a window will open which displays your camera feed. If you move your hands into your camera's view, you will notice that one of your hands will be tracked, and the window will display the connections between the landmarks of that hand. You will receive a prompt in the terminal asking you to press enter to record a gesture, so prepare your hand gesture using the camera feed and press enter in the terminal once you are ready. You will be prompted to enter a name for the gesture. If you would like to add this gesture to your training data, specify a name for it and press enter. This should result in a message stating that the data was successfully added. However, if you have already added training data, you may simply press enter, and the program will attempt to identify the gesture, resulting in a message with the name of the closest match and the message that displays if any errors occurred.

This loop will continually repeat, however, you can press escape while the window is open to close it, which should exit the program. If the window closes, but the program is still active in the terminal, press Ctrl+C on the keyboard to exit the program.
