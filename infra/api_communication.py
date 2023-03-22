import requests
from typing import Literal, Union


class Communication:
    def __init__(self, session: requests.Session):
        self.session = session

    def send(self,
             url: str,
             method: Literal["GET", "POST", "DELETE", "PUT"],
             **options
             ) -> Union[requests.Response, None]:
        try:
            return self.session.request(method, url, **options)
        except Exception as e:
            print(e)
            return None

    @staticmethod
    def body_format_compare(body: Union[str, dict]) -> tuple:
        as_data, as_json = None, None
        if type(body) == str:
            return body, as_json
        else:
            return as_data, body

    def get(self, url: str) -> Union[requests.Response, None]:
        return self.send(url, "GET")

    def post(self, url: str, body: Union[str, dict]) -> Union[requests.Response, None]:
        as_data, as_json = BaseAPI.body_format_compare(body)
        return self.send(url, "POST", data=as_data, json=as_json)

    def delete(self, url: str) -> Union[requests.Response, None]:
        return self.send(url, "DELETE")

    def put(self, url: str, body: Union[str, dict]) -> Union[requests.Response, None]:
        as_data, as_json = BaseAPI.body_format_compare(body)
        return self.send(url, "PUT", data=as_data, json=as_json)
