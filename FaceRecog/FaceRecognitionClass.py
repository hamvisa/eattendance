# coding: utf-8

# # <u>Face Recognition System
# This is based on Siamsese network.
# The advantage of **Siamese Network** is that it allows a way to do this sort of verification task with very little user data, as it is quite unreasonable to train using thousands of images for each user. Here we will be using **FaceNet Model**.
# FaceNet learns a neural network that encodes a face image into a vector of 128 numbers. So by comparing two such vectors, we can then determine if two pictures are of the same person.

from keras.models import Sequential
from keras.layers import Conv2D, ZeroPadding2D, Activation, Input, concatenate
from keras.models import Model
from keras.layers.normalization import BatchNormalization
from keras.layers.pooling import MaxPooling2D, AveragePooling2D
from keras.layers.merge import Concatenate
from keras.layers.core import Lambda, Flatten, Dense
from keras.initializers import glorot_uniform
from keras.engine.topology import Layer
from keras import backend as K
from keras.models import load_model

K.set_image_data_format('channels_first')

import pickle
import cv2
import os.path
import os
import numpy as np
from numpy import genfromtxt
import pandas as pd
import tensorflow as tf
from utility import *

# from webcam_utility import *
np.set_printoptions(threshold=np.nan)


# ## Model
# The model makes an encoding vector consisting of 128 numbers for the input image. Two encodings are compared and if the two encodings are similar then we say that the two images are of the same person otherwise they are different.
# The model uses **Triplet loss function**. The aim is to minimize this function.

# triplet loss function
#  y_pred - list containing three objects:
#         anchor(None, 128) -- encodings for the anchor images
#         positive(None, 128) -- encodings for the positive images
#         negative(None, 128) -- encodings for the negative images

