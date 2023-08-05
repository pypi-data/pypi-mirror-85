"""
A module containing functionality related to the encapsulation of all sorts of results. This includes for example the
results of a single algorithm execution like `AlgorithmResults`, but also the execution of a whole bunch of
algorithms like `ExperimentResults`.
"""
# This line is important to fix the way type annotations will work. More specifically this line is required to be able
# to use the class name of a class as a type annotation within one of its own methods! Without this use a string instead
from __future__ import annotations
import json
import shelve
import os
import re
import collections.abc
from typing import List, Tuple, Type, Dict
from typing import List, Tuple, Type, Dict
from pprint import pprint

import numpy as np

from hetrob.problem import AbstractProblem
from hetrob.solution import AbstractSolution
from hetrob.util import AbstractTerminationCondition, JsonMixin, dump_json, load_json


# SINGLE EXECUTION
# ================

class AlgorithmResult(JsonMixin):
    """
    A class representing the output of a single execution of an algorithm.

    Implements the `JsonMixin`. Implementing this mixin enables a custom json encoding of the object.
    """
    def __init__(self,
                 problem: AbstractProblem,
                 solution: AbstractSolution,
                 termination: AbstractTerminationCondition,
                 logbook: dict,
                 fitness: float,
                 time: float,
                 iterations: float,
                 feasible: bool):
        """
        The constructor.

        :param problem:
        :param solution:
        :param termination:
        :param logbook:
        :param fitness:
        :param time:
        :param iterations:
        :param feasible:
        """
        JsonMixin.__init__(self)

        self.problem = problem
        self.solution = solution
        self.termination = termination
        self.logbook = logbook
        self.fitness = fitness
        self.time = time
        self.iterations = iterations
        self.feasible = feasible

    # IMPLEMENT "JsonMixin"
    # ---------------------

    def to_dict(self) -> dict:
        """
        Returns the dictionary representation of the object.

        :return: Dict representation of the object
        :rtype: dict
        """
        return {
            'problem':          self.problem,
            'solution':         self.solution,
            'termination':      self.termination,
            'logbook':          self.logbook,
            'fitness':          self.fitness,
            'time':             self.time,
            'iterations':       self.iterations,
            'feasible':         self.feasible
        }

    @classmethod
    def from_dict(cls, data: dict) -> AlgorithmResult:
        """
        Recreates the object from a given dictionary.

        :param data: The dictionary containing the attribute values for an object of this class.
        :return:
        """
        return cls(
            problem=data['problem'],
            solution=data['solution'],
            termination=data['termination'],
            logbook=data['logbook'],
            fitness=data['fitness'],
            time=data['time'],
            iterations=data['iterations'],
            feasible=data['feasible']
        )

    def get_import(self) -> Tuple[str, str]:
        """
        Returns a tuple, which contains the full information for dynamically importing this class.
        Refer to `JsonMixin` for details.

        :return:
        :rtype: Tuple[str, str]
        """
        return 'hetrob.result', 'AlgorithmResult'


# MULTIPLE EXECUTIONS
# ===================

class TestResults:

    def __init__(self, file_path: str, writeback: bool = True):
        self.file_path = file_path
        self.shelf = shelve.open(self.file_path, writeback=writeback)

        if 'data' not in self.shelf.keys():
            self.shelf['data'] = {}
            self.shelf['additional'] = {}
            self.shelf['statistics'] = {}

    def register_algorithm(self, key: str, description: str = ''):
        self.shelf['data'][key] = {
            'name':         key,
            'description':  description,
            'instances':    {}
        }

    def add_instance(self, key: str, name: str, description: str = ''):
        self.shelf['data'][key]['instances'][name] = {
            'name':         name,
            'description':  description,
            'runs':         []
        }

    def add_run(self, key: str, instance: str, run: dict, fix_imports=None):
        """
        Result:
        - fitness
        - solution
        - logbook
        - problem
        """
        self.shelf['data'][key]['instances'][instance]['runs'].append(run)
        self.shelf.sync()

    def add_runs(self, key: str, instance: str, runs: List[dict]):
        for run in runs:
            self.add_run(key, instance, run)

    def calculate_statistics(self):

        for key, item in self.shelf['data'].items():
            self.shelf['statistics'][key] = {}
            for instance_name, instance in item['instances'].items():
                fitnesses = [run['fitness'] for run in instance['runs']]

                self.shelf['statistics'][key][instance_name] = {
                    'min':              np.min(fitnesses),
                    'max':              np.max(fitnesses),
                    'mean':             np.mean(fitnesses),
                    'std':              np.std(fitnesses)
                }

    def close(self):
        self.shelf.close()

    def to_json(self) -> str:
        return json.dumps(self.__dict__, indent=4, sort_keys=True)

    def save(self, file_path: str):
        json_string = self.to_json()
        with open(file_path, mode='w+') as file:
            file.write(json_string)

    @classmethod
    def from_dict(cls, data: dict):
        obj = cls()

        obj.data = data['data']
        obj.statistics = data['statistics']
        obj.additional = data['additional']

        return obj

    @classmethod
    def from_json(cls, json_string: str):
        data = json.loads(json_string)
        return cls.from_dict(data)

    @classmethod
    def load(cls, file_path: str):
        with open(file_path, mode='r') as file:
            return cls.from_json(file.read())


