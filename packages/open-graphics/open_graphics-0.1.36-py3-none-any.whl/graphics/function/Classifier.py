"""
Name : Classifier.py
Author  : Cash
Contact : tkggpdc2007@163.com
Time    : 2020-01-08 10:52
Desc:
"""

import os

import numpy as np
import torch
from PIL import Image
from torchvision import transforms, datasets

from ..libs.resnet.network import Network, train_test_split

__all__ = ['train_test_split', 'Classifier']


class Classifier(Network):
    def __init__(self, model_name="resnet_checkpoint.pth.tar", ctx_id=-1):
        """
        图像分类
        :param model_name: 模型路径
        :param ctx_id: 指定GPU，-1表示CPU
        """
        super(Classifier, self).__init__(model_name, ctx_id)
        self.model = self.load_model()

    @staticmethod
    def transform_data():
        """
        数据增强函数，可改写
        :return:
        """
        data_transforms = {
            'train': transforms.Compose([
                transforms.Resize((224, 224)),  # fix from 224 to 299
                # transforms.RandomCrop(224),
                # transforms.RandomVerticalFlip(),
                transforms.RandomHorizontalFlip(),
                # transforms.RandomRotation(45),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406],
                                     [0.229, 0.224, 0.225])
            ]),
            'val': transforms.Compose([
                transforms.Resize((224, 224)),
                # transforms.CenterCrop(224),
                transforms.ToTensor(),
                transforms.Normalize([0.485, 0.456, 0.406],
                                     [0.229, 0.224, 0.225])
            ])
        }

        return data_transforms

    def load_model(self):
        """
        加载模型，可改写
        :return:
        """
        if not os.path.exists(self.model_name):
            return None
        model = torch.load(self.model_name, map_location=None if torch.cuda.is_available() else 'cpu')
        model = model.module
        if torch.cuda.is_available():
            print("Classify Use GPU: ", self.device)
            model = model.to(self.device)

        return model

    def predict(self, image):
        """
        图像预测
        :param image: 输入图像（numpy data）
        :return: 分类类别
        """
        temp = Image.fromarray(image).convert("RGB")
        temp = temp.resize((256, 256))
        # temp = ImageOps.equalize(temp)
        image_tensor = torch.FloatTensor(np.array(temp) / 255.0).permute(2, 0, 1)
        image_tensor = image_tensor.unsqueeze_(0)
        if torch.cuda.is_available():
            image_tensor = image_tensor.to(self.device)

        output = self.model(image_tensor)
        _, index = torch.max(output.data, 1)

        return int(index)

    def compute_accuracy(self, data_dir, batch_size=32):
        transform = self.transform_data()["val"]
        dataset = datasets.ImageFolder(data_dir, transform)
        data_loader = torch.utils.data.DataLoader(dataset, batch_size=batch_size, shuffle=False)

        correct_pred, num_examples = 0, 0
        for i, (features, targets) in enumerate(data_loader):
            features = features.to(self.device)
            targets = targets.to(self.device)

            output = self.model(features)
            _, index = torch.max(output.data, 1)

            num_examples += targets.size(0)
            correct_pred += (index == targets).sum()

        return correct_pred.float() / num_examples * 100
