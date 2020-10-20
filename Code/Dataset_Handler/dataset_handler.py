# Dataset Handler
# Used to prepare the dataset for the model, split the dataset into seperate testing and training datasets and serialise the datasets

import numpy as np
import os
import cv2
from tqdm import tqdm # shows a progress bar for an iteration while it's executing
import random
from tensorflow.keras.utils import to_categorical
import sys


class DataHandler:
    def __init__(self, data_path):

        # Path to parent file of data
        self.data_path = data_path

        # Subdirectories in parent file
        self.DIRECTORIES = [["bee1", "bee2"], ["wasp1", "wasp2"], ["other_insect"], ["other_noinsect"]]

        # Labels
        self.INT_LABELS = [0, 1, 2]

        # Where training data will be saved to
        self.training_set = []

        # Where testing data will be saved to
        self.testing_set = []

        # One hot encoded labels
        self.categorical_labels = to_categorical(self.INT_LABELS, num_classes=None)

    def create_data(self):
        for i in range(len(self.DIRECTORIES) - 1): # Not including other_noinsect
            print(self.DIRECTORIES[i])

            for j in range(len(self.DIRECTORIES[i])):

                # Extract label and sub directory
                sub_direct = self.DIRECTORIES[i][j]
                label = self.categorical_labels[i]
                path = os.path.join(self.data_path, sub_direct)

                # Remeber to reserve 20 percent for testing / validation
                counter = 1
                num_train = int(len(os.listdir(path)) * 0.8)
 
                for img in tqdm(os.listdir(path)):
                    # Add to training set
                    img_array = cv2.imread(os.path.join(path,img))

                    img_array = cv2.resize(img_array, (250, 250))

                    if counter < num_train:
                        self.training_set.append([img_array, label])

                    else:
                        self.testing_set.append([img_array, label])

                    counter += 1

    def get_training_set(self):
        return self.training_set[:]

    def get_testing_set(self):
        return self.testing_set[:]


def main():
    # Change working directory to dataset directory
    path = os.path.join(os.getcwd(), "..", "..", "Dataset")
    os.chdir(path)

    # Initialise data handler
    data_handler = DataHandler(path)

    # Create Data
    data_handler.create_data()

    # Extract data
    training_set = data_handler.get_training_set()

    testing_set = data_handler.get_testing_set()

    # Shuffle training data
    random.shuffle(training_set)

    X = []
    y = []

    # Extract labels and features from training data set
    for features, label in training_set:
        X.append(features)
        y.append(label)

    print(X[100].shape)

    # Changes X to a numpy array
    # X will have the shape (?, 250, 250, 1), where ? is the number of images in the np array, (150, 150) is the image dimensions and 1 shows that these are greyscale images ( not rgb )
    X = np.array(X).reshape(-1, 250, 250, 3)
    y = np.array(y)

    # Repeat for testing data
    X_test = []
    y_test = []

    for features, label in testing_set:
        X_test.append(features)
        y_test.append(label)

    X_test = np.array(X_test).reshape(-1, 250, 250, 3)
    y_test = np.array(y_test)


    import joblib

    # Save these serialised files outside the git folders as it is too large to have within the git
    save_location = os.path.join(path, "..", "..", "Pickles")

    # Make sure it exists
    if not os.path.isdir(save_location):
        os.mkdir(save_location)

    os.chdir(save_location)

    # Create serialised training datasets
    pickle_out = open("X.pickle","wb")
    joblib.dump(X, pickle_out)
    pickle_out.close()

    pickle_out = open("y.pickle","wb")
    joblib.dump(y, pickle_out)
    pickle_out.close()

    # Create serialised testing datasets
    pickle_out = open("X_test.pickle","wb")
    joblib.dump(X_test, pickle_out)
    pickle_out.close()

    pickle_out = open("y_test.pickle","wb")
    joblib.dump(y_test, pickle_out)
    pickle_out.close()


if __name__ == '__main__':
    main()
