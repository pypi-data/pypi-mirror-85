import numpy as np
from mhclovac.sequence import model_distribution


def standardize_index(index: dict) -> dict:
    """
    Standardize values of given index to range [-1 1].
    """
    values = np.array([index[k] for k in index])
    mu = values.mean()
    std = values.std()
    for k, v in index.items():
        index[k] = (v - mu) / std
    return index


def sequence_to_features(sequence: str, index_list: list, sigma: float = 0.4, sampling_points: int = 9) -> list:
    """
    Convert sequence string to list of features.
    """
    sequence_features = []
    for index in index_list:
        features = model_distribution(sequence, index, sigma=sigma, sampling_points=sampling_points)
        sequence_features.extend(features)
    return sequence_features
