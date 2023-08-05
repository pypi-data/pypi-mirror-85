import requests


class ElasticsearchError(Exception):
    pass


class Cluster:

    def __init__(self, session):
        self.session = session


class Index:

    def __init__(self, session):
        self.session = session

    def exists(self, name):
        response = self.session.head(name)
        if response.status_code == requests.codes.ok:
            return True
        if response.status_code == requests.codes.not_found:
            return False
        raise ElasticsearchError(f'{response.status_code}: {response.url}')

    def create(self, name):
        response = self.session.put(name)
        if response.status_code == requests.codes.ok:
            return response.json()
        raise ElasticsearchError(response.text)

    def delete(self, name):
        response = self.session.delete(name)
        if response.status_code == requests.codes.ok:
            return response.json()
        raise ElasticsearchError(response.text)

    def get(self, name, id):
        response = self.session.get(name, '_doc', id)
        if response.status_code == requests.codes.ok:
            return response.json()['_source']
        raise ElasticsearchError(response.text)

    def serialize(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            result = func(*args, **kwargs)
            return {
                'total': result['hits']['total']['value'],
                'data': [x['_source'] for x in result['hits']['hits']]
            }
        return wrapper

    @serialize
    def search(self, name):
        response = self.session.get(name, '_search')
        if response.status_code == requests.codes.ok:
            return response.json()
        raise ElasticsearchError(response.text)


class Document:

    def __init__(self, session):
        self.session = session

    def create(self, name, doc, id=None, refresh=False):
        params = None
        if refresh:
            params = {'refresh': 'true'}
        if id:
            response = self.session.put(name, '_doc', id, json=doc, params=params)
        else:
            # Automatic ID Generation
            response = self.session.post(name, '_doc/', json=doc, params=params)
        if response.status_code == requests.codes.created:
            return response.json()
        raise ElasticsearchError(f'{response.status_code}: {response.text}')

    def bulk_create(self, name, bulk_data):
        buf = []
        for data in bulk_data:
            buf.append({'index': {}})
            buf.append(data)
        ndjson = '\n'.join([json.dumps(x, separators=(',', ':')) for x in buf])
        ndjson += '\n'
        headers = {'Content-Type': 'application/x-ndjson'}

        response = self.session.post(name, '_bulk', data=ndjson, headers=headers)
        if response.status_code == requests.codes.ok:
            return response.json()
        raise ElasticsearchError(response.text)
