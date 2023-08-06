"""
Name : Calculate.py
Author  : Cash
Contact : tkggpdc2007@163.com
Time    : 2020-01-08 10:52
Desc:
"""

import math

import numpy as np
import torch
import torch.nn.functional as F

__all__ = ['euclidean',
           'manhattan',
           'chebyshev',
           'cosine',
           'hanming']


def euclidean(vec1, vec2):
    """
    欧式距离
    :param vec1:
    :param vec2:
    :return: np.linalg.norm(vec1-vec2)
    """

    x, y = np.array(vec1), np.array(vec2)
    return np.sqrt(np.sum(np.square(x - y), axis=1))


def manhattan(vec1, vec2):
    """
    曼哈顿距离
    :param vec1:
    :param vec2:
    :return: np.linalg.norm(vec1-vec2, ord=1)
    """

    x, y = np.array(vec1), np.array(vec2)
    return np.sum(np.abs(x - y), axis=1)


def chebyshev(vec1, vec2):
    """
    切比雪夫距离
    :param vec1:
    :param vec2:
    :return: np.linalg.norm(vec1-vec2, ord=np.inf)
    """

    x, y = np.array(vec1), np.array(vec2)
    return np.max(np.abs(x - y))


def minkowski(vec1, vec2, p=2):
    """
    闵可夫斯基距离
    :param vec1:
    :param vec2:
    :param p:
    :return:
    """

    if p == 1:
        return manhattan(vec1, vec2)
    elif p == 2:
        return euclidean(vec1, vec2)
    else:
        return -1


def mahalanobis(vec1, vec2):
    """
    马氏距离
    :param vec1:
    :param vec2:
    :return:
    """

    x, y = np.array(vec1), np.array(vec2)

    X = np.vstack([x, y])
    XT = X.T
    S = np.cov(X)  # 两个维度之间协方差矩阵
    SI = np.linalg.inv(S)  # 协方差矩阵的逆矩阵
    n = XT.shape[0]
    dist = []
    for i in range(0, n):
        for j in range(i + 1, n):
            delta = XT[i] - XT[j]
            d = np.sqrt(np.dot(np.dot(delta, SI), delta.T))
            dist.append(d)

    return dist


def cosine(vec1, vec2):
    """
    余弦夹角
    :param vec1:
    :param vec2:
    :return:
    """

    x, y = np.array(vec1), np.array(vec2)
    return np.dot(x, y) / (np.linalg.norm(x) * np.linalg.norm(y))


def correlation(vec1, vec2):
    """
    相关系数
    :param vec1:
    :param vec2:
    :return:
    """

    x, y = np.array(vec1), np.array(vec2)
    x_ = x - np.mean(x)
    y_ = y - np.mean(y)
    return np.dot(x_, y_) / (np.linalg.norm(x_) * np.linalg.norm(y_))


def similarity(vec1, vec2):
    """
    杰卡德相似系数
    :param vec1:
    :param vec2:
    :return:
    """

    x, y = np.array(vec1).astype(np.int32), np.array(vec2).astype(np.int32)
    up = np.double(np.bitwise_and((x != y), np.bitwise_or(x != 0, y != 0)).sum())
    down = np.double(np.bitwise_or(x != 0, y != 0).sum())
    return up / down


def brayCurtis(vec1, vec2):
    """
    布雷柯蒂斯距离
    :param vec1:
    :param vec2:
    :return:
    """

    x, y = np.array(vec1), np.array(vec2)
    up = np.sum(np.abs(y - x))
    down = np.sum(x) + np.sum(y)
    return up / down


def hanming(vec1, vec2):
    """
    汉明距离
    :param vec1:
    :param vec2:
    :return:
    """

    sum_str = np.nonzero(vec1 - vec2)
    return np.shape(sum_str[0])[0]


