import numpy as np
import cv2
import tensorflow as tf
import yaml
from .label import Label
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


class DLabel (Label):
    
    def __init__(self,cl,pts,prob):
        self.pts = pts
        tl = np.amin(pts,1)
        br = np.amax(pts,1)
        Label.__init__(self,cl,tl,br,prob)

def IOU(tl1,br1,tl2,br2):
    """[summary]

    Args:
        tl1 ([type]): [description]
        br1 ([type]): [description]
        tl2 ([type]): [description]
        br2 ([type]): [description]

    Returns:
        [type]: [description]
    """ 
   
    wh1,wh2 = br1-tl1,br2-tl2
    assert((wh1>=.0).all() and (wh2>=.0).all())
    
    intersection_wh = np.maximum(np.minimum(br1,br2) - np.maximum(tl1,tl2),0.)
    intersection_area = np.prod(intersection_wh)
    area1,area2 = (np.prod(wh1),np.prod(wh2))
    union_area = area1 + area2 - intersection_area
    return intersection_area/union_area

def get_width_height(ptsh):
    """[summary]

    Args:
        ptsh ([type]): [description]

    Returns:
        [type]: [description]
    """    
 
    x1,x2,x3,x4 = ptsh[0]
    y1,y2,y3,y4 = ptsh[1]
    width = (abs(x2-x1) + abs(x3-x4))/2
    height = (abs(y4-y1) + abs(y3-y2))/2

    return width, height

def find_T_matrix(pts,t_pts):
    """[summary]

    Args:
        pts ([type]): [description]
        t_pts ([type]): [description]

    Returns:
        [type]: [description]
    """
     
    A = np.zeros((8,9))
    for i in range(0,4):
        xi  = pts[:,i]
        xil = t_pts[:,i]
        xi  = xi.T
        
        A[i*2,   3:6] = -xil[2]*xi
        A[i*2,   6: ] =  xil[1]*xi
        A[i*2+1,  :3] =  xil[2]*xi
        A[i*2+1, 6: ] = -xil[0]*xi

    
    [U,S,V] = np.linalg.svd(A)
    H = V[-1,:].reshape((3,3))

    return H


def getRectPts(tlx,tly,brx,bry):
    return np.matrix([[tlx,brx,brx,tlx],[tly,tly,bry,bry],[1.,1.,1.,1.]],dtype=float)

def IOU_labels(l1,l2):
    return IOU(l1.tl(),l1.br(),l2.tl(),l2.br())

def getWH(shape):
    return np.array(shape[1::-1]).astype(float)

def nms(Labels,iou_threshold=.5):

    SelectedLabels = []
    Labels.sort(key=lambda l: l.prob(),reverse=True)
    
    for label in Labels:

        non_overlap = True
        for sel_label in SelectedLabels:
            if IOU_labels(label,sel_label) > iou_threshold:
                non_overlap = False
                break

        if non_overlap:
            SelectedLabels.append(label)

    return SelectedLabels

def im2single(img):
    """

    Args:
        img ():

    Returns:

    """

    assert(img.dtype == 'uint8')
    return img.astype('float32')/255.


def preprocess_img(img):
    """Prepare the input image for model

    Args:
        img (np.array): np.array image, HxWx3

    Returns:
        input_img (np.array): image after processing, 1xHxWx3
        resized_img (np.array): resized image with shape of HxWx3
        img (np.array): original image

    """

    net_step = 2**4

    ratio = float(max(img.shape[:2]))/min(img.shape[:2])
    side  = int(ratio*288.)

    # max dimension
    bound_dim = min(side + (side%(2**4)),608)

    single_img = im2single(img)

    min_dim_img = min(single_img.shape[:2])
    factor = float(bound_dim)/min_dim_img

    w,h = (np.array(single_img.shape[1::-1],dtype=float)*factor).astype(int).tolist()
    w += (w%net_step!=0)*(net_step - w%net_step)
    h += (h%net_step!=0)*(net_step - h%net_step)

    resized_img = cv2.resize(single_img,(w,h))

    input_img = resized_img.copy()
    input_img = input_img.reshape((1,input_img.shape[0],input_img.shape[1],input_img.shape[2]))

    return input_img,resized_img,img

