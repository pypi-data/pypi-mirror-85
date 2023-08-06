import os
import warnings

import cv2
import numpy as np
import pandas as pd
import tensorflow as tf
import tensorflow_hub as hub
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MultiLabelBinarizer
from tensorflow.keras import layers

from ..common.utils import print_time, learning_curves

__all__ = ['MultiLabelClassify']
warnings.filterwarnings('ignore')


def parse_function(filename, label):
    """Function that returns a tuple of normalized image array and labels array.
    Args:
        filename: string representing path to image
        label: 0/1 one-dimensional array of size N_LABELS
    """
    image_string = tf.io.read_file(filename)
    image_decoded = tf.image.decode_jpeg(image_string, channels=3)
    image_resized = tf.image.resize(image_decoded, [224, 224])
    image_normalized = image_resized / 255.0
    return image_normalized, label


def create_dataset(filenames, labels, batch_size=256, is_training=True):
    """Load and parse dataset.
    Args:
        filenames: list of image paths
        labels: numpy array of shape (BATCH_SIZE, N_LABELS)
        batch_size:
        is_training: boolean to indicate training mode
    """
    dataset = tf.data.Dataset.from_tensor_slices((filenames, labels))
    # AUTOTUNE 将使预处理和预取工作负载适应模型训练和批量消耗
    dataset = dataset.map(parse_function, num_parallel_calls=tf.data.experimental.AUTOTUNE)
    # if is_training:
    #     dataset = dataset.cache()
    #     dataset = dataset.shuffle(buffer_size=1024)
    dataset = dataset.batch(batch_size)
    dataset = dataset.prefetch(buffer_size=tf.data.experimental.AUTOTUNE)
    return dataset


@tf.function
def macro_soft_f1(y, y_hat):
    """Compute the macro soft F1-score as a cost (average 1 - soft-F1 across all labels).
    Use probability values instead of binary predictions.

    Args:
        y (int32 Tensor): targets array of shape (BATCH_SIZE, N_LABELS)
        y_hat (float32 Tensor): probability matrix from forward propagation of shape (BATCH_SIZE, N_LABELS)

    Returns:
        cost (scalar Tensor): value of the cost function for the batch
    """
    y = tf.cast(y, tf.float32)
    y_hat = tf.cast(y_hat, tf.float32)
    tp = tf.reduce_sum(y_hat * y, axis=0)
    fp = tf.reduce_sum(y_hat * (1 - y), axis=0)
    fn = tf.reduce_sum((1 - y_hat) * y, axis=0)
    soft_f1 = 2 * tp / (2 * tp + fn + fp + 1e-16)
    cost = 1 - soft_f1  # reduce 1 - soft-f1 in order to increase soft-f1
    macro_cost = tf.reduce_mean(cost)  # average on all labels
    return macro_cost


@tf.function
def macro_f1(y, y_hat, thresh=0.5):
    """Compute the macro F1-score on a batch of observations (average F1 across labels)
    Args:
        y (int32 Tensor): labels array of shape (BATCH_SIZE, N_LABELS)
        y_hat (float32 Tensor): probability matrix from forward propagation of shape (BATCH_SIZE, N_LABELS)
        thresh: probability value above which we predict positive

    Returns:
        macro_f1 (scalar Tensor): value of macro F1 for the batch
    """
    y_pred = tf.cast(tf.greater(y_hat, thresh), tf.float32)
    tp = tf.cast(tf.math.count_nonzero(y_pred * y, axis=0), tf.float32)
    fp = tf.cast(tf.math.count_nonzero(y_pred * (1 - y), axis=0), tf.float32)
    fn = tf.cast(tf.math.count_nonzero((1 - y_pred) * y, axis=0), tf.float32)
    f1 = 2 * tp / (2 * tp + fn + fp + 1e-16)
    macro_f1 = tf.reduce_mean(f1)
    return macro_f1


class MultiLabelClassify:
    """
        todo: 1、修改网络backbone为resnet50 2、修改loss函数 3、修改metrics后能正常加载模型
    """

    def __init__(self, model_dir="models/", num_classes=-1, pretrained=True):
        """
        图像分类
        :param model_dir: 模型路径
        :param num_classes: 指定训练类别数
        :param pretrained: 指定预训练是否开启
        """
        self.num_classes = num_classes
        self.model = self.load_model(model_dir, pretrained)

    def load_model(self, model_path, pretrained=True):
        if pretrained:
            features = hub.KerasLayer(model_path, input_shape=(224, 224, 3))
            features.trainable = False
            model = tf.keras.Sequential([
                features,
                layers.Dense(self.num_classes, activation='sigmoid')
            ])
        else:
            model = tf.keras.models.load_model(model_path)
        model.summary()
        return model

    def predict(self, image):
        """
        图像预测
        :param image: 输入图像（numpy data）
        :return: 分类类别
        """
        img = cv2.resize(image, (224, 224))
        img = img / 255
        img = np.expand_dims(img, axis=0)
        prediction = (self.model.predict(img) > 0.5).astype('int')
        prediction = pd.Series(prediction[0])
        prediction = prediction[prediction == 1].index.values
        return [int(r) for r in list(prediction)]

    def load_data(self, data_dir, batch_size):
        movies = pd.read_csv(os.path.join(data_dir, "movies_new.csv"))
        X_train, X_val, y_train, y_val = train_test_split(movies['imdbId'], movies['Genre'], test_size=0.2,
                                                          random_state=44)
        X_train = [os.path.join(data_dir, 'images', str(f) + '.jpg') for f in X_train]
        X_val = [os.path.join(data_dir, 'images', str(f) + '.jpg') for f in X_val]
        y_train = [eval(s) for s in y_train]
        y_val = [eval(s) for s in y_val]

        mlb = MultiLabelBinarizer()
        mlb.fit(y_train)
        self.num_classes = len(mlb.classes_)
        for (i, label) in enumerate(mlb.classes_):
            print("{}. {}".format(i, label))

        y_train_bin = mlb.transform(y_train)
        y_val_bin = mlb.transform(y_val)

        train_ds = create_dataset(X_train, y_train_bin, batch_size)
        val_ds = create_dataset(X_val, y_val_bin, batch_size)
        return train_ds, val_ds

    def train(self, data_path="datasets", batch_size=256, num_epochs=50, lr=5e-4):
        train_ds, val_ds = self.load_data(data_path, batch_size)
        import time
        self.model.compile(optimizer=tf.keras.optimizers.Adam(learning_rate=lr),
                           loss=tf.keras.metrics.binary_crossentropy,
                           metrics=['accuracy'])

        start = time.time()
        history = self.model.fit(train_ds,
                                 epochs=num_epochs,
                                 validation_data=val_ds)
        print('\nTraining {}'.format(print_time(time.time() - start)))

        losses, val_losses, accuracy, val_accuracy = learning_curves(history)

        print("Macro soft-F1 loss: %.2f" % val_losses[-1])
        print("Macro F1-score: %.2f" % val_accuracy[-1])
        export_path = os.path.join("models", "resnet_v2")
        self.model.save(export_path)
        return


if __name__ == '__main__':
    import graphics as g

    cl = g.MultiLabelClassify("datasets/mobilenet_v2",
                              num_classes=23,
                              pretrained=False)
    cl.train("datasets")
    image = cv2.imread("12304.jpg")[:, :, ::-1]
    res = cl.predict(image)
    print(res)