def jaccard(vec1, vec2):
    """
    杰卡德距离
    :param vec1:
    :param vec2:
    :return:
    """

    import scipy.spatial.distance as dist

    matv = np.array([vec1, vec2])
    return dist.pdist(matv, 'jaccard')


def gaussian(x, sigma=10.0):
    """
    计算高斯函数值
    :param x:
    :param sigma:
    :return:
    """
    return np.exp(-x ** 2 / (2 * sigma ** 2))


def svd(a):
    """
    计算奇异值分解
    :param a: 输入矩阵
    :return: U, S, VT = np.linalg.svd(a)
    """
    # 1、计算特征值和特征向量
    S, U = np.linalg.eig(a.dot(a.T))

    # 2、特征值和特征向量进行降序排列
    idx = np.argsort(S)[::-1]
    S = np.sort(S)[::-1]
    U = U[:, idx]

    # 3、计算奇异值矩阵的逆
    S = np.sqrt(S)
    S_inv = np.linalg.inv(np.diag(S))

    # 4、计算右奇异矩阵
    V = S_inv.dot(U.T).dot(a)

    return U, S, V


def pca(x, k):
    """
    数据降维
    from sklearn.decomposition.pca import PCA
    _pca = PCA(n_components=k)
    _pca.fit(x)
    data = _pca.transform(x)
    :param x: 输入数据 mxn
    :param k: 输入维度
    :return: 输出数据
    """
    # 1、计算协方差的奇异值分解
    x -= np.mean(x, axis=0)  # 假设每个特征都具有零均值， 维度为m x n
    cov = x.T.dot(x) / x.shape[0]  # 协方差矩阵：XT * X / m
    U, S, V = np.linalg.svd(cov)  # 对协方差矩阵计算奇异值分解，cov = USV

    # 2、特征值和特征向量进行降序排列
    idx = np.argsort(S)[::-1]
    U = U[:, idx]

    # 3、选取最大的K个特征值所对应的特征向量计算
    return x.dot(U[:, :k])


def pca_whitening(x):
    """
    pca白化
    :param x:
    :return:
    """
    # 1、计算协方差的奇异值分解
    x -= np.mean(x, axis=0)  # 假设每个特征都具有零均值， 维度为m x n
    cov = x.T.dot(x) / x.shape[0]  # 协方差矩阵：X_T * X / m
    U, S, V = np.linalg.svd(cov)  # 对协方差矩阵计算奇异值分解，cov = USV

    xRot = x.dot(U.T)
    xPCAwhite = xRot * (np.diag(1. / np.sqrt(np.diag(S) + 1e-5)))

    return xPCAwhite


def zca_whitening(x):
    """
    zca白化
    :param x:
    :return:
    """
    # 1、计算协方差的奇异值分解
    x -= np.mean(x, axis=0)  # 假设每个特征都具有零均值， 维度为m x n
    cov = x.T.dot(x) / x.shape[0]  # 协方差矩阵：XT * X / m
    U, S, V = np.linalg.svd(cov)  # 对协方差矩阵计算奇异值分解，cov = USV

    xRot = x.dot(U.T)
    xPCAwhite = xRot * (np.diag(1. / np.sqrt(np.diag(S) + 1e-5)))

    return xPCAwhite.dot(U)


class KNN:
    def __init__(self, task_type='classification'):
        self.train_data = None
        self.train_label = None
        self.task_type = task_type

    def fit(self, train_data, train_label):
        self.train_data = np.array(train_data)
        self.train_label = np.array(train_label)

    def predict(self, test_data, k=3, distance='l2'):
        test_data = np.array(test_data)
        preds = []
        for x in test_data:
            # 1、计算距离
            if distance == 'l1':
                dists = manhattan(self.train_data, x)
            elif distance == 'l2':
                dists = euclidean(self.train_data, x)
            else:
                raise ValueError('wrong distance type')
            # 2、对距离升序排序
            sorted_idx = np.argsort(dists)
            knearnest_dists = dists[sorted_idx[:k]]
            knearnest_labels = self.train_label[sorted_idx[:k]]
            pred = None
            if self.task_type == 'regression':
                pred = np.mean(knearnest_labels)
            elif self.task_type == 'classification':
                label_count = {}
                for i in range(k):
                    # 3、选择k个最近邻
                    label = knearnest_labels[i]
                    # 4、计算k个最近邻中各类别出现的次数
                    weight = gaussian(knearnest_dists[i])
                    label_count[label] = label_count.get(label, 0) + weight * 1
                # 5、返回出现次数最多的类别标签
                pred = sorted(label_count.items(), key=label_count.get, reverse=True)[0][0]
            preds.append(pred)

        return preds


