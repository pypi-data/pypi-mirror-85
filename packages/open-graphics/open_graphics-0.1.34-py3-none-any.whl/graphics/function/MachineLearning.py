import os
import joblib


__all__ = ['LogisticRegressionModel',
           'SGDClassifierModel',
           'LinearSVCModel',
           'MultinomialNBModel',
           'KNeighborsClassifierModel',
           'DecisionTreeClassifierModel',
           'RandomForestClassifierModel',
           'GradientBoostingClassifierModel',
           'LinearRegressionModel',
           'SGDRegressorModel',
           'LogisticRegressionModel',
           'SGDClassifierModel',
           'LinearSVCModel',
           'MultinomialNBModel',
           'KNeighborsClassifierModel',
           'SVRModel',
           'KNeighborsRegressorModel',
           'DecisionTreeRegressorModel',
           'RandomForestRegressorModel',
           'ExtraTreesRegressorModel',
           'GradientBoostingRegressorModel',
           'train_test_split']


class Model:
    model = None
    vectorizer = False  # 是否向量化（将类别型特征转为特征向量）
    normalizer = True  # 是否标准化（将特征数据进行标准化）
    regression = False  # 是否为回归模型（分类模型/回归模型）

    def __init__(self):
        from sklearn.feature_extraction import DictVectorizer
        from sklearn.preprocessing import StandardScaler
        self.vec = DictVectorizer(sparse=False)
        self.sx = StandardScaler()
        self.sy = StandardScaler()

    def fit(self, x_train, y_train):
        """
        模型拟合
        :param x_train: 训练数据
        :param y_train: 训练标签
        # :param vectorizer: 是否向量化（将类别型特征转为特征向量）
        # :param normalizer: 是否标准化（将特征数据进行标准化）
        :return:
        """
        x_train = self.vec.fit_transform(x_train.to_dict(orient='record')) if self.vectorizer else x_train
        x_train = self.sx.fit_transform(x_train) if self.normalizer else x_train
        y_train = self.sy.fit_transform(y_train.reshape(-1, 1)).reshape(-1,) if self.normalizer else y_train

        self.model.fit(x_train, y_train)

    def predict(self, x_test):
        """
        模型预测
        :param x_test:
        :return:
        """
        x_test = self.vec.transform(x_test.to_dict(orient='record')) if self.vectorizer else x_test
        x_test = self.sx.transform(x_test) if self.normalizer else x_test
        return self.model.predict(x_test)

    def evaluate(self, x_test, y_test):
        x_test = self.vec.transform(x_test.to_dict(orient='record')) if self.vectorizer else x_test
        x_test = self.sx.transform(x_test) if self.normalizer else x_test
        y_test = self.sy.transform(y_test.reshape(-1, 1)).reshape(-1,) if self.normalizer else y_test
        if not self.regression:
            return self.model.score(x_test, y_test)
        else:
            from sklearn.metrics import r2_score, mean_squared_error, mean_absolute_error
            y_predict = self.model.predict(x_test)
            r2 = r2_score(y_test, y_predict)
            mse = mean_squared_error(self.sy.inverse_transform(y_test) if self.normalizer else y_test,
                                     self.sy.inverse_transform(y_predict) if self.normalizer else y_predict)
            mae = mean_absolute_error(self.sy.inverse_transform(y_test) if self.normalizer else y_test,
                                      self.sy.inverse_transform(y_predict) if self.normalizer else y_predict)
            return r2, mse, mae

    def save(self, model_dir=None):
        if model_dir is not None:
            os.makedirs(model_dir, exist_ok=True)
            model_path = os.path.join(model_dir, 'model.pkl')
            joblib.dump(self.model, model_path)


class LogisticRegressionModel(Model):
    """
    逻辑回归分类器
    """

    def __init__(self):
        super(LogisticRegressionModel, self).__init__()
        from sklearn.linear_model import LogisticRegression
        self.model = LogisticRegression()


class SGDClassifierModel(Model):
    """
    随机梯度分类器
    """

    def __init__(self):
        super(SGDClassifierModel, self).__init__()
        from sklearn.linear_model import SGDClassifier
        self.model = SGDClassifier()


class LinearSVCModel(Model):
    """
    支持向量机分类器
    """

    def __init__(self):
        super(LinearSVCModel, self).__init__()
        from sklearn.svm import LinearSVC
        self.model = LinearSVC()


class MultinomialNBModel(Model):
    """
    朴素贝叶斯分类器
    """

    def __init__(self):
        super(MultinomialNBModel, self).__init__()
        from sklearn.naive_bayes import MultinomialNB
        self.model = MultinomialNB()


class KNeighborsClassifierModel(Model):
    """
    K近邻分类器
    """

    def __init__(self):
        super(KNeighborsClassifierModel, self).__init__()
        from sklearn.neighbors import KNeighborsClassifier
        self.model = KNeighborsClassifier()