class FaceRecognition:

    def __init__(self, absolute_database_path):
        self.FRmodel = self.load_FRmodel()
        self.user_db = self.ini_user_database(absolute_path=absolute_database_path)
        self.absolute_database_path = absolute_database_path

    def triplet_loss(self, y_true, y_pred, alpha=0.2):
        anchor, positive, negative = y_pred[0], y_pred[1], y_pred[2]

        # triplet formula components
        pos_dist = tf.reduce_sum(tf.square(tf.subtract(y_pred[0], y_pred[1])))
        neg_dist = tf.reduce_sum(tf.square(tf.subtract(y_pred[0], y_pred[2])))
        basic_loss = pos_dist - neg_dist + alpha

        loss = tf.maximum(basic_loss, 0.0)

        return loss

    # ### Loading the Model
    # The model outputs a vector of 128 numbers which represent encoding for the given input image. We will be using this encoding vector for comparing two images.
    # #### Input
    # - This network takes as input 96x96 RGB image as its input. Specifically, inputs a tensor of shape $(m, n_C, n_H, n_W)$ , where $n_C$ = channel.
    #
    # #### Output
    # - A matrix of shape **(m, 128)** where the 128 numbers are the encoding values for $ith$ image.
    # load the model
    def load_FRmodel(self):
        FRmodel = load_model('models/model.h5', custom_objects={'triplet_loss': self.triplet_loss})
        return FRmodel

    # We will create a database of registered. For this we will use a simple dictionary and map each registered user with his/her face encoding.
    # initialize the user database
    def ini_user_database(self, absolute_path):
        # check for existing database
        if os.path.exists(absolute_path):
            with open(absolute_path, 'rb') as handle:
                user_db = pickle.load(handle)
        else:
            # make a new one
            # we use a dict for keeping track of mapping of each person with his/her face encoding
            user_db = {}
        return user_db

    # adds a new user face to the database using his/her image stored on disk using the image path
    def add_user_img_path(self, user_db, FRmodel, name, img_path):
        resize_img(img_path)
        if name not in user_db:
            user_db[name] = img_to_encoding(img_path, FRmodel)
            # save the database
            with open(self.absolute_database_path, 'wb') as handle:
                pickle.dump(user_db, handle, protocol=pickle.HIGHEST_PROTOCOL)
            print('User ' + name + ' added successfully')
            return True
        else:
            print('The ID is already registered! Try a different name.........')
            return False

    # adds a new user using image taken from webcam
    # def add_user_webcam(user_db, FRmodel, name):
    #     # we can use the webcam to capture the user image then get it recognized
    #     face_found = detect_face(user_db, FRmodel)
    #
    #     if face_found:
    #         resize_img("saved_image/1.jpg")
    #         if name not in user_db:
    #             add_user_img_path(user_db, FRmodel, name, "saved_image/1.jpg")
    #         else:
    #             print('The name is already registered! Try a different name.........')
    #     else:
    #         print('There was no face found in the visible frame. Try again...........')
    #

    # deletes a registered user from database
    def delete_user(self, user_db, name):
        popped = user_db.pop(name, None)

        if popped is not None:
            print('User ' + name + ' deleted successfully')
            # save the database
            with open(self.absolute_database_path, 'wb') as handle:
                pickle.dump(user_db, handle, protocol=pickle.HIGHEST_PROTOCOL)
            return True
        elif popped == None:
            print('No such user !!')
            return False

    # ### Putting everything together
    # For making this face recognition system we are going to take the input image, find its encoding and then
    # see if there is any similar encoding in the database or not. We define a threshold value to decide whether the two images are similar
    # or not based on the similarity of their encodings.
    def find_face(self, image_path, database, model, threshold):
        # find the face encodings for the input image
        resize_img(image_path)
        encoding = img_to_encoding(image_path, model)

        min_dist = 99999
        # loop over all the recorded encodings in database
        for name in database:
            # find the similarity between the input encodings and claimed person's encodings using L2 norm
            dist = np.linalg.norm(np.subtract(database[name], encoding))
            # check if minimum distance or not
            if dist < min_dist:
                min_dist = dist
                identity = name

        if min_dist > threshold:
            print("User not in the database.")
            identity = 'unknown'
        else:
            print("Hi! " + str(identity) + ", L2 distance: " + str(min_dist))

        return min_dist, identity

    # for doing face recognition
    def do_face_recognition(self, user_db, FRmodel, threshold, save_loc):
        # we can use the webcam to capture the user image then get it recognized
        # face_found = detect_face(user_db, FRmodel)
        face_found = True
        if face_found:
            self.find_face(save_loc, user_db, FRmodel, threshold)
        else:
            print('There was no face found in the visible frame. Try again...........')

    def delete_all_users(self, user_db):
        names = []
        for name in user_db:
            names.append(name)
        for name in names:
            status = self.delete_user(user_db, name)
            if status == False:
                return False
        return True

    def recognizeFace(self, image_path, threshold=0.6):
        min_distance, identity = self.find_face(image_path=image_path, database=self.user_db, model=self.FRmodel,
                                                threshold=threshold)
        if identity == 'unknown':
            return False, identity
        else:
            return True, identity

    def addFace(self, id, image_path):
        status = self.add_user_img_path(user_db=self.user_db, FRmodel=self.FRmodel, name=id, img_path=image_path)
        return status

    def deleteFace(self, id):
        status = self.delete_user(user_db=self.user_db, name=id)
        return status

    def deleteAllFaces(self):
        status = self.delete_all_users(user_db=self.user_db)
        return status

    def my_main(self):
        FRmodel = self.FRmodel
        print('\n\nModel loaded...')

        user_db = self.user_db
        print('User database loaded')

        ch = 'y'
        while (ch == 'y' or ch == 'Y'):
            user_input = input(
                '\nEnter choice \n1. Recognize face via image path\n2. Add or Delete user\n3. Quit\n')

            if user_input == '1':
                os.system('cls' if os.name == 'nt' else 'clear')
                # we can use the webcam to capture the user image then get it recognized
                img_path = input('Enter Absolute Path to the Face:')
                threshold = float(input('Enter Maximum Affordable Distance:'))
                self.do_face_recognition(user_db, FRmodel, threshold=threshold, save_loc=img_path)

            elif user_input == '2':
                os.system('cls' if os.name == 'nt' else 'clear')
                print('1. Add user using saved image path\n2. Delete user\n3. Delete all users.\n')

                add_ch = input()
                name = input('Enter the ID of the person\n')

                if add_ch == '1':
                    img_path = input('Enter the face\'s absolute path path:\n')
                    self.add_user_img_path(user_db, FRmodel, name, img_path)
                elif add_ch == '2':
                    self.delete_user(user_db, name)
                elif add_ch == '3':
                    self.delete_all_users(user_db)
                else:
                    print('Invalid choice....\n')

            elif user_input == '3':
                return

            else:
                print('Invalid choice....\nTry again?\n')

            ch = input('Continue ? y or n\n')
            # clear the screen
            os.system('cls' if os.name == 'nt' else 'clear')

# obj = FaceRecognition()
# obj.my_main()
