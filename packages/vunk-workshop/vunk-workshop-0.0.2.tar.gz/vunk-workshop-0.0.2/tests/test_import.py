import importlib
import unittest


class ImportTestCase(unittest.TestCase):

    def test_import(self):
        # from workshop import elasticsearch
        elasticsearch = importlib.import_module(
            '.elasticsearch', package='workshop')
        assert elasticsearch.Elasticsearch('foo')

    def test_import_workshop(self):
        # import workshop
        workshop = importlib.import_module('workshop')
        assert workshop.elasticsearch.Elasticsearch('foo')
