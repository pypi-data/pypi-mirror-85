import os
import shutil

import cv2
import numpy as np
import requests
from tqdm import tqdm
from skimage import filters
from .Format import get_file_md5
from .Graphics import resize
from ..common.logs import logs

__all__ = ["delete_file",
           "extract_frames",
           "blur_detect",
           "download"]


def delete_file(src, dst="../"):
    all_md5 = {}
    dirs = os.listdir(src)
    if ".DS_Store" in dirs:
        dirs.remove(".DS_Store")
    for p in dirs:
        md5 = get_file_md5(os.path.join(src, p))
        if md5 in all_md5.values():
            shutil.move(os.path.join(src, p), os.path.join(dst, p))
            logs.info(os.path.join(src, p))
        else:
            all_md5[p] = md5


def blur_detect(img):
    """
    清晰度检测
    Args:
        img: 输入图片（BGR）
    Returns:
        清晰度分数
    """
    tmp, _ = resize(img, interpolation=cv2.INTER_CUBIC)
    tmp = cv2.cvtColor(tmp, cv2.COLOR_BGR2GRAY)
    tmp = filters.sobel(np.matrix(tmp) / 255.0)
    score = np.sqrt(np.sum(tmp ** 2))

    return score


def extract_frames(path, threshold=0.6, clarity=30.0):
    """
    提取视频关键帧
    :param path: the video path
    :param threshold: the threshold of two frames`s pixel diff
    :param clarity: the min score of the current frame's clarity
    :return: [frame for (idx, frame) in key_frames.items()]
    """

    def rel_change(a, b):
        x = abs(b - a) / max(a, b) if max(a, b) != 0 else 0
        return x

    idx, prev_diff, key_frames, prev_frame = 0, -1, {}, None
    try:
        video_capture = cv2.VideoCapture(path)
        success, frame = video_capture.read()
        key_frames[idx] = frame[:, :, ::-1]
        idx += 1
        while success:
            curr_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2LUV)
            if curr_frame is not None and prev_frame is not None:
                curr_diff = np.sum(cv2.absdiff(curr_frame, prev_frame))
                if prev_diff != -1:
                    diff = rel_change(np.float(prev_diff), np.float(curr_diff))
                    if diff > threshold and blur_detect(frame) > clarity:
                        key_frames[idx] = frame[:, :, ::-1]
                prev_diff = curr_diff
            idx += 1
            prev_frame = curr_frame
            success, frame = video_capture.read()
        video_capture.release()
        return key_frames
    except:
        return []


def download(url, path=None, overwrite=False):
    """
    下载文件
    Args:
        url: 下载的文件地址
        path: 文件保存路径，默认保存在当前文件夹
        overwrite: 如果文件存在，是否覆盖原文件
    Returns: 下载的文件路径
    """
    try:
        if path is None:
            file_name = url.split('/')[-1]
        else:
            path = os.path.expanduser(path)
            if os.path.isdir(path):
                if len(os.path.splitext(url.split('/')[-1])[-1]):
                    file_name = os.path.join(path, url.split('/')[-1])
                else:
                    file_name = os.path.join(path, url.split('/')[-1] + '.jpg')
            else:
                file_name = path

        if overwrite or not os.path.exists(file_name):
            dir_name = os.path.dirname(os.path.abspath(os.path.expanduser(file_name)))
            if not os.path.exists(dir_name):
                os.makedirs(dir_name)
            print('Downloading %s from %s' % (file_name, url))
            r = requests.get(url, stream=True)
            if r.status_code != 200:
                return None
            total_length = r.headers.get('content-length')
            with open(file_name, 'wb') as f:
                if total_length is None:  # no content length header
                    for chunk in r.iter_content(chunk_size=1024):
                        if chunk:  # filter out keep-alive new chunks
                            f.write(chunk)
                else:
                    total_length = int(total_length)
                    for chunk in tqdm(r.iter_content(chunk_size=1024),
                                      total=int(total_length / 1024. + 0.5),
                                      unit='KB', unit_scale=False, dynamic_ncols=True):
                        f.write(chunk)
        return file_name
    except:
        return None
