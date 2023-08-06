import numpy as np
import imutils
import torch
import time
import cv2
import torch
import sys

from od_yolov5.author.old_models.yolo_old import Model
from od_yolov5.author.utils.torch_utils import select_device
# from od_yolov5.author.utils.datasets import *
# from od_yolov5.author.utils import *


class YoloV5:
    """ YOLOV5 Detection """
    def __init__(self, config):
        torch.backends.cudnn.benchmark = True
        self.device = select_device(config['yolov5']['device'])
        self.weight = config['yolov5']['weight']
        
        self.model = Model(config['yolov5']['config_path'])
        self.model.load_state_dict(torch.load(self.weight, map_location=self.device)['model'])
        self.model.float().fuse().eval()

        # self.model = torch.load(self.weight, map_location=self.device)['model_state_dict'].float()

        self.names = self.model.module.names if hasattr(self.model, 'module') else self.model.names
        self.agnostic_nms = False
        self.imgsz = config['yolov5']['imgsz']

    def detect(im0s, conf_thres=0.4, iou_thres=0.5,
                  wanted_labels=['car', 'bus', 'truck', 'motorcycle', 'bicycle']):

        # PREPROCESSING IMAGE
        # padded resize
        img = letterbox(im0s, new_shape=self.imgsz)[0]

        # convert
        img = img[:, :, ::-1].transpose(2, 0, 1)  # BGR to RGB, to 3x416x416
        img = np.ascontiguousarray(img)

        img = torch.from_numpy(img).to(device)
        img = img.float()
        img /= 255.0
        if img.ndimension() == 3:
            img = img.unsqueeze(0)

        # PREDICTION
        pred = self.model(img, augment=False)[0]
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes=None, agnostic=self.agnostic_nms)

        boxes = []
        class_names = []
        scores = []

        for i, det in enumerate(pred):
            if det is not None and len(det):
                # Rescale boxes from img_size to im0 size
                det[:, :4] = scale_coords(img.shape[2:], det[:, :4], im0s.shape).round()
                det = det.cpu().detach().numpy()
                for *xyxy, conf, cls in reversed(det):
                    x1, y1, x2, y2 = xyxy[0], xyxy[1], xyxy[2], xyxy[3]
                    w, h = x2 - x1, y2 - y1

                    if names[int(cls)] in wanted_labels:

                        boxes.append([int(x1), int(y1), int(w), int(h)])
                        class_names.append(str(names[int(cls)]))
                        scores.append(float(conf))

        return boxes, class_names, scores