class AbstractResultBatching(object):

    def __init__(self, folder_path: str):
        self.folder_path = folder_path

    @classmethod
    def split_query(cls, query: str) -> list:
        split = query.split('/')
        return split

    @classmethod
    def init_query(cls, data: dict, query: str) -> dict:
        keys = cls.split_query(query)

        current = data
        for key in keys:
            if key not in current.keys():
                current[key] = {}
            current = current[key]

        return data

    def __enter__(self):
        self.open()
        return self

    def __exit__(self, *exc_details):
        self.close()

    # TO BE IMPLEMENTED
    # -----------------

    def save(self, query: str, algorithm_result: AlgorithmResult):
        raise NotImplementedError()

    def load(self, query: str):
        """

        .. note::

            One special case that has to be taken care of when implementing this method is an empty string query. If
            an empty string is passed as a query, this is supposed to return the whole data, which would be the root
            dictionary.

        :param query:
        :return:
        """
        raise NotImplementedError()

    def get_algorithm_keys(self):
        raise NotImplementedError()

    def open(self):
        raise NotImplementedError()

    def close(self):
        raise NotImplementedError()


class QueryCachingMixin(object):

    QUERY_CACHE_FILE_NAME = 'query_cache.csv'

    def __init__(self):
        self.query_cache = set()

        self.query_cache_file_path = os.path.join(self.folder_path, self.QUERY_CACHE_FILE_NAME)
        print(self.query_cache_file_path)

    def cache_query(self, query: str):
        self.query_cache.add(query)

    def get_algorithm_keys(self):
        algorithm_keys = set()
        for query in self.query_cache:
            keys = self.split_query(query)
            if len(keys) > 0:
                algorithm_keys.add(keys[0])

        return list(algorithm_keys)

    def open(self):
        if os.path.exists(self.query_cache_file_path):
            with open(self.query_cache_file_path, mode='r+') as file:
                self.query_cache = set(file.read().split(','))

    def close(self):
        with open(self.query_cache_file_path, mode='w+') as file:
            content = ','.join(self.query_cache)
            file.write(content)


class NoResultBatching(QueryCachingMixin, AbstractResultBatching):

    FILE_NAME = 'no_batch.json'

    def __init__(self, folder_path: str, quick_save: int = 5):
        AbstractResultBatching.__init__(self, folder_path=folder_path)
        QueryCachingMixin.__init__(self)

        self.save_interval = quick_save

        self.file_path = os.path.join(self.folder_path, self.FILE_NAME)
        self.data = {}
        self.index = 0

    # IMPLEMENT "AbstractResultBatching"
    # ----------------------------------

    def open(self):
        self.data = self._load_data(self.file_path)
        QueryCachingMixin.open(self)

    def save(self, query: str, algorithm_result: AlgorithmResult):
        self.data = self.init_query(self.data, query)

        keys = self.split_query(query)
        assert len(keys) == 3, 'The given result query does not evaluate correctly. Check the syntax!'

        algorithm_key, instance_key, run_key = keys

        self.data[algorithm_key][instance_key][run_key] = algorithm_result
        self._quick_save()

        self.cache_query(query)

    def load(self, query: str) -> object:
        # 19.09.2020: So I have added this special case for when an empty string is passed as a query. This means that
        # the root dictionary is supposed to be returned. I think this might be the only of getting the root without
        # an ugly hack such as accessing the data dict directly or implementing an additional (unnecessary) method
        if query == '':
            return self.data

        keys = self.split_query(query)
        current = self.data
        for key in keys:
            current = current[key]

        return current

    def close(self):
        self._save_data()
        QueryCachingMixin.close(self)

    # HELPER METHODS
    # --------------

    def _quick_save(self):
        if self.index == self.save_interval:
            self._save_data()
            self.index = 0
        else:
            self.index += 1

    def _save_data(self):
        with open(self.file_path, mode='w+') as file:
            file.write(dump_json(self.data, indent=None))

    @classmethod
    def _load_data(cls, file_path):
        if os.path.exists(file_path):
            with open(file_path, mode='r') as file:
                content = file.read()
                return load_json(content)

        return {}


