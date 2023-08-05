from unittest import TestCase

from hetrob.problem import BasicProblem



class TestBasicProblem(TestCase):

    BASIC_PROBLEM_DICT = {
        'vehicle_count': 2,
        'duration': 5,
        'coordinates': [
            (0, 0),
            (10, 20),
            (20, 10),
            (30, 30),
            (40, 0)
        ]
    }

    def test_empty_construction(self):
        """
        If an empty problem can even be constructed
        :return:
        """
        problem = BasicProblem(0, [], 0)
        self.assertIsInstance(problem, BasicProblem)

    def test_from_dict(self):
        """
        if an object can be created from a dict
        :return:
        """
        problem = BasicProblem.from_dict(self.BASIC_PROBLEM_DICT)
        self.assertIsInstance(problem, BasicProblem)
        self.assertEqual(2, problem.vehicle_count)
        self.assertEqual(5, problem.node_count)

    def test_to_dict(self):
        """
        If conversion to dict works
        :return:
        """
        problem = BasicProblem.from_dict(self.BASIC_PROBLEM_DICT)
        # Converting it into a dict
        problem_dict = problem.to_dict()
        # Has to be the same dict as it was loaded from
        self.assertEqual(self.BASIC_PROBLEM_DICT, problem_dict)

    def test_edge_weight(self):
        """
        If edge weight is calculated correctly
        :return:
        """
        problem = BasicProblem.from_dict(self.BASIC_PROBLEM_DICT)
        # Straight line from (0, 0) to (40, 0)
        expected_weight_1 = 40
        weight1 = problem.get_edge_weight(0, 4)
        self.assertAlmostEqual(expected_weight_1, weight1)
        # Line from (20, 10) to (30, 30)
        expected_weight_2 = 22.36
        weight2 = problem.get_edge_weight(1, 3)
        self.assertAlmostEqual(expected_weight_2, weight2, 2)
