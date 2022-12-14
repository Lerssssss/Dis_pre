from models.xgboost import XGBoost
from models.random_forest import RandomForest
from models.kMeans import kMeans
from models.knn import KNN
from models.model import Model
import config
import torch_utils
import os
import difflib


class InferenceService:
    INSTANCE = None

    def __init__(self):
        self.__model = None
        self.__model_name= str()
        self.__result = dict()
        self.__dataset_path = str()

    def __new__(cls, *args, **kwargs):
        print('new inference service create')
        # 判断类属性是否已经被赋值
        if cls.INSTANCE is None:
            cls.INSTANCE = super().__new__(cls)
        # 返回类属性的单例引用
        return cls.INSTANCE

    def train_model(self, model_name, parameter: dict):
        """
        :return: 训练情况(string),训练结果(dict)
        """
        if model_name == config.Models.XGBoost.value:
            self.__model = XGBoost()
            self.__model_name = model_name
        if model_name == config.Models.RandomForest.value:
            self.__model = RandomForest()
            self.__model_name = model_name
        if model_name == config.Models.Kmeans.value:
            self.__model = kMeans()
            self.__model_name = model_name
        if model_name == config.Models.Knn.value:
            self.__model = KNN()
            self.__model_name = model_name
        # 获取数据集
        dataset = torch_utils.get_dataset_from_file(self.__dataset_path)
        # 训练模型
        try:
            self.__model.load_data(dataset)  # TODO
            result = self.__model.fit(parameter)
        except RuntimeError:
            return 'fit error', None
        self.__result = result
        return 'success', result

    def get_result(self):
        """
        :return: 训练结果(dict)
        """
        return self.__result

    def get_prediction(self, data):
        return self.__model.get_prediction(data)

    def get_model_name(self):
        return self.__model_name

    def solve_dataset(self, dataset_path: str):
        try:
            file_list = os.listdir(config.dataPath)
            closest: list = difflib.get_close_matches(dataset_path, file_list, n=1)
            self.__dataset_path = closest[0]
        except IndexError as e:
            raise FileNotFoundError
