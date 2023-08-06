import numpy as np
import mxnet as mx
import cv2
from sklearn import preprocessing
from skimage import transform as trans

class ArcFace():
    """
        ArcFace
        Framework: Mxnet
        Args:
            ctx: gpu or cpu
            img_size:

        Returns:

    """

    def __init__(self, config):
        """

        Args:
            config ():
        """

        if config['face_embedding']['gpuid'] >= 0:
            self.ctx = mx.gpu(config['face_embedding']['gpuid'])
        else:
            self.ctx = mx.cpu()

        self.image_size = tuple(config['face_embedding']['img_size'])
        self.model = None

        if config['face_embedding']['weight']:
            self.model = self.get_model(self.ctx, self.image_size, config['face_embedding']['weight'], 'fc1')

    def get_model(self, ctx, image_size, model_str, layer):
        """ Get the model """
        _vec = model_str.split(',')
        assert len(_vec) == 2
        prefix = _vec[0]
        epoch = int(_vec[1])

        print('[INFO] Loading Face Detection Model...', prefix)

        sym, arg_params, aux_params = mx.model.load_checkpoint(prefix, epoch)
        all_layers = sym.get_internals()
        sym = all_layers[layer + '_output']
        model = mx.mod.Module(symbol=sym, context=ctx, label_names=None)
        model.bind(data_shapes=[('data', (1, 3, image_size[0], image_size[1]))])
        model.set_params(arg_params, aux_params)
        return model

    def get_input_2(self, face_img, bbox=None, points=None):
        """

        Args:
            face_img ():
            bbox ():
            points ():

        Returns:

        """

        if bbox.shape[0] == 0:
            return None
        nimg = self.preprocess(face_img, bbox, points, image_size='112,112')
        nimg = cv2.cvtColor(nimg, cv2.COLOR_BGR2RGB)
        aligned = np.transpose(nimg, (2, 0, 1))
        return aligned

    def get_input_3(self, face_img, bbox=None, points=None):
        if bbox.shape[0] == 0:
            return None

        nimg = self.preprocess(face_img, bbox, points, image_size='112,112')

        return nimg  # aligned

    def get_feature(self, aligned):
        """

        Args:
            aligned ():

        Returns:

        """

        input_blob = np.expand_dims(aligned, axis=0)
        data = mx.nd.array(input_blob)
        db = mx.io.DataBatch(data=(data,))

        self.model.forward(db, is_train=False)
        embedding = self.model.get_outputs()[0].asnumpy()
        embedding = preprocessing.normalize(embedding).flatten()
        return embedding

    def read_image(self, img_path, **kwargs):
        mode = kwargs.get('mode', 'rgb')
        layout = kwargs.get('layout', 'HWC')
        if mode == 'gray':
            img = cv2.imread(img_path, cv2.CV_LOAD_IMAGE_GRAYSCALE)
        else:
            img = cv2.imread(img_path, cv2.CV_LOAD_IMAGE_COLOR)
            if mode == 'rgb':
                # print('to rgb')
                img = img[..., ::-1]
            if layout == 'CHW':
                img = np.transpose(img, (2, 0, 1))
        return img

    def preprocess(self, img, bbox=None, landmark=None, **kwargs):
        if isinstance(img, str):
            img = self.read_image(img, **kwargs)
        M = None
        image_size = []
        str_image_size = kwargs.get('image_size', '')
        if len(str_image_size) > 0:
            image_size = [int(x) for x in str_image_size.split(',')]
            if len(image_size) == 1:
                image_size = [image_size[0], image_size[0]]
            assert len(image_size) == 2
            assert image_size[0] == 112
            assert image_size[0] == 112 or image_size[1] == 96
        if landmark is not None:
            assert len(image_size) == 2
            src = np.array([
                [30.2946, 51.6963],
                [65.5318, 51.5014],
                [48.0252, 71.7366],
                [33.5493, 92.3655],
                [62.7299, 92.2041]], dtype=np.float32)
            if image_size[1] == 112:
                src[:, 0] += 8.0
            dst = landmark.astype(np.float32)

            tform = trans.SimilarityTransform()
            tform.estimate(dst, src)
            M = tform.params[0:2, :]

        if M is None:
            if bbox is None:  # use center crop
                det = np.zeros(4, dtype=np.int32)
                det[0] = int(img.shape[1] * 0.0625)
                det[1] = int(img.shape[0] * 0.0625)
                det[2] = img.shape[1] - det[0]
                det[3] = img.shape[0] - det[1]
            else:
                det = bbox
            margin = kwargs.get('margin', 44)
            bb = np.zeros(4, dtype=np.int32)
            bb[0] = np.maximum(det[0] - margin / 2, 0)
            bb[1] = np.maximum(det[1] - margin / 2, 0)
            bb[2] = np.minimum(det[2] + margin / 2, img.shape[1])
            bb[3] = np.minimum(det[3] + margin / 2, img.shape[0])
            ret = img[bb[1]:bb[3], bb[0]:bb[2], :]
            if len(image_size) > 0:
                ret = cv2.resize(ret, (image_size[1], image_size[0]))
            return ret
        else:  # do align using landmark
            assert len(image_size) == 2

            warped = cv2.warpAffine(img, M, (image_size[1], image_size[0]), borderValue=0.0)

            return warped