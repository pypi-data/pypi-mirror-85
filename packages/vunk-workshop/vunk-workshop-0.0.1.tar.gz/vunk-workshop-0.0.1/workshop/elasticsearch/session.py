import requests
from functools import wraps
import urllib3

urllib3.disable_warnings()


class ElasticsearchSession(requests.Session):

    def __init__(self, host):
        '''
        Argument
          host: {protocol}://{domain}:{port}
        '''
        super().__init__()
        self.host = host
        self.verify = False

    def __del__(self):
        self.close()

    def urljoin(func):
        @wraps(func)
        def wrapper(self, *paths, **kwargs):
            paths = '/'.join((str(path) for path in paths))
            url = f'{self.host}/{paths}'
            return func(self, url, **kwargs)
        return wrapper

    @urljoin
    def head(self, url, **kwargs):
        return super().head(url=url, **kwargs)

    @urljoin
    def get(self, url, **kwargs):
        return super().get(url=url, **kwargs)

    @urljoin
    def post(self, url, **kwargs):
        return super().post(url=url, **kwargs)

    @urljoin
    def put(self, url, **kwargs):
        return super().put(url=url, **kwargs)

    @urljoin
    def delete(self, url, **kwargs):
        return super().delete(url=url, **kwargs)
