import os
import tensorflow as tf
import numpy as np

from .EfficientDet.model import efficientdet
from .EfficientDet.utils import postprocess_boxes

class EfficientDet():
    """ Efficient Detection Model
    """

    def __init__(self, config):
        self.model = None
        self.config = config

        self.load_model()

    def load_model(self):
        """Load crowd counting model"""

        model_path = self.config['model2']['path']
        gpu_device = self.config['gpu']
        
        phi = self.config['model2']['params']['phi']
        weighted_bifpn = self.config['model2']['params']['weighted_bifpn']
        num_classes = self.config['model2']['params']['num_classes']
        score_threshold = self.config['model2']['params']['score_threshold']

        if gpu_device==-1:
            with tf.device('/cpu:0'):
                _, self.model = efficientdet(phi=phi,
                                            weighted_bifpn=weighted_bifpn,
                                            num_classes=num_classes,
                                            score_threshold=score_threshold)
                self.model.load_weights(model_path, by_name=True)
                print('Load the pretrained model sucessfully!')
        else:
            with tf.device('/gpu:{}'.format(gpu_device)):
                _, self.model = efficientdet(phi=phi,
                                            weighted_bifpn=weighted_bifpn,
                                            num_classes=num_classes,
                                            score_threshold=score_threshold)
                self.model.load_weights(model_path, by_name=True)
                print('Load the pretrained model sucessfully in GPU mode!')


    def get_predictions(self, image, scale, h, w):
        """ Get the predictions from the input image

        Args:
            image (np.array): the RGB image

        Returns:

        """
        try:
            # run network
            boxes, scores, labels = self.model.predict_on_batch([np.expand_dims(image, axis=0)])
            boxes, scores, labels = np.squeeze(boxes), np.squeeze(scores), np.squeeze(labels)
            boxes = postprocess_boxes(boxes=boxes, scale=scale, height=h, width=w)

            # select indices which have a score above the threshold
            score_threshold = self.config['model2']['params']['score_threshold']
            indices = np.where(scores[:] > score_threshold)[0]

            # select those detections
            boxes = boxes[indices]
            labels = labels[indices]

            # select indices which have a label 'person'
            indices = np.where(labels[:]==0)[0]

            # select those detections
            boxes = boxes[indices]
            labels = labels[indices]
            scores = scores[indices]
            return boxes, labels, scores
        except:
            return None, None, None
