class VhostAlreadyExists(Exception):
    def __init__(self, vhost: str):
        self.vhost = vhost


class VhostNotFound(Exception):
    def __init__(self, vhost: str):
        self.vhost = vhost


class Unauthorised(Exception):
    def __init__(self, url: str):
        self.url = url


class NotFoundException(Exception):
    def __init__(self, message: str, url: str):
        self.message = message
        self.url = url


class ServerErrorException(Exception):
    def __init__(self, message: str, url: str):
        self.message = message
        self.url = url


class BadRequest(Exception):
    def __init__(self, message: str, url: str, body: object):
        self.message = message
        self.url = url
        self.body = body


class TemplateException(BaseException):
    def __init__(self, message: str, template_name: str):
        self.message = message
        self.template_name = template_name


class NotValidPermissions(BaseException):
    def __init__(self, message: str, permissions: dict):
        self.message = message
        self.permissions = permissions


class UserAlreadyExists(BaseException):
    def __init__(self, user: str):
        self.user = user