def gap(x):
    """
    global average pooling 全局均值池化
    :param x:
    :return:
    """
    return torch.nn.AdaptiveAvgPool2d((1, 1))(x)


def gmp(x):
    """
    global max pooling 全局最大池化
    :param x:
    :return:
    """
    return torch.nn.AdaptiveMaxPool2d((1, 1))(x)


def gem(x, p=3, eps=1e-6):
    """
    generalized-mean pooling
    :param x:
    :param p:
    :param eps:
    :return:
    """
    x = x.clamp(min=eps).pow(p)
    x = F.avg_pool2d(x, (x.size(-2), x.size(-1)))
    return x.pow(1. / p)


def mac(x):
    """
    maximum activations of convolutions
    :param x:
    :return:
    """
    return F.max_pool2d(x, (x.size(-2), x.size(-1)))


def spoc(x):
    """
    sum-pooled convolution
    :param x:
    :return:
    """
    return F.avg_pool2d(x, (x.size(-2), x.size(-1)))


def rmac(x, L=3, eps=1e-6):
    """
    regional maximum activations of convolutions
    :param x:
    :param L:
    :param eps:
    :return:
    """
    ovr = 0.4  # desired overlap of neighboring regions
    steps = torch.Tensor([2, 3, 4, 5, 6, 7])  # possible regions for the long dimension

    W = x.size(3)
    H = x.size(2)

    w = min(W, H)
    w2 = math.floor(w / 2.0 - 1)

    b = (max(H, W) - w) / (steps - 1)
    (tmp, idx) = torch.min(torch.abs(((w ** 2 - w * b) / w ** 2) - ovr), 0)  # steps(idx) regions for long dimension

    # region overplus per dimension
    Wd = 0
    Hd = 0
    if H < W:
        Wd = idx.item() + 1
    elif H > W:
        Hd = idx.item() + 1

    v = F.max_pool2d(x, (x.size(-2), x.size(-1)))
    v = v / (torch.norm(v, p=2, dim=1, keepdim=True) + eps).expand_as(v)

    for l in range(1, L + 1):
        wl = math.floor(2 * w / (l + 1))
        wl2 = math.floor(wl / 2 - 1)

        if l + Wd == 1:
            b = 0
        else:
            b = (W - wl) / (l + Wd - 1)
        cenW = torch.floor(wl2 + torch.Tensor(range(l - 1 + Wd + 1)) * b) - wl2  # center coordinates
        if l + Hd == 1:
            b = 0
        else:
            b = (H - wl) / (l + Hd - 1)
        cenH = torch.floor(wl2 + torch.Tensor(range(l - 1 + Hd + 1)) * b) - wl2  # center coordinates

        for i_ in cenH.tolist():
            for j_ in cenW.tolist():
                if wl == 0:
                    continue
                R = x[:, :, (int(i_) + torch.Tensor(range(wl)).long()).tolist(), :]
                R = R[:, :, :, (int(j_) + torch.Tensor(range(wl)).long()).tolist()]
                vt = F.max_pool2d(R, (R.size(-2), R.size(-1)))
                vt = vt / (torch.norm(vt, p=2, dim=1, keepdim=True) + eps).expand_as(vt)
                v += vt

    return v


