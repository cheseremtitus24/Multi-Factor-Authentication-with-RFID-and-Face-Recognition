import os
import pickle

import numpy as np
from PIL import Image
import cv2

# Gets the current working directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

face_cascade = cv2.CascadeClassifier('data/haarcascade_frontalface_alt2.xml')

recognizer = cv2.face.LBPHFaceRecognizer_create()


# looks for a directory name(images) in the current directory

image_dir = os.path.join(BASE_DIR, "images")

print("image directory is " + str(image_dir))

current_id = 0
label_ids = {}
y_labels = []
x_train = []

# recursively searches for images in the images directory
for root, dirs, files in os.walk(image_dir):
    for file in files:
        if file.endswith("png") or file.endswith("jpg"):
            path = os.path.join(root, file)
            print(file+ "check this")
            label = os.path.basename(os.path.dirname(path)).replace(" ", "-").lower()  # replaces a space with a dash
            print("the Subdirectory after 'images'  is the label and is "+ label)
            print("The full path is " + path)  ### full path to the current file

            if label in label_ids:
                pass
            else:
                label_ids[label] = current_id
                current_id += 1

            id_ = label_ids[label]
            # print(label_ids)

            # y_labels.append(label)
            # x_train.append(path)  #verify and turn into a numpy array
            pil_image = Image.open(path).convert("L")  # grayscale
            # size = (960, 960)
            size = (550, 550)  # resize image then convert to numpy array

            final_image = pil_image.resize(size, Image.ANTIALIAS)

            # scale correctly without distortion

            image_array = np.array(final_image, "uint8")
            # print(image_array)  # convert image to pixel values matrix

            # Finding the Region of interest

            faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5)
            for (x, y, w, h) in faces:
                roi = image_array[y:y + h, x:x + w]
                x_train.append(roi)
                y_labels.append(id_)
# print(y_labels)
# print(x_train)

with open("Resources/labels.pickle", 'wb') as f:
    pickle.dump(label_ids, f)
    # wb write in bytes as files

################################TRain the Recognizer ###################333333333
recognizer.train(x_train, np.array(y_labels))
recognizer.save("Resources/trainer.yml")
