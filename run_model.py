# Program which calls and runs the trained CNN model

import sys
import os
import numpy as np
from tensorflow.keras.models import load_model
import matplotlib.pyplot as plt
import cv2

def main():
    # Current working directory
    DATA_DIR = os.getcwd()

    # Get images located in Images Test_Images folder
    IMAGES_LOCATION = os.path.join(DATA_DIR, "Test_Images")

    # Labels
    LABELS = ["bee", "wasp", "neither"]

    # Outside Git repo
    model = load_model(os.path.join(DATA_DIR, "..", "Models", "model_1.h5"))

    # Possible output of the model
    output = []

    # Expected output
    names = []

    # Feed images to the models
    for image in os.listdir(IMAGES_LOCATION):

        img_array = cv2.imread(os.path.join(IMAGES_LOCATION, image))  # convert to array
        img_array = cv2.resize(img_array, (250, 250))

        imgplot = plt.imshow(img_array)
        plt.show()

        img_array = np.array(img_array).reshape(-1, 250, 250, 3)

        prediction = model.predict(img_array, verbose=0)
        print(prediction)

        output.append(LABELS[prediction.argmax()])
        names.append(image.split(".")[0])

    print("Output from the models : {}".format(" ".join(output)))
    print("Expected Output: {}".format(" ".join(names)))


if __name__ == '__main__':
    main()