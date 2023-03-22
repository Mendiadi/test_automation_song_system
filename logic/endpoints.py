import requests

from infra.api_communication import Communication

class BaseAPI:
    def __init__(self,communication:Communication):
        self.communication = communication

class Users(BaseAPI):

    def add_user(self,user):
        ...


    def get_user(self):
        ...



