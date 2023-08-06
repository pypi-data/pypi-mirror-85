import json
import os

basename = os.path.dirname(os.path.realpath(__file__))


class Environments(object):
    __content: dict = {}

    def __init__(self, path_file: str):
        self.__path_file = path_file
        self.__parse()

    def __parse(self) -> None:
        with open(self.__path_file) as json_file:
            self.__content = json.load(json_file)

    def get_env(self, env: str) -> dict:
        return self.__content[env]

    def get_host(self, env: str) -> str:
        return self.__content[env]['host']
