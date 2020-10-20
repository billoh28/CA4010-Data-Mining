import tensorflow as tf
from tensorflow.keras.applications.xception import Xception

# Load in necessary libraries
from tensorflow.keras.models import Model
from tensorflow.keras.models import Sequential, load_model
from tensorflow.keras.layers import Dense, Dropout, Activation, Flatten
from tensorflow.keras.layers import Conv2D, MaxPooling2D, BatchNormalization, GaussianNoise
from tensorflow.keras.regularizers import l2
from tensorflow.keras.utils import to_categorical
from tensorflow.keras.regularizers import l2
import os
import sys
import joblib
import numpy as np

""" Input shape is (250, 250, 3)  """

# Change working directory to dataset directory
path = os.path.join(os.getcwd(), "..", "..", "..", "Pickles")
os.chdir(path)

#Load in training files
pickle_in = open("X.pickle","rb")
X_train = joblib.load(pickle_in)
print("JOBLIB X done")


pickle_in = open("y.pickle","rb")
y_train = joblib.load(pickle_in)
print("JOBLIB y done")

#Load in testing files
pickle_in = open("X_test.pickle","rb")
X_test = joblib.load(pickle_in)
print("JOBLIB X done")


pickle_in = open("y_test.pickle","rb")
y_test = joblib.load(pickle_in)
print("JOBLIB y done")


# Building the model
model = Sequential()
base_model = Xception(weights='imagenet', include_top=False, input_shape=(250, 250, 3))
model.add(base_model)
model.add(MaxPooling2D(pool_size=(2, 2)))
model.add(Flatten())
model.add(Dense(128, kernel_regularizer=l2(0.0001)))
model.add(Dropout(0.45)) # was 0.4
model.add(Dense(3, activation='softmax'))

print("Compiling...")
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

# Print the summary of the model
model.summary()

print("Testing...")
model.fit(X_train, y_train, batch_size=16, epochs=10, verbose=1, validation_data=(X_test, y_test))#, callbacks=[tensorboard])

# Save in a folder outsied of git as it is way too big
save_location = os.path.join(path, "..", "Models")

# Make sure it exists
if not os.path.isdir(save_location):
    os.mkdir(save_location)

os.chdir(save_location)

model.save("model_1.h5")
del model

