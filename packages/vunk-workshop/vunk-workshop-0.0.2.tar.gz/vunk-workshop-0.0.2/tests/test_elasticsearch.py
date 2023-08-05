import unittest
from unittest import mock

from workshop import elasticsearch


class ElasticsearchTestCase(unittest.TestCase):

    def setUp(self):
        self.es = elasticsearch.Elasticsearch('foo')

    def test_elasticsearch(self):
        with self.assertRaises(TypeError):
            elasticsearch.Elasticsearch()

    def test_host(self):
        assert self.es.host == 'foo'

    def test_attributes(self):
        assert isinstance(self.es.session, elasticsearch.ElasticsearchSession)
        assert isinstance(self.es.cluster, elasticsearch.Cluster)
        assert isinstance(self.es.index, elasticsearch.Index)
        assert isinstance(self.es.document, elasticsearch.Document)


class SessionTestCase(unittest.TestCase):

    def setUp(self):
        es = elasticsearch.Elasticsearch('foo')
        self.session = es.session

    def test_host(self):
        self.assertEqual(self.session.host, 'foo')

    def test_verify(self):
        self.assertFalse(self.session.verify)

    def test_urljoin(self):
        self.assertTrue(callable(self.session.urljoin))

    @mock.patch('requests.Session.get')
    def test_get(self, mock_func):
        mock_func.return_value = True
        result = self.session.get('p1', 'p2')
        self.assertEqual(mock_func.call_count, 1)
        self.assertTrue(result)


class ConnectTestCase(unittest.TestCase):

    def test_connect(self):
        with self.assertRaises(TypeError):
            elasticsearch.connect()

        es = elasticsearch.connect('foo')
        assert isinstance(es, elasticsearch.Elasticsearch)