class InstanceBatching(QueryCachingMixin, AbstractResultBatching):

    def __init__(self, folder_path: str):
        AbstractResultBatching.__init__(self, folder_path=folder_path)
        QueryCachingMixin.__init__(self)

        self.index = 0

        self.query_cache = set()
        self.instance_path_map = {}

        self.current_instance = None
        self.current_data = {}

    def open(self):
        self.scan_batches()
        QueryCachingMixin.open(self)

    def save(self, query: str, algorithm_result: AlgorithmResult):
        keys = self.split_query(query)
        assert len(keys) == 3, 'The given result query does not evaluate correctly. Check the syntax!'

        algorithm_key, instance_key, run_key = keys

        if instance_key != self.current_instance:
            self.change_batch(instance_key)

        self.init_query(self.current_data, query)
        self.current_data[algorithm_key][instance_key][run_key] = algorithm_result

        self.cache_query(query)

    def load(self, query: str) -> dict:
        if query == '':
            return self.load_all()

        keys = self.split_query(query)
        if len(keys) == 1:
            return self.load_algorithm(keys[0])
        else:
            instance_key = keys[1]

            if instance_key != self.current_instance:
                self.change_batch(instance_key)

            current = self.current_data
            for key in keys:
                current = current[key]

            self.cache_query(query)

            return current

    def close(self):
        self.save_current()

        self.current_data = {}
        self.current_instance = None
        self.index = 0

        QueryCachingMixin.close(self)

    # HELPER METHODS
    # --------------

    def load_all(self):
        data = {}
        for instance_key in self.instance_path_map.keys():
            self.change_batch(instance_key)
            self.update_dict(data, self.current_data)

        return data

    def load_algorithm(self, algorithm_key: str):
        data = {}
        for instance_key in self.instance_path_map.keys():
            self.change_batch(instance_key)
            self.update_dict(data, self.current_data[algorithm_key])

        return data

    def batch_exists(self, instance_key: str):
        return instance_key in self.instance_path_map.keys()

    def save_current(self):
        if self.current_instance is not None:
            file_path = self.instance_path_map[self.current_instance]
            self.write_file(self.current_data, file_path)

    def create_file_path(self, instance_key: str):
        file_path = os.path.join(self.folder_path, 'instance_batch_{}.json'.format(instance_key))
        self.index += 1
        return file_path

    def create_batch(self, instance_key: str):
        file_path = self.create_file_path(instance_key)
        self.write_file({}, file_path)
        self.instance_path_map[instance_key] = file_path

    def write_file(self, obj: object, file_path: str):
        with open(file_path, mode='w+') as file:
            string = dump_json(
                obj,
                indent=None
            )
            file.write(string)

    def read_file(self, file_path: str):
        with open(file_path, mode='r+') as file:
            content = file.read()
            return load_json(content)

    def load_batch(self, instance_key: str):
        file_path = self.instance_path_map[instance_key]
        self.current_data = self.read_file(file_path)
        self.current_instance = instance_key

    def scan_batches(self):
        for root, folders, files in os.walk(self.folder_path):
            for file in files:
                match = re.search(r'instance_batch_(.*?).json', file)
                if match:
                    instance_key = match.group(1)
                    file_path = os.path.join(root, file)

                    self.instance_path_map[instance_key] = file_path
                    self.index += 1
            break

    def change_batch(self, instance_key: str):
        # Save the current batch state
        self.save_current()

        # Load the new batch
        if not self.batch_exists(instance_key):
            self.create_batch(instance_key)
        self.load_batch(instance_key)

    @classmethod
    def update_dict(cls, d, u):
        for k, v in u.items():
            if isinstance(v, collections.abc.Mapping):
                d[k] = cls.update_dict(d.get(k, {}), v)
            else:
                d[k] = v
        return d


