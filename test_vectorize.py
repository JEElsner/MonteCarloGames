import numpy as np
import unittest

from vectorize_objects import vectorize


class Foo:
    '''
    Dummy test class to test vectorization on
    '''

    def __init__(self, value):
        self.value = value

        # Call the vectorizer
        vectorize(Foo)

    def get_value(self):
        return self.value


class VectorizeTest(unittest.TestCase):
    def test_object_call(self):
        self.assertEqual(Foo(3).get_value(), 3, 'Call from object')

    def test_ndarray_call(self):
        arr = np.array([Foo(x) for x in range(10)])
        n_arr = np.arange(10)
        self.assertTrue(np.all(Foo.v_bar(arr) == n_arr), 'Call to v_func')

    def test_double_vectorization(self):
        # Called once just to make sure this still works even on the first run
        Foo(3)

        self.assertEqual(vectorize(Foo), False, 'Type already vectorized')


if __name__ == '__main__':
    unittest.main()