class DecisionTreeClassifierModel(Model):
    """
    决策树分类器
    """

    def __init__(self):
        super(DecisionTreeClassifierModel, self).__init__()
        from sklearn.tree import DecisionTreeClassifier
        self.model = DecisionTreeClassifier()


class RandomForestClassifierModel(Model):
    """
    随机森林分类器
    """

    def __init__(self):
        super(RandomForestClassifierModel, self).__init__()
        from sklearn.ensemble import RandomForestClassifier
        self.model = RandomForestClassifier()


class GradientBoostingClassifierModel(Model):
    """
    随机森林分类器
    """

    def __init__(self):
        super(GradientBoostingClassifierModel, self).__init__()
        from sklearn.ensemble import GradientBoostingClassifier
        self.model = GradientBoostingClassifier()


class LinearRegressionModel(Model):
    """
    线性回归器预测
    """

    def __init__(self):
        super(LinearRegressionModel, self).__init__()
        from sklearn.linear_model import LinearRegression
        self.model = LinearRegression()


class SGDRegressorModel(Model):
    """
    线性回归器预测
    """

    def __init__(self):
        super(SGDRegressorModel, self).__init__()
        from sklearn.linear_model import SGDRegressor
        self.model = SGDRegressor()


class SVRModel(Model):
    """
    支持向量机回归：（预测方式）
    'linear' 线性核函数
    'poly' 多项式核函数
    'rbf' 径向基核函数
    """

    def __init__(self, kernel=None):
        super(SVRModel, self).__init__()
        from sklearn.svm import SVR
        self.model = SVR(kernel='linear' if kernel is None else kernel)


class KNeighborsRegressorModel(Model):
    """
    K近邻回归器：（预测方式）
    'uniform' 平均回归
    'distance' 距离加权回归
    """

    def __init__(self, weights=None):
        super(KNeighborsRegressorModel, self).__init__()
        from sklearn.neighbors import KNeighborsRegressor
        self.model = KNeighborsRegressor(weights='uniform' if weights is None else weights)


class DecisionTreeRegressorModel(Model):
    """
    回归树预测
    """

    def __init__(self):
        super(DecisionTreeRegressorModel, self).__init__()
        from sklearn.tree import DecisionTreeRegressor
        self.model = DecisionTreeRegressor()


class RandomForestRegressorModel(Model):
    """
    集成回归模型预测
    """

    def __init__(self):
        super(RandomForestRegressorModel, self).__init__()
        from sklearn.ensemble import RandomForestRegressor
        self.model = RandomForestRegressor()


class ExtraTreesRegressorModel(Model):
    """
    集成回归模型预测
    """

    def __init__(self):
        super(ExtraTreesRegressorModel, self).__init__()
        from sklearn.ensemble import ExtraTreesRegressor
        self.model = ExtraTreesRegressor()


class GradientBoostingRegressorModel(Model):
    """
    集成回归模型预测
    """

    def __init__(self):
        super(GradientBoostingRegressorModel, self).__init__()
        from sklearn.ensemble import GradientBoostingRegressor
        self.model = GradientBoostingRegressor()


def train_test_split(data, label):
    from sklearn.model_selection import train_test_split
    x_train, x_test, y_train, y_test = train_test_split(data, label, test_size=0.25, random_state=33)
    return x_train, x_test, y_train, y_test


# class ModelInfo:
#     rmse = 0
#     pipeline = None
#
#     def __init__(self, model_cls, model_kwargs={}):
#         self.model_cls = model_cls
#         self.model_kwargs = model_kwargs
#         self.model_name = self.model_cls.__name__
#         self.model_dir = os.path.join(base_model_dir, self.model_name)
#         os.makedirs(self.model_dir, exist_ok=True)
#         self.model_instance = self.model_cls(**self.model_kwargs)
#
#     def dump(self):
#         model_path = os.path.join(self.model_dir, 'model.pkl')
#         score_path = os.path.join(self.model_dir, 'score.txt')
#         joblib.dump((self.pipeline, self.model_instance), model_path)
#         with open(score_path, 'w') as f:
#             f.write(str(self.rmse))
#
#
# model_info_list = [
#     ModelInfo(LinearRegressionModel),
#     ModelInfo(DecisionTreeRegressor),
#     ModelInfo(RandomForestRegressor),
#     ModelInfo(SVR),
#     ModelInfo(GradientBoostingRegressor)
# ]
#
#
# def load_model_by_name(model_name):
#     model_file_path = os.path.join(base_model_dir, model_name, "model.pkl")
#     model_info_path = os.path.join(base_model_dir, model_name, "score.txt")
#     pipeline, model = joblib.load(model_file_path)
#     with open(model_info_path, 'r') as f:
#         score = f.read()
#     return pipeline, model, score
