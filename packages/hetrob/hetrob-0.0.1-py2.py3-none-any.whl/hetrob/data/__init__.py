import os
import json
import pathlib

from hetrob.data._set import DATASETS
PATH = pathlib.Path(__file__).parent.absolute()


def load_data_set_map(name: str, datasets: dict = DATASETS):
    if name not in datasets:
        raise NotImplementedError("There is no dataset defined with the name '{}'".format(name))

    dataset_map = {}
    for path in datasets[name]:
        instance_name = os.path.basename(path).replace('.json', '')
        dataset_map[instance_name] = path

    return dataset_map


def load_data(name: str):
    file_path = os.path.join(PATH, name)
    with open(file_path, mode='r') as file:
        return json.load(file)


def load_data_raw(path: str):
    with open(path, mode='r') as file:
        return json.load(file)