class ExperimentResult(object):

    def __init__(self, folder_path: str, batching_strategy: Type[AbstractResultBatching] = NoResultBatching):
        self.folder_path = folder_path
        self._create_folder()

        self.batching = batching_strategy(self.folder_path)
        self.batching.open()

    # BASIC OPERATIONS
    # ----------------

    def set(self, query: str, algorithm_result: AlgorithmResult):
        self.batching.save(query, algorithm_result)

    def get(self, query: str):
        return self.batching.load(query)

    def close(self):
        self.batching.close()

    # ADDITIONAL OPERATIONS
    # ---------------------

    def add_run(self, algorithm: str, instance: str, run: str, result: AlgorithmResult):
        query = '/'.join([algorithm, instance, run])
        self.set(query, result)

    def get_all_algorithm_keys(self) -> List[str]:
        # TODO: Change the way these keys are being acquired
        # Right now the keys are being computed from getting the whole dictionary into the memory and then getting its
        # keys. This is not a good idea though when thinking about the fact that these dicts can be so big that they
        # have to be batched. A better solution would be to implement a sort of query caching in the batch object and
        # then compute the keys from that...
        return self.batching.get_algorithm_keys()

    def get_algorithm_instance_keys(self, algorithm_key: str) -> List[str]:
        query = algorithm_key
        instances = self.get(query)
        return list(instances.keys())

    def get_all_instance_keys(self) -> List[str]:
        instance_keys = []
        algorithm_keys = self.get_all_algorithm_keys()
        for algorithm_key in algorithm_keys:
            instance_keys += self.get_algorithm_instance_keys(algorithm_key)

        return instance_keys

    def get_results(self, algorithm_key: str, instance_key: str) -> List[AlgorithmResult]:
        query = '{}/{}'.format(algorithm_key, instance_key)
        runs = self.get(query)
        return list(runs.values())

    # HELPER FUNCTIONS
    # ----------------

    def _create_folder(self):
        if not os.path.exists(self.folder_path):
            os.mkdir(self.folder_path, 0o777)


class ExperimentStatistics(object):

    def __init__(self, data: dict):
        self.data = data

    # This method will look at every instance for every algorithm and then summarize over the runs
    @classmethod
    def calc_algorithm_instance_metrics(cls, result: ExperimentResult):
        stats = {}
        algorithm_keys = result.get_all_algorithm_keys()
        for algorithm_key in algorithm_keys:
            stats[algorithm_key] = {}
            instance_keys = result.get_algorithm_instance_keys(algorithm_key)
            for instance_key in instance_keys:
                _stats = {}

                results = result.get_results(algorithm_key, instance_key)

                fitnesses = [result.fitness for result in results]
                _stats.update(cls.get_numeric_attribute_stats('fitness', fitnesses))
                computation_times = [result.time for result in results]
                _stats.update(cls.get_numeric_attribute_stats('time', computation_times))
                iterations = [result.iterations for result in results]
                _stats.update(cls.get_numeric_attribute_stats('iter', iterations))
                feasible = [result.feasible for result in results]
                _stats.update(cls.get_boolean_attribute_stats('feasible', feasible))

                stats[algorithm_key][instance_key] = _stats

        return stats

    @classmethod
    def get_numeric_attribute_stats(cls, attribute_name: str, attribute_values: List[float]) -> Dict[str, float]:
        stats = {
            f'avg_{attribute_name}':        float(np.mean(attribute_values)),
            f'std_{attribute_name}':        float(np.std(attribute_values)),
            f'min_{attribute_name}':        float(np.min(attribute_values)),
            f'max_{attribute_name}':        float(np.max(attribute_values))
        }

        return stats

    @classmethod
    def get_boolean_attribute_stats(cls, attribute_name: str, attribute_values: List[bool]) -> Dict[str, float]:
        stats = {
            f'sum_{attribute_name}':        float(np.sum([1 for value in attribute_values if value]))
        }

        return stats

    def save(self, file_path: str):
        with open(file_path, mode='w+') as file:
            json.dump(self.data, file, sort_keys=False, indent=4)

    @classmethod
    def from_experiment_result(cls, experiment_result: ExperimentResult) -> ExperimentStatistics:
        data = {}

        # Actually calculating the metrics
        data.update(cls.calc_algorithm_instance_metrics(experiment_result))

        return cls(data)

    @classmethod
    def load(cls, file_path: str) -> ExperimentStatistics:
        with open(file_path, mode='r+') as file:
            data = json.load(file)

        return cls(data)
