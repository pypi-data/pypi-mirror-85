import requests
from pyramda import map, contains

from rabbitmqbaselibrary.common.exceptions import ServerErrorException, VhostNotFound, VhostAlreadyExists
from rabbitmqbaselibrary.common.handlers import handle_rest_response


def is_present(broker: dict, vhost: str) -> bool:
    return contains(vhost, get_vhosts(broker=broker))


def get_vhosts(broker: dict) -> dict:
    url = 'https://{}/api/vhosts'.format(broker['host'])
    response: requests.Response = requests.get(url=url, auth=(broker['user'], broker['passwd']))
    if not response.ok:
        # noinspection PyTypeChecker
        raise ServerErrorException(str(response.status_code), url=url)
    return map(lambda i: i['name'], response.json())


def create_vhost(broker: dict, vhost: str) -> None:
    if is_present(broker=broker, vhost=vhost):
        raise VhostAlreadyExists(vhost)
    url = 'https://{}/api/vhosts/{}'.format(broker['host'], vhost)
    response = requests.put('https://{}/api/vhosts/{}'.format(broker['host'], vhost),
                            auth=(broker['user'], broker['passwd']))
    handle_rest_response(response=response, url=url)


def delete_vhost(broker: dict, vhost: str) -> None:
    if not is_present(broker=broker, vhost=vhost):
        raise VhostNotFound(vhost)
    url = 'https://{}/api/vhosts/{}'.format(broker['host'], vhost)
    response = requests.delete(url, auth=(broker['user'], broker['passwd']))
    handle_rest_response(response=response, url=url)
