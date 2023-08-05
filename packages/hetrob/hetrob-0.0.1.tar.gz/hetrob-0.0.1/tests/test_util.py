from unittest import TestCase

from hetrob.util import load_json, dump_json


class TestJsonSerialization(TestCase):

    def test_util_import(self):
        """
        This test checks if we can even import stuff from the "util" module, which is in the same folder as this test
        module.
        """
        from util import HELLO
        self.assertEqual('Hello World!', HELLO)

    def test_serialize(self):
        """
        Whether or not a class is correctly being serialized by the "dump_json" method within the util module.
        """
        from util import JsonSampleClass

        sample = JsonSampleClass(1, 2, 3)
        string = dump_json(sample)
        # The main objective is to check whether this "dump_json" function does not raise errors, but we can also check
        # here if the string is at least not empty.
        # I dont want to check for the actual content of the string since the json encoding process could change over
        # time
        self.assertIsInstance(string, str)
        self.assertNotEqual(string, '')

    def test_serialize_and_deserialize(self):
        """
        Tests whether or not an object with the JsonMixin can be dumped into a string and be loaded from this string
        again correctly.
        """
        from util import JsonSampleClass

        sample = JsonSampleClass(1, 2, 3)
        string = dump_json(sample)
        loaded_sample = load_json(string)

        self.assertEqual(loaded_sample, sample)
