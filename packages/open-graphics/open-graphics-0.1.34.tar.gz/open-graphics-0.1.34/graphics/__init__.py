from .function import Analysis
from .function import Calculate
from .function import Classifier
from .function import Color, get_temperature, get_hsv, get_hist
from .function import Evaluate
from .function import FaceDetector
from .function import Format
from .function import Graphics
from .function import MachineLearning
from .function import MtcnnDetector
from .function import MultiLabelClassify
from .function import OcrDetector
from .function import Recognizer
from .function import SceneDetector
from .function import Segmentation
from .function import VideoProcess
from .function import train_test_split

__all__ = ['Analysis',
           'Graphics',
           'MultiLabelClassify',
           'Format',
           'Color',
           'get_temperature',
           'get_hsv',
           'get_hist',
           'VideoProcess',
           'SceneDetector',
           'MtcnnDetector',
           'OcrDetector',
           'Classifier',
           'train_test_split',
           'Segmentation',
           'Evaluate',
           'Calculate',
           'MachineLearning',
           'FaceDetector',
           'Recognizer']
