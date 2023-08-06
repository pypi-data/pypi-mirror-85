import os
import random
from collections import Counter

import numpy as np
import torch
import torchvision.transforms.functional as TF
from PIL import Image, ImageFilter, ImageOps
from sklearn.utils import shuffle
from torch.utils.data import Dataset
from torchvision import transforms

IMG_SIZE = 256


class TrainDataset(Dataset):
    def __init__(self, path, grey=False, classes=[]):
        assert isinstance(path, str)
        self.x = []
        self.y = []
        self.path = path
        self.grey = grey
        self.class_dict = {s: i for i, s in enumerate(classes)}
        self.datalist = classes

        for labels in self.datalist:
            if labels == ".DS_Store":
                continue
            label = self.class_dict[labels]
            for image_file in os.listdir(os.path.join(self.path, labels)):
                if image_file == ".DS_Store":
                    continue
                image = Image.open(os.path.join(self.path, labels, image_file)).convert('RGB')
                image = image.resize((IMG_SIZE, IMG_SIZE))
                self.x.append(image)     # ImageOps.equalize(image)
                self.y.append(label)

        self.x, self.y = shuffle(self.x, self.y, random_state=42)
        self.counter = Counter(self.y)

    def __len__(self):
        return len(self.x)

    def __getitem__(self, i):
        if self.grey:
            grey = transforms.Grayscale()
            self.x[i] = grey(self.x[i])
            return torch.FloatTensor(np.array(self.x[i]).reshape(1, IMG_SIZE, IMG_SIZE) / 255.0), self.y[i]
        return torch.FloatTensor(np.array(self.x[i]) / 255.0).permute(2, 0, 1), self.y[i]

    def resample(self):
        """
        For class balancing
        :return:
        """
        random_crop = transforms.RandomResizedCrop(IMG_SIZE)
        target = max(self.counter.values())
        for x, y in zip(self.x, self.y):
            if self.counter[y] < target:
                self.x.append(random_crop(x))
                self.y.append(y)
                self.counter[y] += 1
        self.counter = Counter(self.y)
        assert len(set(self.counter.values())) == 1

    def augment(self, first=True):
        """
        For data augmentation
        :param first:
        :return:
        """
        # resize = transforms.Resize((IMG_SIZE, IMG_SIZE))
        colorjitter = transforms.ColorJitter(brightness=0.5, contrast=0.5, saturation=0.5, hue=0.5)
        shear = transforms.Compose([transforms.RandomAffine(0, shear=30), transforms.Resize((IMG_SIZE, IMG_SIZE))])

        for labels in self.datalist:
            if labels == ".DS_Store":
                continue
            label = self.class_dict[labels]
            for image_file in os.listdir(os.path.join(self.path, labels)):
                if image_file == ".DS_Store":
                    continue
                image = Image.open(os.path.join(self.path, labels, image_file)).convert('RGB')
                self.x.append(shear(image))
                self.y.append(label)

                # self.x.append(resize(image.rotate(random.uniform(-70, 70))))
                # self.y.append(label)

                image = image.resize((IMG_SIZE, IMG_SIZE))

                self.x.append(TF.adjust_brightness(image, random.random()))
                self.y.append(label)

                self.x.append(TF.adjust_brightness(image, random.random() + 1))
                self.y.append(label)

                if first:
                    self.x.append(image.filter(ImageFilter.BLUR))
                    self.y.append(label)

                    self.x.append(image.transpose(Image.FLIP_LEFT_RIGHT))
                    self.y.append(label)

                self.x.append(colorjitter(image))
                self.y.append(label)
        self.x, self.y = shuffle(self.x, self.y, random_state=42)


class TestDataset(Dataset):
    def __init__(self, path, grey=False):
        assert isinstance(path, str)
        self.images = []
        self.filenames = []
        self.grey = grey

        for image_file in os.listdir(path):
            image = Image.open(os.path.join(path, image_file)).convert('RGB')
            image = image.resize((IMG_SIZE, IMG_SIZE))

            self.images.append(image)
            self.filenames.append(image_file[:-4])

    def __len__(self):
        return len(self.images)

    def __getitem__(self, i):
        if self.grey:
            grey = transforms.Grayscale()
            self.images[i] = grey(self.images[i])
            return torch.FloatTensor(np.array(self.images[i]).reshape(1, IMG_SIZE, IMG_SIZE) / 255.0), self.filenames[i]
        return torch.FloatTensor(np.array(self.images[i]) / 255.0).permute(2, 0, 1), self.filenames[i]
