from torch.utils.data import Dataset

from models.model import Model


class LR (Model):
    def get_prediction(self, data) -> dict:
        pass

    def fit(self, parameter: dict) -> dict:
        pass

    def load_data(self, dataset: Dataset):
        pass

    def save_model(self, path):
        pass

    def load_model(self, path):
        pass