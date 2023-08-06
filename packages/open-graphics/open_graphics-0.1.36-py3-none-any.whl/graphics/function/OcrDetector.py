import math
import os
from collections import OrderedDict

import cv2
import numpy as np
import torch
import torch.backends.cudnn as cudnn
from torch.autograd import Variable

from ..libs.craft.craft import CRAFT

__all__ = ["OcrDetector"]


def copyStateDict(state_dict):
    if list(state_dict.keys())[0].startswith("module"):
        start_idx = 1
    else:
        start_idx = 0
    new_state_dict = OrderedDict()
    for k, v in state_dict.items():
        name = ".".join(k.split(".")[start_idx:])
        new_state_dict[name] = v
    return new_state_dict


def find_largest_contour(contours):
    max_ind = 0
    max_area = 0
    for ind, c in enumerate(contours):
        if cv2.contourArea(c) > max_area:
            max_area = cv2.contourArea(c)
            max_ind = ind
    return max_ind


class OcrDetector:
    def __init__(self,
                 model_dir="models",
                 text_threshold=0.6,
                 low_text_small=0.4,
                 low_text_huge=0.3,
                 link_threshold=0.4,
                 max_detect_length=1200,
                 min_detect_length=300,
                 ctx_id=-1):
        self.net = CRAFT()  # initialize
        self.device = torch.device("cuda:" + str(ctx_id)) if ctx_id > -1 else torch.device("cpu")
        self.text_threshold = text_threshold
        self.low_text_small = low_text_small
        self.low_text = low_text_small
        self.low_text_huge = low_text_huge
        self.link_threshold = link_threshold
        self.max_detect_length = max_detect_length
        self.min_detect_length = min_detect_length

        model_path = os.path.join(model_dir, "craft_mlt_25k.pth")
        if torch.cuda.is_available():
            print("OCR Use GPU: ", self.device)
            self.net.load_state_dict(copyStateDict(torch.load(model_path)))
            self.net = self.net.to(self.device)
            cudnn.benchmark = False
        else:
            state_dict = torch.load(model_path, map_location=torch.device('cpu'))
            self.net.load_state_dict(copyStateDict(state_dict))
        self.net.eval()

    @staticmethod
    def get_poly(textmap, x1, y1):
        contours, hierarchy = cv2.findContours(textmap, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contour_index = find_largest_contour(contours)
        contour = contours[contour_index]
        epsilon = 0.001 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        approx = np.squeeze(approx)
        return approx

    def get_boxes(self, textmap, linkmap):
        """
        :param textmap: 用于文字检测的map
        :param linkmap: 用于文字之间连接的map
        :return:
        """
        img_h, img_w = textmap.shape
        """ labeling method """
        ret, text_score = cv2.threshold(textmap, self.low_text, 1, 0)
        ret, link_score = cv2.threshold(linkmap, self.link_threshold, 1, 0)
        text_score_comb = np.clip(text_score + link_score, 0, 1)
        ret, text_score_comb = cv2.threshold(text_score_comb, 0, 1, 0)
        nLabels, labels, stats, centroids = cv2.connectedComponentsWithStats(text_score_comb.astype(np.uint8),
                                                                             connectivity=8)
        dets = list()
        ploys = list()
        for k in range(1, nLabels):
            # size filtering
            size = stats[k, cv2.CC_STAT_AREA]
            if size < 10:
                continue
            # thresholding
            if np.max(textmap[labels == k]) < self.text_threshold:
                continue
            # make segmentation map
            segmap = np.zeros(textmap.shape, dtype=np.uint8)
            segmap[labels == k] = 255
            segmap[np.logical_and(link_score == 1, text_score == 0)] = 0  # remove link area
            x, y = stats[k, cv2.CC_STAT_LEFT], stats[k, cv2.CC_STAT_TOP]
            w, h = stats[k, cv2.CC_STAT_WIDTH], stats[k, cv2.CC_STAT_HEIGHT]
            niter = int(math.sqrt(size * min(w, h) / (w * h)) * 2)
            sx, ex, sy, ey = x - niter, x + w + niter + 1, y - niter, y + h + niter + 1
            # boundary check
            if sx < 0:
                sx = 0
            if sy < 0:
                sy = 0
            if ex >= img_w:
                ex = img_w
            if ey >= img_h:
                ey = img_h
            kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1 + niter, 1 + niter))
            segmap[sy:ey, sx:ex] = cv2.dilate(segmap[sy:ey, sx:ex], kernel)
            # make poly
            approx_poly = self.get_poly(segmap[sy:ey, sx:ex], 0, 0)
            approx_poly[:, 0] = approx_poly[:, 0] + sx
            approx_poly[:, 1] = approx_poly[:, 1] + sy
            # make box
            np_contours = np.roll(np.array(np.where(segmap != 0)), 1, axis=0).transpose().reshape(-1, 2)
            rectangle = cv2.minAreaRect(np_contours)
            box = cv2.boxPoints(rectangle)
            # align diamond-shape
            w, h = np.linalg.norm(box[0] - box[1]), np.linalg.norm(box[1] - box[2])
            box_ratio = max(w, h) / (min(w, h) + 1e-5)
            if abs(1 - box_ratio) <= 0.1:
                l, r = min(np_contours[:, 0]), max(np_contours[:, 0])
                t, b = min(np_contours[:, 1]), max(np_contours[:, 1])
                box = np.array([[l, t], [r, t], [r, b], [l, b]], dtype=np.float32)
            # make clock-wise order
            startidx = box.sum(axis=1).argmin()
            box = np.roll(box, 4 - startidx, 0)
            dets.append(box)
            ploys.append(approx_poly)
        ret, text_score = cv2.threshold(textmap, 0.4, 1, 0)
        text_mask = (text_score * 255).astype(np.uint8)
        return dets, text_mask, ploys

    @staticmethod
    def normalize_mean_variance(in_img, mean=(0.485, 0.456, 0.406), variance=(0.229, 0.224, 0.225)):
        # should be RGB order
        img = in_img.copy().astype(np.float32)
        img -= np.array([mean[0] * 255.0, mean[1] * 255.0, mean[2] * 255.0], dtype=np.float32)
        img /= np.array([variance[0] * 255.0, variance[1] * 255.0, variance[2] * 255.0], dtype=np.float32)
        return img

    def crop_image(self, image, h, w):
        """
        crop image by max_detect_length and min_detect_length
        """
        x_step = w // self.max_detect_length + 1
        y_step = h // self.max_detect_length + 1

        roi_list = list()
        for i in range(y_step):
            for j in range(x_step):
                x1 = j * self.max_detect_length
                x2 = (j + 1) * self.max_detect_length
                x2 = w if w - x2 < self.min_detect_length or x2 > w else x2
                y1 = i * self.max_detect_length
                y2 = (i + 1) * self.max_detect_length
                y2 = h if h - y2 < self.min_detect_length or y2 > h else y2
                if y1 == y2 or x1 == x2:
                    break
                roi_list.append(image[y1: y2, x1: x2, :])

        return roi_list, x_step, y_step

    def concat_windows(self, image_list, h, w, x_step, y_step, ratio=2):
        h = h // ratio
        w = w // ratio
        max_detect_length = self.max_detect_length // ratio
        min_detect_length = self.min_detect_length // ratio
        image = np.zeros((h, w), dtype=image_list[0].dtype)
        count = 0
        for i in range(y_step):
            for j in range(x_step):
                x1 = j * max_detect_length
                x2 = (j + 1) * max_detect_length
                x2 = w if w - x2 < min_detect_length or x2 > w else x2
                y1 = i * max_detect_length
                y2 = (i + 1) * max_detect_length
                y2 = h if h - y2 < min_detect_length or y2 > h else y2
                if y1 == y2 or x1 == x2:
                    break
                image[y1: y2, x1: x2] = image_list[count]
                count += 1
        return image

    def detect(self, image_array):
        self.low_text = self.low_text_small
        height, width = image_array.shape[0], image_array.shape[1]
        roi_list, x_step, y_step = self.crop_image(image_array, height, width)
        if len(roi_list) > 1:
            self.low_text = self.low_text_huge
        score_text_list = list()
        score_link_list = list()
        for roi in roi_list:
            x = self.normalize_mean_variance(roi)
            with torch.no_grad():
                x = torch.from_numpy(x).permute(2, 0, 1)  # [h, w, c] to [c, h, w]
                x = Variable(x.unsqueeze(0))  # [c, h, w] to [b, c, h, w]
                if torch.cuda.is_available():
                    x = x.to(self.device)
                y, feature = self.net(x)
            score_text_list.append(y[0, :, :, 0].cpu().data.numpy())
            score_link_list.append(y[0, :, :, 1].cpu().data.numpy())
        score_text = self.concat_windows(score_text_list, height, width, x_step, y_step, ratio=2)
        score_link = self.concat_windows(score_link_list, height, width, x_step, y_step, ratio=2)
        boxes, text_mask, ploys = self.get_boxes(score_text, score_link)
        results = []
        for i, box in enumerate(boxes):
            p1 = (int(box[0, 0] * 2), int(box[0, 1] * 2))
            p2 = (int(box[1, 0] * 2), int(box[1, 1] * 2))
            p3 = (int(box[2, 0] * 2), int(box[2, 1] * 2))
            p4 = (int(box[3, 0] * 2), int(box[3, 1] * 2))
            results.append([p1, p2, p3, p4])
        return results


if __name__ == '__main__':
    import cv2
    import graphics as g

    detector = g.OcrDetector('models')
    image = cv2.imread("720.jpg")
    import time

    s = time.time()
    boxes = detector.detect(image)
    print("time: ", time.time() - s)
    print(boxes)

    for box in boxes:
        cv2.line(image, (box[0][0], box[0][1]), (box[1][0], box[1][1]), color=(0, 255, 0), thickness=2)
        cv2.line(image, (box[1][0], box[1][1]), (box[2][0], box[2][1]), color=(0, 255, 0), thickness=2)
        cv2.line(image, (box[2][0], box[2][1]), (box[3][0], box[3][1]), color=(0, 255, 0), thickness=2)
        cv2.line(image, (box[3][0], box[3][1]), (box[0][0], box[0][1]), color=(0, 255, 0), thickness=2)

    cv2.imwrite("res.png", image)
