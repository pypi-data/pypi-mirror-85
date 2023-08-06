import statistics
from license_recognition.utils.tools import *

class OCR():
	""" OCR Model
	"""

	def __init__(self, config):
		self.model_ocr = None
		self.config = config
		
		self.ocr_classes = None

		self.load_classes()
		self.load_model_ocr()

	def load_classes(self):
		""" Load class names """

		model_classes = self.config['model2']['classes']

		with open(model_classes, 'rt') as f:
		    self.ocr_classes = f.read().rstrip('\n').split('\n')

	def load_model_ocr(self):
	    """Load orc model"""
	    
	    model_config = self.config['model2']['config']
	    model_weight = self.config['model2']['weight']
	    

	    self.model_ocr = cv2.dnn.readNetFromDarknet(model_config, model_weight)
	    self.model_ocr.setPreferableBackend(cv2.dnn.DNN_BACKEND_OPENCV)
	    self.model_ocr.setPreferableTarget(cv2.dnn.DNN_TARGET_CPU)


	def get_number(self, image):
	    """Get the string number from license plate

	    Args:
	        image (np.array): plate image after processing

	    Returns:
	        lp_str (str): number of plate
	    """        

	    H, W = image.shape[:2]

	    # Create a 4D blob from a image.
	    blob = cv2.dnn.blobFromImage(image, 1 / 255, (W, H), [0, 0, 0], 1, crop=False)

	    # Sets the input to the network
	    self.model_ocr.setInput(blob)

	    # Runs the forward pass to get output of the output layers
	    outs = self.model_ocr.forward(getOutputsNames(self.model_ocr))

	    # Remove the bounding boxes with low confidence
	    res = postprocess_ocr(image, outs, self.ocr_classes, 0.2, 0.1)

	    if len(res) <= 0:
	        return ""

	    L = dknet_label_conversion(res, W, H)
	    L = nms(L, .45)

	    # Compute the average height
	    heights = [l.wh()[1] for l in L]
	    avg_H = statistics.mean(heights)

	    # Sort letters by coordinate 'top'
	    L.sort(key=lambda x: x.tl()[1])

	    # Group the letters into rows
	    groups = do_grouping(L, bias=avg_H / 2)

	    # For each row, we sort letters from left to right
	    lp_str = ''
	    for g in groups:
	        g.sort(key=lambda x: x.tl()[0])
	        temp_str = ''.join([chr(l.cl()) for l in g])
	        lp_str = lp_str + temp_str + ' '

	    return lp_str