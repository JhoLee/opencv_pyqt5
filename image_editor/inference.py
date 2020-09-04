import datetime
import enum
import time

import cv2
import numpy as np
import torch
from PIL import Image
from torchvision import transforms

from main.utils import print_log


class InferenceModel:
    def __init__(self):
        self._cuda = torch.cuda.is_available()
        self._model = None
        self._image = None
        self._result = None
        self._batch = None
        self._output = None
        self._predictions = None

    @property
    def cuda(self):
        return self._cuda

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model_name="deeplabv3_resnet101"):
        print_log("Start")
        print_log("model: {}".format(model_name))
        _model = torch.hub.load('pytorch/vision:v0.6.0', model_name, pretrained=True)
        _model.eval()
        print_log("End")
        self._model = _model

    @property
    def image(self):
        return self._image

    @image.setter
    def image(self, image):
        print_log("Start")
        print_log("Type: {}".format(type(image)))
        if isinstance(image, str):
            image = cv2.imread(image)
            self._image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        elif isinstance(image, np.ndarray):
            self._image = image
        elif isinstance(image, Image.Image):
            self._image = np.asarray(image)

        print_log("Shape: {}".format(self._image.shape))

    @property
    def batch(self):
        return self._batch

    @batch.setter
    def batch(self, image):
        print_log("Start")
        batch = transforms.Compose([
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406], std=[0.229, 0.224, 0.225])
        ])(image).unsqueeze(0)
        self._batch = batch
        print_log("End")

    @property
    def output(self):
        return self._output

    @property
    def predictions(self):
        return self._predictions

    def to_cuda(self):
        if self.cuda:
            print_log("using cuda")
            self.batch.to('cuda')
            self.model.to('cuda')
        else:
            print_log("using cpu")
            self.batch.to('cpu')
            self.model.to('cpu')

        return self.cuda

    def inference(self):
        print_log("Start")
        start_t = time.time()
        with torch.no_grad():
            self._output = self.model(self.batch)['out'][0]
        end_t = time.time()
        t = end_t - start_t
        print_log("Inference time: {}".format(time.strftime("%Mm %S.%fs", time.gmtime(t))[:-3]))
        self._predictions = self.output.argmax(0).byte().cpu().numpy()
        print_log("End")

    def get_prediction(self, label: str):
        print_log("class: {}".format(label))
        prediction = np.where(self.predictions == Label[label.upper()].value, 1, 0)
        return prediction

    def get_classes(self):
        sum = self.predictions.shape[0] * self.predictions.shape[1]
        classes, counts = np.unique(self.predictions, return_counts=True)
        classes = [Label(_class).name for _class in classes]
        percentages = [count / sum * 100 for count in counts]
        print_log("There are {} classes.".format(len(classes)))
        for _class, percentage in zip(classes, percentages):
            print_log("'{}' ({:.2f}%)".format(_class, percentage))
        return classes, percentages


class Label(enum.Enum):
    BACKGROUND = 0
    AEROPLANE = 1
    BICYCLE = 2
    BIRD = 3
    BOAT = 4
    BOTTLE = 5
    BUS = 6
    CAR = 7
    CAT = 8
    CHAIR = 9
    COW = 10
    DININGTABLE = 11
    DOG = 12
    HORSE = 13
    MOTORBIKE = 14
    PERSON = 15
    POTTEDPLANT = 16
    SHEEP = 17
    SOFA = 18
    TRAIN = 19
    TVMONITOR = 20
