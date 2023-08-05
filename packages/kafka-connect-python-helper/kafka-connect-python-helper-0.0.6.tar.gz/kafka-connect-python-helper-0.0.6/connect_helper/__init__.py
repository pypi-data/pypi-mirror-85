import requests
import time
import sys
import logging
import json

class Connector:
    """ Controls single connector """

    __slots__ = 'session', 'base_url', 'name'

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        self.name = None

    def _check_empty_name(self):
        if not self.name:
            logging.error(f"{self.__class__} attribute 'name' not set")
            raise AttributeError

    def get_remote_config(self, retry=False, backoff_seconds=2):
        self._check_empty_name()
        url = f"{self.base_url}/connectors/{self.name}"
        try:
            r = self.session.get(url=url)
            r.raise_for_status()
            return r
        except requests.exceptions.HTTPError as e:
            if e.response.status_code == 409:
                if not retry:
                    logging.warn(f"Concurrency error while getting remote config. Retrying in {backoff_seconds} seconds...")
                    logging.debug(e)
                    time.sleep(backoff_seconds)
                    return self.get_remote_config(True)
                else:
                    logging.error(f"Concurrency error occurred second time while retrieving remote config. Exiting...")
                    raise e
            else:
                raise e

    def delete(self):
        self._check_empty_name()
        logging.debug(f"Deleting {self.name}")
        url = f"{self.base_url}/connectors/{self.name}"
        return self.session.delete(url=url)

    def put(self, body):
        self._check_empty_name()
        url = f"{self.base_url}/connectors/{self.name}/config"
        return self.session.put(url=url, json=body)

    def get_status(self):
        self._check_empty_name()
        url = f"{self.base_url}/connectors/{self.name}/status"
        r = self.session.get(url=url)
        r.raise_for_status()
        return r

    def poll_status(self, max_retries=90, backoff_seconds=2, minimal_running_tasks=1, initial_sleep_seconds=3):
        self._check_empty_name()

        connector_running = False

        logging.info(f"Intial sleep {initial_sleep_seconds}...")
        time.sleep(initial_sleep_seconds)

        logging.info(f"Waiting for connector {self.name} to become healthy. Max retries: {max_retries}")
        for i in range(0, max_retries):
            logging.info(f"Sleeping {backoff_seconds} seconds...")
            time.sleep(backoff_seconds)
            try:
                status = self.get_status()
                status_result = status.json()
                logging.debug(json.dumps(status_result, indent=2))
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    if not retry:
                        logging.warn(f"Connector {self.name} doesn't exist yet")
                        logging.debug(e)
                        time.sleep(backoff_seconds)
                        return self.poll_status(True)
                    else:
                        logging.error(f"Connector {self.name} doesn't exist after retry. Exiting...")
                        logging.error(e)
                        raise e
                else:
                    raise e

            if not connector_running:
                # Check connector state
                connector_state = status_result["connector"]["state"]
                if connector_state == "RUNNING":
                    logging.info(f"Connector {self.name} is in {connector_state} state")
                    connector_running = True
                else:
                    logging.warn(f"Try {i + 1} of {max_retries}: {self.name} is still in {connector_state} state")
                    continue

            if connector_running:
                if len(status_result["tasks"]) < 1:
                    logging.warn(f"No tasks created yet")
                    continue

                if any(task["state"] == "FAILED" for task in status_result["tasks"]):
                    logging.warn(f"Try {i + 1} of {max_retries}: one or more failed tasks")
                    continue

                running_tasks = sum(task["state"] == "RUNNING" for task in status_result["tasks"])
                if running_tasks < minimal_running_tasks:
                    logging.info(f"Try {i + 1} of {max_retries}: only {running_tasks} running tasks, expecting {minimal_running_tasks}")
                    continue

                logging.info(json.dumps(status_result, indent=2))
                logging.info(f"{running_tasks} running tasks. The connector is healthy!")
                return
        else:
            logging.error(json.dumps(status_result, indent=2))
            logging.error("Too many attempts waiting for connector to become healthy. Exiting...")
            raise TimeoutError

class ConnectHelper():
    """ Initialize Connect session """

    __slots__ = 'session', 'base_url', 'connector'

    def __init__(self, session, base_url):
        self.session = session
        self.base_url = base_url
        self.connector = Connector(session, base_url)

    def get_connectors(self):
        url = f"{self.base_url}/connectors"
        return self.session.get(url=url)
