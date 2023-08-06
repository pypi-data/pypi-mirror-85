import os

import cv2
import numpy as np

__all__ = ['compute_mae',
           'compute_pr',
           'batch_compute_mae',
           'batch_compute_measure',
           'batch_compute_iou']


# 计算MAE
def compute_mae(mask1, mask2):
    """
    计算MAE
    :param mask1: HxW or HxWxC
    :param mask2: HxW or HxWxC
    :return: a value MAE, Mean Absolute Error
    """
    h, w = mask1.shape[0], mask1.shape[1]
    mask1 = mask1 / (np.amax(mask1) + 1e-8)
    mask2 = mask2 / (np.amax(mask2) + 1e-8)
    _mae = np.sum(np.absolute((mask1.astype(float) - mask2.astype(float))))

    return _mae / (float(h) * float(w) + 1e-8)


# 计算PR
def compute_pr(mask, gt):
    """
    计算PR
    :param mask: (W, H)
    :param gt: (W, H)
    :return: precision, recall
    """
    FP = sum(sum(mask - gt == 255))  # 将负类预测为正类数误报
    FN = sum(sum(gt - mask == 255))  # 将正类预测为负类数漏报
    TP = sum(sum((mask == gt) & (gt == 255)))  # 将正类预测为正类数
    precision = TP / (TP + FP + 1e-8)
    recall = TP / (TP + FN + 1e-8)

    return precision, recall


# 计算MAE评价指标
def batch_compute_mae(mask_path, gt_path):
    dirs = os.listdir(mask_path)
    if ".DS_Store" in dirs:
        dirs.remove(".DS_Store")
    sum_mae = 0.0
    count = 0
    for p in dirs:
        print("path: ", p)
        mask = cv2.imread(mask_path + p, cv2.IMREAD_UNCHANGED)
        gt = cv2.imread(gt_path + os.path.splitext(p)[0] + ".png", cv2.IMREAD_UNCHANGED)
        tmp_mae = compute_mae(mask, gt)
        print("mae: ", tmp_mae)
        sum_mae += tmp_mae
        count += 1
    return sum_mae / (count + 1e-8)


# 计算P/R/F-measure评价指标
def batch_compute_measure(mask_path, gt_path, beta=0.3):
    """
    计算PRE/REC/FM
    :param mask_path: mask name list
    :param gt_path: ground truth name list
    :param beta: 0.3
    :return: precision, recall, F-measure (beta)
    """
    dirs = os.listdir(mask_path)
    if ".DS_Store" in dirs:
        dirs.remove(".DS_Store")
    precision = [0 for _ in range(len(dirs))]
    recall = [0 for _ in range(len(dirs))]
    for i, p in enumerate(dirs):
        mask = cv2.imread(mask_path + p, cv2.IMREAD_UNCHANGED)
        _, mask = cv2.threshold(mask, 125, 255, cv2.THRESH_BINARY)

        gt = cv2.imread(gt_path + os.path.splitext(p)[0] + ".png", cv2.IMREAD_UNCHANGED)
        _, gt = cv2.threshold(gt, 125, 255, cv2.THRESH_BINARY)

        p, r = compute_pr(mask, gt)
        precision[i] = p
        recall[i] = r

    precision = sum(precision) / len(precision)
    recall = sum(recall) / len(recall)
    f_measure = ((1 + beta) * precision * recall) / (beta * precision + recall)

    return precision, recall, f_measure


# 计算IOU评价指标
def batch_compute_iou(mask_path, gt_path):
    """
    计算IOU
    :param mask_path: mask name list
    :param gt_path: ground truth name list
    :return: IOU
    """
    dirs = os.listdir(mask_path)
    if ".DS_Store" in dirs:
        dirs.remove(".DS_Store")
    iou = []
    for i, p in enumerate(dirs):
        mask = cv2.imread(mask_path + p, cv2.IMREAD_UNCHANGED)
        _, mask = cv2.threshold(mask, 125, 255, cv2.THRESH_BINARY)

        gt = cv2.imread(gt_path + os.path.splitext(p)[0] + ".png", cv2.IMREAD_UNCHANGED)
        _, gt = cv2.threshold(gt, 125, 255, cv2.THRESH_BINARY)

        iou_and = sum(sum((mask == 255) & (gt == 255)))
        iou_or = sum(sum(mask == 255)) + sum(sum(gt == 255)) - iou_and
        iou.append(iou_and / iou_or)

    return sum(iou) / (len(iou) + 1e-8)
