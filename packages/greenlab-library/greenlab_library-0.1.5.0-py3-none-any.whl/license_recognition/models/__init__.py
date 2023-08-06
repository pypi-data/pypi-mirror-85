from __future__ import absolute_import

import os
import sys

from .wpod import WPOD
from .ocr import OCR

from license_recognition.utils.tools import get_cfg, download_url

__model_factory = {
    # license plate detection
    'wpod': WPOD,

    # number extracting
    'ocr': OCR
}

_model_urls = {
    'wpod': '1xKNbPIERGA0vf3Y4vdENxvij2H1RXL6H',
    'ocr': '1uTsHKHnxH5fqfOGvqtrkw1OQU3Ue9Lw6'
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
    if not os.path.exists('models/LicenseRecognition/ocr'):
        download_url(_model_urls['ocr'], name='ocr', dst = "models")

    if not os.path.exists('models/LicenseRecognition/wpod'):
        download_url(_model_urls['wpod'],name = 'wpod', dst = "models")

    return __model_factory[name](config)
