"""
A module containing utility for the test modules within this very same folder.
"""
from hetrob.util import JsonMixin


HELLO = 'Hello World!'


class JsonSampleClass(JsonMixin):

    def __init__(self, a, b, c):
        JsonMixin.__init__(self)

        self.a = a
        self.b = b
        self.c = c

    def get_import(self):
        return 'util', 'JsonSampleClass'

    def to_dict(self):
        return {
            'a': self.a,
            'b': self.b,
            'c': self.c
        }

    @classmethod
    def from_dict(cls, data: dict):
        return cls(
            a=data['a'],
            b=data['b'],
            c=data['c']
        )

    def __eq__(self, other):
        return self.a == other.a and self.b == other.b and self.c == other.c
