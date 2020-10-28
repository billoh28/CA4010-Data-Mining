from sklearn.neighbors import KNeighborsClassifier
from sklearn.model_selection import train_test_split
import numpy as np
from imutils import paths
import cv2
import os

def main():
    imagePath = list(paths.list_images(os.path.join(os.getcwd(), "..", "..", "Dataset")))
    rawImages = []
    labels = []

    for (i, imagePath) in enumerate(imagePath):

        image = cv2.imread(imagePath)
        labels.append(imagePath.split(os.path.sep)[-1].split(".")[0])
        pixels = cv2.resize(image, (100, 100)).flatten()
        rawImages.append(pixels)

    (trainRI, testRI, trainRL, testRL) = train_test_split(rawImages, labels, test_size=0.25, random_state=42)

    model = KNeighborsClassifier(n_neighbors=1, n_jobs=-1)
    print("before")
    model.fit(trainRI, trainRL)
    print("after")

    acc = model.score(testRI, testRL)
    print("[INFO] raw pixel accuracy: {:.2f}%".format(acc * 100))
  
if __name__ == "__main__":
    main()