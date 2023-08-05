import json
from io import StringIO
from itertools import zip_longest
from unittest import TestCase

from json_stream import load
from json_stream.base import (
    TransientAccessException,
    PersistentStreamingJSONObject,
    TransientStreamingJSONList,
    TransientStreamingJSONObject,
    PersistentStreamingJSONList,
)


class TestLoader(TestCase):
    def test_load_empty_object(self):
        obj = {}
        self._test_object(obj, persistent=True)
        self._test_object(obj, persistent=False)

    def test_load_object(self):
        obj = {"a": 1, "b": None, "c": True}
        self._test_object(obj, persistent=True)
        self._test_object(obj, persistent=False)

    def test_load_object_get_persistent(self):
        json = '{"a": 1, "b": null, "c": true}'

        # Access in order
        data = load(StringIO(json), persistent=True)
        self.assertEqual(data['a'], 1)
        self.assertEqual(data['b'], None)
        self.assertEqual(data['c'], True)
        with self.assertRaises(KeyError):
            _ = data['d']

        # Access out of order
        data = load(StringIO(json), persistent=True)
        self.assertEqual(data['b'], None)
        self.assertEqual(data['a'], 1)
        self.assertEqual(data['c'], True)
        with self.assertRaises(KeyError):
            _ = data['d']

        # Access with key error first order
        data = load(StringIO(json), persistent=True)
        with self.assertRaises(KeyError):
            _ = data['d']
        self.assertEqual(data['a'], 1)
        self.assertEqual(data['b'], None)
        self.assertEqual(data['c'], True)

    def test_load_object_get_transient(self):
        json = '{"a": 1, "b": null, "c": true}'

        # Access in order
        data = load(StringIO(json), persistent=False)
        self.assertEqual(data['a'], 1)
        self.assertEqual(data['b'], None)
        self.assertEqual(data['c'], True)
        with self.assertRaises(TransientAccessException):
            _ = data['d']

        # Access out of order
        data = load(StringIO(json), persistent=False)
        self.assertEqual(data['b'], None)
        with self.assertRaises(TransientAccessException):
            _ = data['a']
        with self.assertRaises(TransientAccessException):
            _ = data['c']  # stream was exhausted in search for 'a'
        with self.assertRaises(TransientAccessException):
            _ = data['d']  # don't know if this was a key error or was in the past

        # Access with key error first order
        data = load(StringIO(json), persistent=False)
        with self.assertRaises(KeyError):
            _ = data['d']
        with self.assertRaises(TransientAccessException):
            _ = data['a']  # stream was exhausted in search for 'd'

    def test_load_empty_list(self):
        obj = []
        self._test_list(obj, persistent=True)
        self._test_list(obj, persistent=False)

    def test_load_list(self):
        obj = [1, True, ""]
        self._test_list(obj, persistent=True)
        self._test_list(obj, persistent=False)

    def test_load_list_get_persistent(self):
        json = '[1, true, ""]'

        # Access in order
        data = load(StringIO(json), persistent=True)
        self.assertEqual(data[0], 1)
        self.assertTrue(data[1])
        self.assertEqual(data[2], "")
        with self.assertRaises(IndexError):
            _ = data[3]

        # Access out of order
        data = load(StringIO(json), persistent=True)
        self.assertEqual(data[0], 1)
        self.assertTrue(data[1])
        self.assertEqual(data[2], "")
        with self.assertRaises(IndexError):
            _ = data[3]

    def test_load_list_get_transient(self):
        json = '[1, true, ""]'

        # Access in order
        data = load(StringIO(json), persistent=False)
        self.assertEqual(data[0], 1)
        self.assertTrue(data[1])
        self.assertEqual(data[2], "")
        with self.assertRaises(IndexError):
            _ = data[3]

        # Access out of order
        data = load(StringIO(json), persistent=False)
        self.assertTrue(data[1])
        with self.assertRaises(TransientAccessException):
            _ = data[0]
        self.assertEqual(data[2], "")
        with self.assertRaises(IndexError):
            _ = data[3]

    def test_load_nested_persistent(self):
        json = '{"count": 3, "results": ["a", "b", {}]}'
        data = load(StringIO(json), persistent=True)
        self.assertIsInstance(data, PersistentStreamingJSONObject)
        results = data['results']
        self.assertIsInstance(results, PersistentStreamingJSONList)
        self.assertEqual(results[0], 'a')
        self.assertEqual(results[1], 'b')
        self.assertIsInstance(results[2], PersistentStreamingJSONObject)
        self.assertEqual(len(results), 3)
        self.assertEqual(len(results[2]), 0)
        self.assertEqual(len(data), 2)
        self.assertEqual(data["count"], 3)

    def test_load_nested_transient(self):
        json = '{"count": 3, "results": ["a", "b", "c"]}'
        data = load(StringIO(json), persistent=False)
        self.assertIsInstance(data, TransientStreamingJSONObject)
        results = data['results']
        self.assertIsInstance(results, TransientStreamingJSONList)
        self.assertEqual(list(results), ['a', 'b', 'c'])

    def _test_object(self, obj, persistent):
        self.assertListEqual(list(self._to_data(obj, persistent)), list(obj))
        self.assertListEqual(list(self._to_data(obj, persistent).keys()), list(obj.keys()))
        self.assertListEqual(list(self._to_data(obj, persistent).values()), list(obj.values()))
        self.assertListEqual(list(self._to_data(obj, persistent).items()), list(obj.items()))
        if persistent:
            self.assertEqual(len(self._to_data(obj, persistent)), len(obj))
        for k, expected_k in zip_longest(self._to_data(obj, persistent), obj):
            self.assertEqual(k, expected_k)

        if not persistent:
            data = self._to_data(obj, persistent)
            iter(data)  # iterates first time
            with self.assertRaises(TransientAccessException):
                iter(data)  # can't get second iterator
            with self.assertRaises(TransientAccessException):
                data.keys()  # can't get keys
            with self.assertRaises(TransientAccessException):
                data.values()  # can't get keys
            with self.assertRaises(TransientAccessException):
                data.items()  # can't get keys

    def _test_list(self, obj, persistent):
        self.assertListEqual(list(self._to_data(obj, persistent)), list(obj))
        if persistent:
            self.assertEqual(len(self._to_data(obj, persistent)), len(obj))
        for k, expected_k in zip_longest(self._to_data(obj, persistent), obj):
            self.assertEqual(k, expected_k)

        if not persistent:
            data = self._to_data(obj, persistent)
            iter(data)  # iterates first time
            with self.assertRaises(TransientAccessException):
                iter(data)  # can't get second iterator

    def _to_data(self, obj, persistent):
        return load(StringIO(json.dumps(obj)), persistent)
