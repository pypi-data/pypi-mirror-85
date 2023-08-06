from setuptools import setup

setup(
    author="David Navarro Alvarez",
    author_email="me@davengeo.com",
    description="rabbitmq-base-library dist",
    url="https://github.com/davengeo/rabbitme-base-library",
    name="rabbitmq-base-library",
    packages=['rabbitmqbaselibrary',
              'rabbitmqbaselibrary.history',
              'rabbitmqbaselibrary.bindings',
              'rabbitmqbaselibrary.common',
              'rabbitmqbaselibrary.definitions',
              'rabbitmqbaselibrary.exchanges',
              'rabbitmqbaselibrary.messages',
              'rabbitmqbaselibrary.policies',
              'rabbitmqbaselibrary.queues',
              'rabbitmqbaselibrary.users',
              'rabbitmqbaselibrary.vhost'],
    install_requires=['requests', 'argparse', 'pyramda', 'rabbitpy'],
)
