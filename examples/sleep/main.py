import logging

from task_sharding_client.arg_parse import parse_input_arguments
from task_sharding_client.connection import Connection
from task_sharding_client.client import Client

from sleep_task import SleepTask


def main():
    configuration = parse_input_arguments()
    with Connection("ws://localhost:8000/ws/api/1/" + configuration.client_id + "/") as connection:
        client = Client(configuration, connection, SleepTask)
        client.run()


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    main()
