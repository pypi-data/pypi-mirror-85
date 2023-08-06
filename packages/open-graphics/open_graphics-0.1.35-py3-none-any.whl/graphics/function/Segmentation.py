"""
Name : FaceDetector.py
Author  : Cash
Contact : tkggpdc2007@163.com
Time    : 2020-01-08 10:52
Desc:
"""

import cv2
import numpy as np
import torch
import torch.nn.functional as F

from ..libs.yolact.config import cfg, MEANS, STD, COCO_CLASSES
from ..libs.yolact.output_utils import postprocess
from ..libs.yolact.yolact import Yolact


class FastBaseTransform(torch.nn.Module):
    """
    Transform that does all operations on the GPU for super speed.
    This doesn't suppport a lot of config settings and should only be used for production.
    Maintain this as necessary.
    """

    def __init__(self):
        super().__init__()

        self.mean = torch.Tensor(MEANS).float()[None, :, None, None]
        self.std = torch.Tensor(STD).float()[None, :, None, None]
        self.transform = cfg.backbone.transform

    def forward(self, img):
        # self.mean = self.mean.to(img.device)
        # self.std = self.std.to(img.device)

        # img assumed to be a pytorch BGR image with channel order [n, h, w, c]
        if cfg.preserve_aspect_ratio:
            raise NotImplementedError

        img = img.permute(0, 3, 1, 2).contiguous()
        img = F.interpolate(img, (cfg.max_size, cfg.max_size), mode='bilinear', align_corners=False)

        if self.transform.normalize:
            img = (img - self.mean) / self.std
        elif self.transform.subtract_means:
            img = (img - self.mean)
        elif self.transform.to_float:
            img = img / 255

        if self.transform.channel_order != 'RGB':
            raise NotImplementedError

        img = img[:, (2, 1, 0), :, :].contiguous()

        # Return value is in channel order [n, c, h, w] and RGB
        return img


class Segmentation(object):

    def __init__(self, model_name='yolact_im700_54_800000.pth', ctx_id=-1):
        self.model_name = model_name
        self.ctx_id = ctx_id if torch.cuda.is_available() else -1
        self.device = torch.device("cuda:" + str(ctx_id)) if self.ctx_id > -1 else torch.device("cpu")
        self.net = self.load_model()
        self.transformer = FastBaseTransform()

    def load_model(self):
        net = Yolact()
        net.detect.use_fast_nms = False
        net.load_weights(self.model_name, True if self.ctx_id > -1 else False)
        if torch.cuda.is_available():
            net.to(self.device)
        net.eval()

        return net

    @staticmethod
    def to_tensor(image):
        temp = np.zeros((image.shape[0], image.shape[1], 3))
        if len(image.shape) == 2:
            image = image.reshape(image.shape[0], image.shape[1], 1)
            temp[:, :, 0] = image[:, :, 0]
            temp[:, :, 1] = image[:, :, 0]
            temp[:, :, 2] = image[:, :, 0]
        else:
            temp[:, :, 0] = image[:, :, 0]
            temp[:, :, 1] = image[:, :, 1]
            temp[:, :, 2] = image[:, :, 2]

        temp = np.expand_dims(temp, 0)
        temp = np.asarray(temp, np.float32)
        return torch.from_numpy(temp.astype(np.float32))

    def predict(self, image, score_threshold=0.1, top_k=100, class_name='person'):
        w, h = image.shape[:2][::-1]
        x = self.to_tensor(image)
        x = self.transformer(x)

        if torch.cuda.is_available():
            x = x.to(self.device)

        y = self.net(x)
        t = postprocess(y,
                        cfg.max_size,
                        cfg.max_size,
                        crop_masks=True,
                        score_threshold=score_threshold
                        )
        masks = t[3][:top_k]
        classes, scores, boxes = [x[:top_k].detach().cpu().numpy() for x in t[:3]]

        num_dets_to_consider = min(top_k, classes.shape[0])
        for j in range(num_dets_to_consider):
            if scores[j] < score_threshold:
                num_dets_to_consider = j
                break
        mask = None
        for j in reversed(range(num_dets_to_consider)):
            _class = COCO_CLASSES[classes[j]]
            if _class == class_name:
                if mask is None:
                    mask = np.asarray(masks[j].detach().cpu().numpy().squeeze() * 255, np.uint8)
                else:
                    mask1 = np.asarray(masks[j].detach().cpu().numpy().squeeze() * 255, np.uint8)
                    mask = mask | mask1

        return cv2.resize(mask, (w, h), cv2.INTER_LINEAR) if mask is not None else None
