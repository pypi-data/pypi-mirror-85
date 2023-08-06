import yaml
import gdown
import zipfile
import os


def unzip(src: str, dst: str = ""):
    """unzip the file

    Args:
        src (str):
        dst (str):

    Returns:
        None
    """
    with zipfile.ZipFile(src, 'r') as zip_ref:
        if len(dst):
            zip_ref.extractall(dst)
        else:
            zip_ref.extractall()


def get_cfg(path: str):
    """Set up the config

    Args:
        path (str):

    Returns:
        None
    """
    
    yaml.warnings({'YAMLLoadWarning': False})
    with open(path, 'r') as fs:
        config = yaml.load(fs)
    return config


def download_url(id: str, name: str, dst: str = ""):
    """Downloads file from a url to a destination.
    
    Args:
        id (str): url to download file.
        dst (str): destination path.
    """

    url = "https://drive.google.com/uc?id=" + id
    output = name + '.zip'
    gdown.download(url, output, quiet=False)

    # unzip the file
    unzip(output, dst)

    # clean up space
    os.remove(output)
