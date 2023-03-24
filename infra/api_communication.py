import requests
from typing import Literal, Union


from utils import logger,my_origin

class Communication:
    def __init__(self, session: requests.Session):
        self.session = session

    def send(self,
             url: str,
             method: Literal["GET", "POST", "DELETE", "PUT"],
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
            r = self.session.request(method, url, **options)
            logger.log(f"{method} > {r.status_code} > {r.text}", attach_origin=my_origin())
            return r
        except requests.RequestException as e:
            logger.log(str(e),level="error",attach_origin=my_origin())
            return None

    @staticmethod
    def body_format_compare(body: Union[str, dict]) -> tuple:
        as_data, as_json = None, None
        if type(body) == str:
            return body, as_json
        else:
            return as_data, body

    def get(self, url: str,**options) -> Union[requests.Response, None]:
        return self.send(url, "GET",**options)

    def post(self, url: str, body: Union[str, dict],**options) -> Union[requests.Response, None]:
        as_data, as_json = Communication.body_format_compare(body)
        return self.send(url, "POST", data=as_data, json=as_json,**options)

    def delete(self, url: str,**option) -> Union[requests.Response, None]:
        return self.send(url, "DELETE",**option)

    def put(self, url: str, body: Union[str, dict],**options) -> Union[requests.Response, None]:
        as_data, as_json = Communication.body_format_compare(body)
        return self.send(url, "PUT", data=as_data, json=as_json,**options)

