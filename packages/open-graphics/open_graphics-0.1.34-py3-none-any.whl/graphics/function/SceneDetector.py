"""
Name : SceneDetector.py
Author  : Cash
Contact : tkggpdc2007@163.com
Time    : 2020-08-13 10:52
Desc:
"""

import os
import threading

import numpy as np
import torch
from torch.nn import functional as F
from torchvision import transforms

# from ..common.logs import logs
from ..libs.place365 import wideresnet

__all__ = ["SceneDetector"]

os.environ["KMP_DUPLICATE_LIB_OK"] = "TRUE"


class SceneDetector:
    def __init__(self, model_dir="models"):
        self.classes, self.labels_IO, self.labels_attribute, self.W_attribute = self.load_labels(model_dir)
        self.model = self.load_model(model_dir)
        self.tf = self.to_tensor()
        self.lock = threading.Lock()

    @staticmethod
    def load_labels(model_dir):
        # scene category relevant
        filename_category = os.path.join(model_dir, 'categories_places365.txt')
        classes = list()
        with open(filename_category) as class_file:
            for line in class_file:
                classes.append(line.strip().split(' ')[0][3:])
        classes = tuple(classes)

        # indoor and outdoor relevant
        filename_IO = os.path.join(model_dir, 'IO_places365.txt')
        with open(filename_IO) as f:
            lines = f.readlines()
            labels_IO = []
            for line in lines:
                items = line.rstrip().split()
                labels_IO.append(int(items[-1]) - 1)  # 0 is indoor, 1 is outdoor
        labels_IO = np.array(labels_IO)

        # scene attribute relevant
        filename_attribute = os.path.join(model_dir, 'labels_sunattribute.txt')
        with open(filename_attribute) as f:
            lines = f.readlines()
            labels_attribute = [item.rstrip() for item in lines]

        filename_W = os.path.join(model_dir, 'W_sceneattribute_wideresnet18.npy')
        W_attribute = np.load(filename_W)

        return classes, labels_IO, labels_attribute, W_attribute

    @staticmethod
    def load_model(model_dir):
        model = wideresnet.resnet18(num_classes=365)
        checkpoint = torch.load(os.path.join(model_dir, "wideresnet18_places365.pth.tar"),
                                map_location=None if torch.cuda.is_available() else 'cpu')
        state_dict = {str.replace(k, 'module.', ''): v for k, v in checkpoint['state_dict'].items()}
        model.load_state_dict(state_dict)
        model.avgpool = torch.nn.AvgPool2d(kernel_size=14, stride=1, padding=0)
        model.eval()

        return model

    @staticmethod
    def to_tensor():
        # load the image transformer
        transformer = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])
        ])
        return transformer

    def predict(self, image):
        features_blobs = []

        # 闭包 为了thread safety
        def hook_feature(module, input, output):
            features_blobs.append(np.squeeze(output.data.cpu().numpy()))

        def add_hook():
            features_names = ['layer4', 'avgpool']  # this is the last conv layer of the resnet
            removable_handles = []
            for name in features_names:
                removable_handles.append(self.model._modules.get(name).register_forward_hook(hook_feature))
            return removable_handles

        self.lock.acquire()  # hook need synchronized
        removable_handles = add_hook()  # need to remove at last
        try:
            from PIL import Image
            img = Image.fromarray(image)
            if img.mode == 'RGBA':
                img = img.convert('RGB')
            img = self.tf(img).unsqueeze(0)
            # forward pass
            logit = self.model(img)
        finally:
            for handle in removable_handles:
                handle.remove()
            self.lock.release()
        # confirm multi-thread safety
        assert len(features_blobs) == 2

        h_x = F.softmax(logit, 1).data.squeeze()
        probs, idx = h_x.sort(0, True)
        probs = probs.numpy()
        idx = idx.numpy()

        predict_res = {}
        # output the IO prediction
        io_image = np.mean(self.labels_IO[idx[:10]])  # vote for the indoor or outdoor

        if io_image < 0.5:
            predict_res['environment'] = 'indoor'
        else:
            predict_res['environment'] = 'outdoor'

        # output the prediction of scene category
        scene_categories = []
        for i in range(0, 5):
            category = {
                'name': self.classes[idx[i]],
                'score': str(probs[i])
            }
            scene_categories.append(category)
        predict_res['scene_categories'] = scene_categories

        # output the scene attributes
        responses_attribute = self.W_attribute.dot(features_blobs[1])
        idx_a = np.argsort(responses_attribute)
        attributes = [self.labels_attribute[idx_a[i]] for i in range(-1, -10, -1)]
        predict_res['attributes'] = attributes
        return predict_res


if __name__ == '__main__':
    import cv2
    import graphics as g

    scene_detector = g.SceneDetector('models')
    img = cv2.imread("14.jpg")[:, :, ::-1]
    res = scene_detector.predict(img)
