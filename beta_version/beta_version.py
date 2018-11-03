# -*- coding: utf-8 -*-
"""beta-version.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1e6nC7zLRMDvodTroGS5Mdn7ns3l5ywTa
"""

# !pip install -U -q PyDrive

# from pydrive.auth import GoogleAuth
# from pydrive.drive import GoogleDrive
# from google.colab import auth
# from oauth2client.client import GoogleCredentials

# # 1. Authenticate and create the PyDrive client.
# auth.authenticate_user()
# gauth = GoogleAuth()
# gauth.credentials = GoogleCredentials.get_application_default()
# drive = GoogleDrive(gauth)

from keras.models import Sequential
from keras.layers import UpSampling2D, InputLayer
from keras.layers import Conv2D
from keras.optimizers import RMSprop
from keras.utils import np_utils
from keras.preprocessing.image import ImageDataGenerator
from keras import optimizers
import keras
import numpy as np
import matplotlib.pyplot as plt
from keras.models import Model, load_model
from keras.models import model_from_json
from skimage.color import rgb2lab,lab2rgb
import matplotlib.pyplot as plt
import cv2

# downloaded = drive.CreateFile({'id':'train_file_id'})
# downloaded.GetContentFile('X_small.npy')

# downloaded = drive.CreateFile({'id':'test_image_id'})
# downloaded.GetContentFile('1.jpg')

# downloaded = drive.CreateFile({'id':'test_image_id'})
# downloaded.GetContentFile('2.jpg')

train = np.load('X_small.npy')

model = Sequential()
model.add(InputLayer(input_shape=(256, 256, 1)))
model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(64, (3, 3), activation='relu', padding='same', strides=2))
model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(128, (3, 3), activation='relu', padding='same', strides=2))
model.add(Conv2D(256, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(256, (3, 3), activation='relu', padding='same', strides=2))
model.add(Conv2D(512, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(256, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(128, (3, 3), activation='relu', padding='same'))
model.add(UpSampling2D((2, 2)))
model.add(Conv2D(64, (3, 3), activation='relu', padding='same'))
model.add(UpSampling2D((2, 2)))
model.add(Conv2D(32, (3, 3), activation='relu', padding='same'))
model.add(Conv2D(2, (3, 3), activation='tanh', padding='same'))
model.add(UpSampling2D((2, 2)))

model.compile(optimizer='rmsprop', loss='mse',metrics=['accuracy'])

datagen = ImageDataGenerator(
        shear_range=0.2,
        zoom_range=0.2,
        rotation_range=20,
        horizontal_flip=True)

batch_size = 50
def image_a_b_gen(batch_size):
    for batch in datagen.flow(train, batch_size=batch_size):
        lab_batch = rgb2lab(batch)
        X_batch = lab_batch[:,:,:,0]
        Y_batch = lab_batch[:,:,:,1:] / 128        
        yield (X_batch.reshape(X_batch.shape+(1,)), Y_batch)

model.fit_generator(image_a_b_gen(batch_size),steps_per_epoch=20, epochs=4)

pred = model.predict(rgb2lab(train[20])[:,:,0].reshape((1,256,256,1)),steps=1)

pred = pred * 128

cur = np.zeros((256, 256, 3))
cur[:,:,0] = rgb2lab(train[20])[:,:,0].reshape((256,256))
cur[:,:,1:] = pred.reshape((256,256,2)) * 128

cur = lab2rgb(cur)

# imsave('my_image.png',color.lab2rgb(canvas))

# file = drive.CreateFile({'parents':[{u'id': 'folder_id'}]})
# file.SetContentFile('my_image.png')
# file.Upload()