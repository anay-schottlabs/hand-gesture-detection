# Hand Gesture Detection
A basic project to detect hand gestures.

# Status of the project
The project is currently under development. The dependencies used by this project are listed in the requirements text file, along with the versions that are required. In the current stage of the project, only still hand signs can be detected, however, in the future, it will be updated to be able to detect full gestures.

# Using the training program
Within training.py is a variable, TRAINING_DATA_FILE_PATH, which you should set to the file path of the JSON file which will hold your data.
Your camera feed will show up in a window, which will allow you to position your hand sign.
Once you have prepared your hand sign, press enter to take a picture when prompted.
You will be prompted for a name, which will be used to label the picture that you have taken.
Once you have filled out the name, you will receive another prompt.
In the new prompt, press enter to continue and add the data, or enter anything else if you would like to cancel.
Once you complete that, the file at the TRAINING_DATA_FILE_PATH will be updated with the information.
Afterwards, the prompts will repeat and you may continue to add your training data.

# Using the detect gesture program
Make sure to set the same TRAINING_DATA_FILE_PATH variable to the same file path as the JSON file which holds your data.
Your camera feed will show up in a window, which will allow you to position your hand sign later on.
Show your open palm on the camera, and you will be told to prepare your hand gesture within a certain number of seconds.
Within that amount of time, prepare your hand sign in front of the camera, and a picture will be taken when the time is up.
The data will be classified based on the training data, and several messages may be shown, described below.

One possibility is "Your gesture was identified as '(YOUR GESTURE NAME)'", which means that the program was able to classify the hand sign. From here, you can evaluate if the classification is correct. If it is correct, press enter and the information will be restated. Then, you can press enter to proceed and add the new data, or type anything else to cancel instead. If the classification wasn't correct, then you may type in a new name to classify it. If you type in "none", all lowercase, it will add the hand sign as a special case where it will not be classified as a correct sign. If you type in any other name, you will again be asked if you would like to proceed. Press enter if so. Your final option would be to type in "NONE", all uppercase, which would result in cancelling adding the information entirely.

Another possiblity is "Your gesture did not match any other gesture.", which means that the hand sign was either similar to another sign that you classified as "none", or that the sign was higher than a certain threshold, meaning that it wasn't close to any matches.

The final possibility is "The camera failed to capture your gesture.", meaning that your hand wasn't detected properly. Usually, this is caused by your hand not being completely within the camera frame. Simply use the window displaying your camera feed to align your hands within the image, and take another picture.
