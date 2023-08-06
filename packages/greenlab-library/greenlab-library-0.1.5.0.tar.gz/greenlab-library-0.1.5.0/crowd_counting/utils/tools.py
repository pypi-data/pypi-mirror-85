import numpy as np
import cv2
import yaml
import gdown
import zipfile
import os
from shutil import copyfile


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


def download_model(id: str, name: str, ext: str, dst: str = "./"):
    """Downloads file from a url to a destination.
    
    Args:
        id (str): url to download file.
        dst (str): destination path.
    """

    url = "https://drive.google.com/uc?id=" + id
    output = name + ext
    gdown.download(url, output, quiet=False)
    
    copyfile(output, os.path.join(dst,output))
    
    # clean up space
    os.remove(output)


def download_url(id: str, name: str, dst: str = "./"):
    """Downloads file from a url to a destination.
    
    Args:
        id (str): url to download file.
        dst (str): destination path.
    """

    url = "https://drive.google.com/uc?id=" + id
    output = name + '.zip'
#    time.sleep(100)
    gdown.download(url, output, quiet=False)

    # unzip the file
    unzip(output, dst)

    # clean up space
    os.remove(output)


def load_img(path):
    img = cv2.cvtColor(cv2.imread(path), cv2.COLOR_BGR2RGB)
    img = img / 255.0
    img[:, :, 0] = (img[:, :, 0] - 0.485) / 0.229
    img[:, :, 1] = (img[:, :, 1] - 0.456) / 0.224
    img[:, :, 2] = (img[:, :, 2] - 0.406) / 0.225
    return img.astype(np.float32)

def preprocess_image(image, image_size):
    # image, RGB
    image_height, image_width = image.shape[:2]
    if image_height > image_width:
        scale = image_size / image_height
        resized_height = image_size
        resized_width = int(image_width * scale)
    else:
        scale = image_size / image_width
        resized_height = int(image_height * scale)
        resized_width = image_size

    image = cv2.resize(image, (resized_width, resized_height))
    image = image.astype(np.float32)
    image /= 255.
    mean = [0.485, 0.456, 0.406]
    std = [0.229, 0.224, 0.225]
    image -= mean
    image /= std
    pad_h = image_size - resized_height
    pad_w = image_size - resized_width
    image = np.pad(image, [(0, pad_h), (0, pad_w), (0, 0)], mode='constant')

    return image, scale


def load_processed_image(path, image_size=640):
    image = cv2.imread(path)

    # BGR -> RGB
    image = image[:, :, ::-1]
    h, w = image.shape[:2]
    image, scale = preprocess_image(image, image_size=image_size)
    return image, scale, h, w


def draw_boxes(image, boxes, scores, labels):
    num_classes = 90
    colors = [np.random.randint(0, 256, 3).tolist() for _ in range(num_classes)]
    for b, l, s in zip(boxes, labels, scores):
        class_id = int(l)
        class_name = 'person'
    
        xmin, ymin, xmax, ymax = list(map(int, b))
        score = '{:.4f}'.format(s)
        color = colors[class_id]
        label = '-'.join([class_name, score])
    
        ret, baseline = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
        cv2.rectangle(image, (xmin, ymin), (xmax, ymax), color, 1)
        cv2.rectangle(image, (xmin, ymax - ret[1] - baseline), (xmin + ret[0], ymax), color, -1)
        cv2.putText(image, label, (xmin, ymax - baseline), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)
