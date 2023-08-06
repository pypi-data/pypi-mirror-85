import os
import tensorflow as tf
from tensorflow.keras.models import model_from_json
import numpy as np


class SANet():
    """ SANet Model
    """

    def __init__(self, config):
        self.model = None
        self.config = config

        self.load_model()

    def load_model(self):
        """Load crowd counting model"""

        model_path = self.config['model1']['path']
        json_path = self.config['model1']['cfg_json']
        gpu_device = self.config['gpu']

        if gpu_device==-1:
            with tf.device('/cpu:0'):
                with open(json_path, 'r') as json_file:
                    model_json = json_file.read()

                self.model = model_from_json(model_json)
                self.model.load_weights(model_path)
                print('Load the pretrained model sucessfully!')
        else:
            with tf.device('/gpu:{}'.format(gpu_device)):
                with open(json_path, 'r') as json_file:
                    model_json = json_file.read()

                self.model = model_from_json(model_json)
                self.model.load_weights(model_path)
                print('Load the pretrained model sucessfully in GPU mode!')


    def get_densitymap(self, image):
        """ Get the density map from the input image

        Args:
            image (np.array): the RGB image

        Returns:

        """
        try:
            output = self.model.predict(np.expand_dims(image, axis=0))
            output = np.squeeze(output)
            return output
        except:
            return None
