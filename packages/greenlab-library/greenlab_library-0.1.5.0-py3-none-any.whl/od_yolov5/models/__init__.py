from __future__ import absolute_import
import os
from .yolov5 import YoloV5
from od_yolov5.utils.tools import get_cfg, download_url

__model_factory = {
    # face detection models
    'yolov5s': YoloV5,
    'yolov5m': YoloV5,
    'yolov5l': YoloV5,
    'yolov5x': YoloV5
}

_model_urls = {
    'yolov5s': '15QTwYBoGvRn3RnAJRhddPxhbVOS7HPNV',
    'yolov5m': '',
    'yolov5l': '',
    'yolov5x': ''
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
    if not os.path.exists('./models/Yolov5'):
        download_url(_model_urls[name], name=name, dst = "models")

    return __model_factory[name](config)
