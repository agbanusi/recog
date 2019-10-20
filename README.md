# recog
The facial_recognition.py takes in a directory with pictures and also captures a face using the camera of tje device and then runs a check with the pictures stored in the file and tell if any is a match with the one which is the match.
Dependencies are: cv2,pickle, keras_VGGFace, PIL, numpy and Scipy.

For the rest.py, it is an flask api that lets u put in a file for adding to the stored images, or run a check on a person and outputs the results simply, no html or css was used.
Dependencies are: flask, flask_restful and flask_cors and the facial_recognition stated above
