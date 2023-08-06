import os
from pathlib import Path

import numpy as np
import torch
import torch.nn.functional as F

from ..libs.dbface.DBFace import DBFace

__all__ = ['FaceDetector']


def clip_value(value, high, low=0):
    return max(min(value, high), low)


def exp(v):
    if isinstance(v, tuple) or isinstance(v, list):
        return [exp(item) for item in v]
    elif isinstance(v, np.ndarray):
        return np.array([exp(item) for item in v], v.dtype)

    gate = 1
    base = np.exp(1)
    if abs(v) < gate:
        return v * base

    if v > 0:
        return np.exp(v)
    else:
        return -np.exp(-v)


def pad(image, stride=32):
    has_change = False
    stdw = image.shape[1]
    if stdw % stride != 0:
        stdw += stride - (stdw % stride)
        has_change = True

    stdh = image.shape[0]
    if stdh % stride != 0:
        stdh += stride - (stdh % stride)
        has_change = True

    if has_change:
        newImage = np.zeros((stdh, stdw, 3), np.uint8)
        newImage[:image.shape[0], :image.shape[1], :] = image
        return newImage
    else:
        return image


def compute_iou(rec1, rec2):
    cx1, cy1, cx2, cy2 = rec1
    gx1, gy1, gx2, gy2 = rec2
    S_rec1 = (cx2 - cx1 + 1) * (cy2 - cy1 + 1)
    S_rec2 = (gx2 - gx1 + 1) * (gy2 - gy1 + 1)
    x1 = max(cx1, gx1)
    y1 = max(cy1, gy1)
    x2 = min(cx2, gx2)
    y2 = min(cy2, gy2)

    w = max(0, x2 - x1 + 1)
    h = max(0, y2 - y1 + 1)
    area = w * h
    iou = area / (S_rec1 + S_rec2 - area)
    return iou


def intv(*value):
    if len(value) == 1:
        value = value[0]
    if isinstance(value, tuple):
        return tuple([int(item) for item in value])
    elif isinstance(value, list):
        return [int(item) for item in value]
    elif value is None:
        return 0
    else:
        return int(value)


def floatv(*value):
    if len(value) == 1:
        value = value[0]
    if isinstance(value, tuple):
        return tuple([float(item) for item in value])
    elif isinstance(value, list):
        return [float(item) for item in value]
    elif value is None:
        return 0
    else:
        return float(value)


def nms(objs, iou=0.5):
    if objs is None or len(objs) <= 1:
        return objs
    objs = sorted(objs, key=lambda obj: obj.score, reverse=True)
    keep = []
    flags = [0] * len(objs)
    for index, obj in enumerate(objs):
        if flags[index] != 0:
            continue
        keep.append(obj)
        for j in range(index + 1, len(objs)):
            if flags[j] == 0 and obj.iou(objs[j]) > iou:
                flags[j] = 1
    return keep


class BBox:
    def __init__(self, label, xyrb, score=0, landmark=None, rotate=False):
        self.label = label
        self.score = score
        self.landmark = landmark
        self.x, self.y, self.r, self.b = xyrb
        self.rotate = rotate
        # 避免出现rb小于xy的时候
        minx = min(self.x, self.r)
        maxx = max(self.x, self.r)
        miny = min(self.y, self.b)
        maxy = max(self.y, self.b)
        self.x, self.y, self.r, self.b = minx, miny, maxx, maxy

    def __repr__(self):
        landmark_formated = ",".join(
            [str(item[:2]) for item in self.landmark]) if self.landmark is not None else "empty"
        return f"(BBox[{self.label}]: x={self.x:.2f}, y={self.y:.2f}, r={self.r:.2f}, " + \
               f"b={self.b:.2f}, width={self.width:.2f}, height={self.height:.2f}, landmark={landmark_formated})"

    @property
    def width(self):
        return self.r - self.x + 1

    @property
    def height(self):
        return self.b - self.y + 1

    @property
    def area(self):
        return self.width * self.height

    @property
    def haslandmark(self):
        return self.landmark is not None

    @property
    def xxxxxyyyyy_cat_landmark(self):
        x, y = zip(*self.landmark)
        return x + y

    @property
    def box(self):
        return [self.x, self.y, self.r, self.b]

    @box.setter
    def box(self, newvalue):
        self.x, self.y, self.r, self.b = newvalue

    @property
    def xywh(self):
        return [self.x, self.y, self.width, self.height]

    @property
    def center(self):
        return [(self.x + self.r) * 0.5, (self.y + self.b) * 0.5]

    # return cx, cy, cx.diff, cy.diff
    def safe_scale_center_and_diff(self, scale, limit_x, limit_y):
        cx = clip_value((self.x + self.r) * 0.5 * scale, limit_x - 1)
        cy = clip_value((self.y + self.b) * 0.5 * scale, limit_y - 1)
        return [int(cx), int(cy), cx - int(cx), cy - int(cy)]

    def safe_scale_center(self, scale, limit_x, limit_y):
        cx = int(clip_value((self.x + self.r) * 0.5 * scale, limit_x - 1))
        cy = int(clip_value((self.y + self.b) * 0.5 * scale, limit_y - 1))
        return [cx, cy]

    def clip(self, width, height):
        self.x = clip_value(self.x, width - 1)
        self.y = clip_value(self.y, height - 1)
        self.r = clip_value(self.r, width - 1)
        self.b = clip_value(self.b, height - 1)
        return self

    def iou(self, other):
        return compute_iou(self.box, other.box)


