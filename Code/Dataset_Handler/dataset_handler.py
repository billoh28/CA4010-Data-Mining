# Dataset Handler
# Used to prepare the dataset for the model, split the dataset into seperate testing and training datasets and serialise the datasets

import numpy as np
import os
import cv2
from tqdm import tqdm # shows a progress bar for an iteration while it's executing
import random
from tensorflow.keras.utils import to_categorical
import sys
import pandas as pd


class DataHandler:
    def __init__(self):
        pass

def main():
    # Change working directory to dataset directory
    path = os.path.join(os.getcwd(), "..", "..", "Dataset")
    print(path)
    os.chdir(path)

    # Import labels csv
    labels = pd.read_csv("labels.csv")
    labels.head()

    # data_handler = DataHandler

if __name__ == '__main__':
    main()
