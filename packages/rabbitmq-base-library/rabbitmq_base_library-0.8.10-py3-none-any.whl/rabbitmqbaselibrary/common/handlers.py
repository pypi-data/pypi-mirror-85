import requests

from rabbitmqbaselibrary.common.exceptions import BadRequest, ServerErrorException, Unauthorised, NotFoundException


# noinspection PyPep8Naming
def handle_rest_response_with_body(response: requests.Response, url: str, body: object) -> None:
    if not response.ok:
        if response.status_code == 404:
            raise NotFoundException(message='resource not found', url=url)
        if response.status_code == 400:
            raise BadRequest(message='bad request', url=url, body=body)
        if response.status_code == 500:
            raise ServerErrorException(message='server exception', url=url)
        if response.status_code == 401:
            raise Unauthorised(url=url)
        else:
            raise Exception(response.status_code, response.reason)


# noinspection PyPep8Naming
def handle_rest_response(response: requests.Response, url: str) -> None:
    if not response.ok:
        if response.status_code == 404:
            raise NotFoundException(message='resource not found', url=url)
        if response.status_code == 500:
            raise ServerErrorException(message='server exception', url=url)
        if response.status_code == 401:
            raise Unauthorised(url=url)
        else:
            raise Exception(response.status_code, response.reason)