class FaceDetector:
    def __init__(self, model_dir=None, ctx_id=-1):
        self.model_dir = model_dir
        self.device = torch.device("cuda:" + str(ctx_id)) if ctx_id > -1 else torch.device("cpu")
        self.model = self.load_model()

    def load_model(self):
        model = DBFace()
        model.eval()
        if torch.cuda.is_available():
            model.to(self.device)

        if self.model_dir is None:
            self.model_dir = str(Path.home()) + '/.openfaces/weights/'
        output = os.path.join(self.model_dir, 'dbface.pth')
        model.load(output)
        return model

    def detect(self, image, threshold=0.4, nms_iou=0.5):
        mean = [0.408, 0.447, 0.47]
        std = [0.289, 0.274, 0.278]

        image = pad(image)
        image = ((image / 255.0 - mean) / std).astype(np.float32)
        image = image.transpose(2, 0, 1)

        torch_image = torch.from_numpy(image)[None]
        if torch.cuda.is_available():
            torch_image = torch_image.to(self.device)

        hm, box, landmark = self.model(torch_image)
        hm_pool = F.max_pool2d(hm, 3, 1, 1)
        scores, indices = ((hm == hm_pool).float() * hm).view(1, -1).cpu().topk(1000)
        hm_height, hm_width = hm.shape[2:]

        scores = scores.squeeze()
        indices = indices.squeeze()
        ys = list((indices // hm_width).int().data.numpy())
        xs = list((indices % hm_width).int().data.numpy())
        scores = list(scores.data.numpy())
        box = box.cpu().squeeze().data.numpy()
        landmark = landmark.cpu().squeeze().data.numpy()

        stride = 4
        rects = []
        for cx, cy, score in zip(xs, ys, scores):
            if score < threshold:
                break
            x, y, r, b = box[:, cy, cx]
            xyrb = (np.array([cx, cy, cx, cy]) + [-x, -y, r, b]) * stride
            x5y5 = landmark[:, cy, cx]
            x5y5 = (exp(x5y5 * 4) + ([cx] * 5 + [cy] * 5)) * stride
            box_landmark = list(zip(x5y5[:5], x5y5[5:]))
            rects.append(BBox(0, xyrb=xyrb, score=score, landmark=box_landmark))

        rects = nms(rects, iou=nms_iou)
        bbox = []
        for rect in rects:
            x, y, r, b = intv(rect.box)
            bbox.append(dict(x1=x, y1=y, x2=r - x + 1, y2=b - y + 1,
                             score=floatv(rect.score),
                             landmark=rect.landmark))
        return bbox


if __name__ == '__main__':
    import cv2
    model = FaceDetector()
    src = cv2.imread("12.jpg")
    result = model.detect(src)
    for r in result:
        cv2.rectangle(src, (r['x1'], r['y1'], r['x2'], r['y2']), (255, 0, 0), 3, 1)
        for i in range(len(r['landmark'])):
            x, y = r['landmark'][i][:2]
            cv2.circle(src, (int(x), int(y)), 3, (0, 0, 255), -1, 16)

    print(result)
    cv2.imwrite("1.png", src)
