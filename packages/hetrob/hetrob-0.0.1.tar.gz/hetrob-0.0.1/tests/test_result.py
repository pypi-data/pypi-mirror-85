from unittest import TestCase
import tempfile
import os
from pprint import pprint

from hetrob.result import AlgorithmResult, NoResultBatching, ExperimentResult, ExperimentStatistics, InstanceBatching
from hetrob.util import MaxIterTermination, dump_json, load_json
from hetrob._testing import MockProblem, MockSolution


# HELPER FUNCTIONS
# ----------------

def get_mock_algorithm_results():
    problem = MockProblem()
    solution = MockSolution(problem)
    termination = MaxIterTermination(niter=100)

    return AlgorithmResult(
        problem=problem,
        solution=solution,
        termination=termination,
        logbook={},
        fitness=solution.evaluate(),
        time=100,
        iterations=100,
        feasible=True
    )


class TestAlgorithmResult(TestCase):

    def test_construction(self):
        """
        Simply tests if the TestAlgorithm object can be constructed
        """
        problem = MockProblem()
        solution = MockSolution(problem)
        termination = MaxIterTermination(niter=100)

        algorithm_result = AlgorithmResult(
            problem=problem,
            solution=solution,
            termination=termination,
            logbook={},
            fitness=100,
            time=100,
            iterations=100,
            feasible=True
        )
        self.assertIsInstance(algorithm_result, AlgorithmResult)

    def test_serialization_and_deserialization(self):
        """
        Tests if a AlgorithmTest object can be serialized and deserialized again while keeping all data
        """
        problem = MockProblem()
        solution = MockSolution(problem)
        termination = MaxIterTermination(niter=100)

        algorithm_result = AlgorithmResult(
            problem=problem,
            solution=solution,
            termination=termination,
            logbook={},
            fitness=solution.evaluate(),
            time=100,
            iterations=100,
            feasible=True
        )

        json_string = dump_json(algorithm_result)
        algorithm_result_loaded = load_json(json_string)

        self.assertIsInstance(algorithm_result_loaded, AlgorithmResult)
        self.assertIsInstance(algorithm_result_loaded.problem, MockProblem)
        self.assertIsInstance(algorithm_result_loaded.solution.problem, MockProblem)


class TestNoResultBatching(TestCase):

    def test_split_query(self):
        """
        Test the "split_query" method
        """
        query = 'algorithm/instance/run'
        expected_split = ['algorithm', 'instance', 'run']

        split_query = NoResultBatching.split_query(query)
        self.assertEqual(3, len(split_query))
        self.assertEqual(expected_split, split_query)

    def test_init_query(self):
        """
        Test the "init_query" method
        """
        query = 'algorithm/instance/run'
        data = {}

        data = NoResultBatching.init_query(data, query)
        print(data)
        self.assertTrue('algorithm' in data)
        self.assertTrue('instance' in data['algorithm'])
        self.assertTrue('run' in data['algorithm']['instance'])

    def test_construction(self):
        """
        Tests if an object can be constructed without error
        """
        with tempfile.TemporaryDirectory() as folder_path:
            no_batching = NoResultBatching(folder_path, quick_save=10)
            no_batching.open()

            algorithm_results = get_mock_algorithm_results()
            no_batching.save('algorithm1/instance1/0', algorithm_results)
            no_batching.close()

            self.assertTrue('algorithm1' in no_batching.data.keys())

    def test_saving_and_loading(self):
        """
        Tests if data can be saved into a file and subseqently be loaded again without error and loss of data
        """
        with tempfile.TemporaryDirectory() as folder_path:
            no_batching = NoResultBatching(folder_path, quick_save=10)
            no_batching.open()

            algorithm_results = get_mock_algorithm_results()
            no_batching.save('algorithm1/instance1/0', algorithm_results)
            no_batching.close()

            del no_batching
            del algorithm_results

            no_batching = NoResultBatching(folder_path, quick_save=10)
            no_batching.open()

            algorithm_results = no_batching.load('algorithm1/instance1/0')
            self.assertIsInstance(algorithm_results, AlgorithmResult)

    def test_context_manager(self):
        """
        Tests the usage of an instance as a context manager
        """
        with tempfile.TemporaryDirectory() as folder_path:
            with NoResultBatching(folder_path) as no_batching:
                self.assertIsInstance(no_batching, NoResultBatching)

    def test_query_cache(self):
        with tempfile.TemporaryDirectory() as folder_path:
            no_batching = NoResultBatching(folder_path)
            no_batching.open()

            algorithm_results = get_mock_algorithm_results()
            no_batching.save('algorithm1/instance1/run1', algorithm_results)
            no_batching.save('algorithm1/instance1/run2', algorithm_results)
            self.assertEqual(2, len(no_batching.query_cache))

            no_batching.close()

            self.assertTrue(os.path.exists(no_batching.query_cache_file_path))


