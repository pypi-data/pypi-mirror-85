from __future__ import absolute_import

import os
import sys

from .sanet import SANet
from .edet import EfficientDet

from crowd_counting.utils.tools import get_cfg, download_model, download_url

__model_factory = {
    # density map-based counting
    'densitymap': SANet,
    # detection-based counting
    'detection': EfficientDet
}

_model_urls = {
    'densitymap': ['1Gfbxk1ONNkdp_aPLnaYftbWpz7D97BHN',
                    '1BT1O0JghB80RnYrhumicBbxORKGX-wpO'],
    'detection': '1LItLb0V5lHMJM-LYx4uWEFe_NbcIm0Gf'
}

def show_avai_models():
    """Displays available models.

    Examples::
        >>> from crowd_counting import models
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
        os.mkdir('models')
    except:
        pass
    
    try:
        os.mkdir('models/CrowdCounting')
    except:
        pass

    if name=='densitymap':
        # Check the models are existed or not
        if not os.path.exists('models/CrowdCounting/densitymap.hdf5'):
            download_model(_model_urls['densitymap'][0], name='densitymap', ext='.hdf5', dst = "models/CrowdCounting")
        if not os.path.exists('models/CrowdCounting/densitymap.json'):
            download_model(_model_urls['densitymap'][1], name='densitymap', ext='.json', dst = "models/CrowdCounting")
    elif name=='detection':
        # Check the models are existed or not
        if not os.path.exists('models/CrowdCounting/detection.h5'):
            download_model(_model_urls['detection'], name='detection.h5', dst = "models/CrowdCounting")

    return __model_factory[name](config)
