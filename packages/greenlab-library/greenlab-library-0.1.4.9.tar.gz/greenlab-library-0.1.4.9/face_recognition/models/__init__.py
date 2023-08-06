from __future__ import absolute_import
import os
from .retina import RetinaFace
from .arcnet import ArcFace
from face_recognition.utils.tools import get_cfg, download_url

__model_factory = {
    # face detection models
    'retina-r50': RetinaFace,

    # face embedding models
    'arc-face': ArcFace
}

_model_urls = {
    'arc-face': '12llN-EmB0NN0mbFNZk8BSAugbmzqNdPQ',
    'retina-r50': '1Irq1yhS4CclF7LQIRi7cgESybYvqCALN',
    'rcnn': '1-5IDPWueGSqvI7zSLyXuDcrUGQEIMv0G'
}

def show_avai_models():
    """Displays available models.

    Examples::
        >>> from face_recognition import models
        >>> models.show_avai_models()
    """
    print(list(__model_factory.keys()))


def build_model(name: str, cfg_path: str = ""):
    """A function wrapper for building a model.

    Args:
        name (str): model name
        cfg_path (str): path to config file
    Returns:
        model instance.
    """
    avai_models = list(__model_factory.keys())
    if name not in avai_models:
        raise KeyError(
            'Unknown model: {}. Must be one of {}'.format(name, avai_models)
        )
    if not len(cfg_path):
        raise RuntimeError(
            'Please input the path config file'
        )
    # Load config file
    config = get_cfg(cfg_path)

    try:
        os.makedirs('models')
    except:
        pass

    # Check the models are existed or not
    if not os.path.exists('models/FaceDetection'):
        download_url(_model_urls['retina-r50'], name='retina', dst = "models")

    if not os.path.exists('models/FaceEmbedding'):
        download_url(_model_urls['arc-face'],name = 'arc', dst = "models")

    return __model_factory[name](config)