def postprocess_plate(Iorig,I,Y):
    """

    Args:
        Iorig ():
        I ():
        Y ():

    Returns:

    """

    threshold = 0.9

    square_out_size = (160,160)
    rectangle_out_size = (240,80)

    net_stride  = 2**4
    side        = ((208. + 40.)/2.)/net_stride # 7.75

    Probs = Y[...,0]
    Affines = Y[...,2:]

    xx,yy = np.where(Probs>threshold)

    WH = getWH(I.shape)
    MN = WH/net_stride

    vxx = vyy = 0.5 #alpha

    base = lambda vx,vy: np.matrix([[-vx,-vy,1.],[vx,-vy,1.],[vx,vy,1.],[-vx,vy,1.]]).T
    labels = []

    for i in range(len(xx)):
        y,x = xx[i],yy[i]
        affine = Affines[y,x]
        prob = Probs[y,x]

        mn = np.array([float(x) + .5,float(y) + .5])

        A = np.reshape(affine,(2,3))
        A[0,0] = max(A[0,0],0.)
        A[1,1] = max(A[1,1],0.)

        pts = np.array(A*base(vxx,vyy)) #*alpha
        pts_MN_center_mn = pts*side
        pts_MN = pts_MN_center_mn + mn.reshape((2,1))

        pts_prop = pts_MN/MN.reshape((2,1))

        labels.append(DLabel(0,pts_prop,prob))

    final_labels = nms(labels,.1)
    TLps = []
    is_square_list = []

    if len(final_labels):
        final_labels.sort(key=lambda x: x.prob(), reverse=True)
        for i,label in enumerate(final_labels):
            ptsh    = np.concatenate((label.pts*getWH(Iorig.shape).reshape((2,1)),np.ones((1,4))))
            width, height = get_width_height(ptsh)

            is_square = True
            out_size = square_out_size

            if (width >= height * 2):
                out_size = rectangle_out_size
                is_square = False
            
            t_ptsh  = getRectPts(0,0,out_size[0],out_size[1])
            
            H       = find_T_matrix(ptsh,t_ptsh)
            Ilp     = cv2.warpPerspective(Iorig,H,out_size,borderValue=.0)

            TLps.append(Ilp)
            is_square_list.append(is_square)

    return final_labels,TLps,is_square_list

# Get the names of the output layers
def getOutputsNames(net):
    # Get the names of all the layers in the network
    layersNames = net.getLayerNames()
    # Get the names of the output layers, i.e. the layers with unconnected outputs
    return [layersNames[i[0] - 1] for i in net.getUnconnectedOutLayers()]


def postprocess_ocr(frame, outs,classes,confThreshold,nmsThreshold):
    """

    Args:
        frame ():
        outs ():
        classes ():
        confThreshold ():
        nmsThreshold ():

    Returns:

    """

    frameHeight = frame.shape[0]
    frameWidth = frame.shape[1]

    # Scan through all the bounding boxes output from the network and keep only the
    # ones with high confidence scores. Assign the box's class label as the class with the highest score.

    cnt = 0
    classIds = []
    confidences = []
    boxes = []

    for out in outs:
        for detection in out:
            scores = detection[5:]
            classId = np.argmax(scores)
            confidence = scores[classId]
            if (confidence > confThreshold):
                center_x = int(detection[0] * frameWidth)
                center_y = int(detection[1] * frameHeight)
                width = int(detection[2] * frameWidth)
                height = int(detection[3] * frameHeight)
                left = int(center_x - width / 2)
                top = int(center_y - height / 2)
                if (width >= 1) and (height >= 1):
                    classIds.append(classId)
                    confidences.append(float(confidence))
                    boxes.append([left, top, width, height])

                cnt += 1
    # print("cnt = ", cnt)

    res = []

    if cnt == 0:
        return res
    # Perform non maximum suppression to eliminate redundant overlapping boxes with
    # lower confidences.
    indices = cv2.dnn.NMSBoxes(boxes, confidences, confThreshold, nmsThreshold)

    for i in indices:
        i = i[0]
        box = boxes[i]
        res.append([classes[classIds[i]], confidences[i], box])

    return res

def dknet_label_conversion(R,img_width,img_height):
    WH = np.array([img_width,img_height],dtype=float)
    L  = []
    for r in R:
        center = np.array(r[2][:2])/WH
        wh2 = (np.array(r[2][2:])/WH)*.5
        L.append(Label(ord(r[0]),tl=center-wh2,br=center+wh2,prob=r[1]))
    return L

def do_grouping(labels,bias):
    prev = None
    group = []
    for l in labels:
        top = l.tl()[1]
        if not prev or abs(top - prev) <= bias:
            group.append(l)
        else:
            yield group
            group = [l]
        prev = top
    if group:
        yield group