class TestInstanceBatching(TestCase):

    def test_construction(self):
        """
        Tests if an object can be constructed without error
        """
        with tempfile.TemporaryDirectory() as folder_path:
            instance_batching = InstanceBatching(folder_path)
            instance_batching.open()

            self.assertIsInstance(instance_batching, InstanceBatching)

    def test_single_save_and_load(self):
        with tempfile.TemporaryDirectory() as folder_path:
            instance_batching = InstanceBatching(folder_path)
            instance_batching.open()

            query = 'algorithm1/instance1/run1'
            algorithm_results = get_mock_algorithm_results()
            instance_batching.save(query, algorithm_results)
            loaded_algorithm_results = instance_batching.load(query)

            self.assertEqual(algorithm_results, loaded_algorithm_results)

    def test_multiple_save_and_load(self):
        with tempfile.TemporaryDirectory() as folder_path:
            instance_batching = InstanceBatching(folder_path)
            instance_batching.open()

            for instance_key in range(3):
                for algorithm_key in range(3):
                    for run_key in range(3):
                        query = '{}/{}/{}'.format(algorithm_key, instance_key, run_key)
                        algorithm_result = get_mock_algorithm_results()
                        instance_batching.save(query, algorithm_result)

            self.assertNotEqual(0, instance_batching.index)
            self.assertEqual(3, instance_batching.index)

            instance_batching.close()
            del instance_batching
            instance_batching = InstanceBatching(folder_path)
            instance_batching.open()

            algorithm_result = instance_batching.load('0/2/2')
            self.assertIsInstance(algorithm_result, AlgorithmResult)

    def test_load_all(self):
        with tempfile.TemporaryDirectory() as folder_path:
            instance_batching = InstanceBatching(folder_path)
            instance_batching.open()

            for instance_key in range(3):
                for algorithm_key in range(3):
                    for run_key in range(3):
                        query = '{}/{}/{}'.format(algorithm_key, instance_key, run_key)
                        algorithm_result = get_mock_algorithm_results()
                        instance_batching.save(query, algorithm_result)

            self.assertNotEqual(0, instance_batching.index)
            self.assertEqual(3, instance_batching.index)

            instance_batching.close()
            del instance_batching
            instance_batching = InstanceBatching(folder_path)
            instance_batching.open()

            data = instance_batching.load_all()
            self.assertIsInstance(data, dict)
            self.assertEqual(3, len(data['0'].keys()))

    def test_query_cache(self):
        with tempfile.TemporaryDirectory() as folder_path:
            instance_batching = InstanceBatching(folder_path)
            instance_batching.open()

            algorithm_results = get_mock_algorithm_results()
            instance_batching.save('algorithm1/instance1/run1', algorithm_results)
            instance_batching.save('algorithm1/instance1/run2', algorithm_results)
            self.assertEqual(2, len(instance_batching.query_cache))

            instance_batching.close()

            self.assertTrue(os.path.exists(instance_batching.query_cache_file_path))


class TestExperimentResult(TestCase):

    def test_construction(self):
        """
        If the construction of a new instance works withou errors
        """
        with tempfile.TemporaryDirectory() as folder_path:
            experiment_result = ExperimentResult(folder_path)
            self.assertIsInstance(experiment_result, ExperimentResult)
            self.assertTrue(os.path.exists(folder_path))

    def test_saving_and_loading(self):
        """
        Tests if the saving and loading from the file system works correctly with some mock entries into the an +
        ExperimentResult instance
        """
        with tempfile.TemporaryDirectory() as folder_path:
            experiment_result = ExperimentResult(folder_path)

            for algorithm_id in range(2):
                for instance_id in range(5):
                    for run_id in range(5):
                        query = '{}/{}/{}'.format(algorithm_id, instance_id, run_id)
                        results = get_mock_algorithm_results()
                        experiment_result.set(query, results)

            # Now we are going to delete this specific instance and load it again...
            experiment_result.close()
            del experiment_result

            # The data should still be accessible from the persistent file after loading a new instance
            experiment_result = ExperimentResult(folder_path)
            self.assertIsInstance(experiment_result.get('0/0/0'), AlgorithmResult)
            self.assertIsInstance(experiment_result.get('1/4/3'), AlgorithmResult)
            # Also testing that a query which is not supposed to exist also raises an error
            self.assertRaises(KeyError, experiment_result.get, '3/3/3')


class TestExperimentStatistics(TestCase):

    def test_construction(self):
        statistics = ExperimentStatistics({})
        self.assertIsInstance(statistics, ExperimentStatistics)

    def test_saving_and_loading(self):
        with tempfile.TemporaryDirectory() as folder_path:
            file_path = os.path.join(folder_path, 'stats.json')

            # Here we create and save the dictionary data
            statistics = ExperimentStatistics({'key': 'value'})
            statistics.save(file_path)

            # Now we need to delete it and load it again from the file system
            del statistics
            statistics = ExperimentStatistics.load(file_path)

            self.assertEqual('value', statistics.data['key'])

    def test_calculating_statistics_from_result(self):
        with tempfile.TemporaryDirectory() as folder_path:
            experiment_result = ExperimentResult(folder_path)

            for algorithm_id in range(2):
                for instance_id in range(2):
                    for run_id in range(2):
                        query = '{}/{}/{}'.format(algorithm_id, instance_id, run_id)
                        results = get_mock_algorithm_results()
                        experiment_result.set(query, results)

            statistics = ExperimentStatistics.from_experiment_result(experiment_result)
            self.assertTrue('0' in statistics.data)
            self.assertTrue('min_time' in statistics.data['0']['0'])