def roipool(x, rpool, L=3, eps=1e-6):
    ovr = 0.4  # desired overlap of neighboring regions
    steps = torch.Tensor([2, 3, 4, 5, 6, 7])  # possible regions for the long dimension

    W = x.size(3)
    H = x.size(2)

    w = min(W, H)
    w2 = math.floor(w / 2.0 - 1)

    b = (max(H, W) - w) / (steps - 1)
    _, idx = torch.min(torch.abs(((w ** 2 - w * b) / w ** 2) - ovr), 0)  # steps(idx) regions for long dimension

    # region overplus per dimension
    Wd = 0
    Hd = 0
    if H < W:
        Wd = idx.item() + 1
    elif H > W:
        Hd = idx.item() + 1

    vecs = []
    vecs.append(rpool(x).unsqueeze(1))

    for l in range(1, L + 1):
        wl = math.floor(2 * w / (l + 1))
        wl2 = math.floor(wl / 2 - 1)

        if l + Wd == 1:
            b = 0
        else:
            b = (W - wl) / (l + Wd - 1)
        cenW = torch.floor(wl2 + torch.Tensor(range(l - 1 + Wd + 1)) * b).int() - wl2  # center coordinates
        if l + Hd == 1:
            b = 0
        else:
            b = (H - wl) / (l + Hd - 1)
        cenH = torch.floor(wl2 + torch.Tensor(range(l - 1 + Hd + 1)) * b).int() - wl2  # center coordinates

        for i_ in cenH.tolist():
            for j_ in cenW.tolist():
                if wl == 0:
                    continue
                vecs.append(rpool(x.narrow(2, i_, wl).narrow(3, j_, wl)).unsqueeze(1))

    return torch.cat(vecs, dim=1)


def l2n(x, eps=1e-6):
    return x / (torch.norm(x, p=2, dim=1, keepdim=True) + eps).expand_as(x)


def powerlaw(x, eps=1e-6):
    x = x + eps
    return x.abs().sqrt().mul(x.sign())


def compute_spatial_weight(x, a=2, b=2):
    """
    Given a tensor of features, compute spatial weights as normalized total activation.
    Normalization parameters default to values determined experimentally to be most effective.
    :param ndarray x:
        3d tensor of activations with dimensions (channels, height, width)
    :param int a:
        the p-norm
    :param int b:
        power normalization
    :returns ndarray:
        a spatial weight matrix of size (height, width)
    """
    if len(x.shape) > 3:
        return x
    s = x.sum(dim=0)  # channel-wise sum (height, width)
    z = (s ** a).sum() ** (1. / a)  # value
    return (s / z) ** (1. / b) if b != 1 else (s / z)  # (height, width)


def compute_channel_weight(x):
    """
    Given a tensor of features, compute channel weights as the log of inverse channel sparsity.
    :param ndarray x:
        3d tensor of activations with dimensions (channels, height, width)
    :returns ndarray:
        a channel weight vector
    """
    if len(x.shape) > 3:
        return x
    c, w, h = x.shape
    area = float(w * h)
    nonzeros = np.zeros(c, dtype=np.float32)
    for i, k in enumerate(x):
        nonzeros[i] = np.count_nonzero(k) / area

    nzsum = nonzeros.sum()
    for i, q in enumerate(nonzeros):
        nonzeros[i] = np.log(nzsum / q) if q > 0. else 0.

    return nonzeros


def crow(x):
    """
    Given a tensor of activations, compute the aggregate CroW feature, weighted
    spatially and channel-wise.
    :param ndarray x:
        3d tensor of activations with dimensions (channels, height, width)
    :returns ndarray:
        CroW aggregated global image feature
    """
    if len(x.shape) > 3:
        return x
    S = compute_spatial_weight(x)  # (height, width)
    C = compute_channel_weight(x)  # (channel weight vector)
    x = x * S
    x = x.sum(dim=(1, 2))
    return x * torch.from_numpy(C)
