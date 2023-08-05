from workshop.elasticsearch.api import Cluster, Document, Index
from workshop.elasticsearch.session import ElasticsearchSession


class Elasticsearch:
    _cluster = None
    _index = None
    _document = None

    def __init__(self, host):
        self.host = host
        self.session = ElasticsearchSession(host)

        self.cluster = Cluster(self.session)
        self.index = Index(self.session)
        self.document = Document(self.session)


def connect(host):
    return Elasticsearch(host)
