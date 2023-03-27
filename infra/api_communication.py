import requests
from typing import Literal, Union

from utils import logger, my_origin


class Communication:
    def __init__(self, session: requests.Session):
        self.session = session

    def send(self,
             url: str,
             method: Literal["GET", "POST", "DELETE", "PUT"],
             timeout: int = 5,
             **options
             ) -> Union[requests.Response, None]:
        """
        Generic send requests method.
        :param url: url path
        :param method: GET,POST,DELETE,PUT
        :param options: kwargs arguments for config
        :return: response object
        """
        try:
            r = self.session.request(method, url, **options, timeout=timeout)
            logger.log(f"{method} > {r.status_code} > {r.text}", attach_origin=my_origin())
            return r
        except requests.RequestException as e:
            logger.log(str(e), level="error", attach_origin=my_origin())
            return None

    def get(self, url: str, **options) -> Union[requests.Response, None]:
        return self.send(url, "GET", **options)

    def post(self, url: str, **options) -> Union[requests.Response, None]:
        return self.send(url, "POST", **options)

    def delete(self, url: str, **option) -> Union[requests.Response, None]:
        return self.send(url, "DELETE", **option)

    def put(self, url: str, **options) -> Union[requests.Response, None]:
        return self.send(url, "PUT", **options)
