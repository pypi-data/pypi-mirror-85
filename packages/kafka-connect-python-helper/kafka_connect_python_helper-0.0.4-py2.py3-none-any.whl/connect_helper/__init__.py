import requests
import time
import sys
import logging

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

    def get_remote_config(self, retry=False):
        self._check_empty_name()
        backoff_seconds = 3
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

    def poll_status(self, max_retries=90, backoff_seconds=2):
        self._check_empty_name()

        connector_running = False
        remote_config = self.get_remote_config()
        count_expected_tasks = remote_config.json()["config"]["tasks.max"]

        logging.info(f"Waiting for connector {self.name} to become healthy. Max retries: {max_retries}")
        for i in range(0, max_retries):
            time.sleep(backoff_seconds)
            try:
                status = self.get_status()
                status_result = status.json()
                logging.debug(status_result)
            except requests.exceptions.HTTPError as e:
                if e.response.status_code == 404:
                    if not retry:
                        logging.warn(f"Connector {self.name} doesn't exist yet. Retrying in {backoff_seconds} seconds...")
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
                    logging.info(f"Connector {self.name} is in RUNNING state")
                    connector_running = True
                elif state == "FAILED":
                    logging.warn(f"Try {i + 1} of {max_retries}: {self.name} created but still in FAILED state. Sleeping {backoff_seconds} seconds")
                    continue
                else:
                    logging.warn(f"Connector state {state}, sleeping {backoff_seconds}...")
                    continue

            if connector_running:
                # Check number of tasks
                count_actual_tasks = len(status_result["tasks"])
                if int(count_actual_tasks) < int(count_expected_tasks):
                    logging.warn(f"Expected tasks: {count_expected_tasks}, actual tasks: {count_actual_tasks}. Sleeping {backoff_seconds}...")
                    continue

                # Check state of tasks
                tasks_healthy = True
                for task in status_result["tasks"]:
                    state = task["state"]
                    if task["state"] == "RUNNING":
                        logging.info(f"Task {task['id']} is in RUNNING state")
                    else:
                        logging.warn(f"Task {task['id']} is in {state} state")
                        tasks_healthy = False

                if not tasks_healthy:
                    logging.warn(f"Try {i + 1} of {max_retries}: not all tasks healthy yet. Sleeping {backoff_seconds}...")
                    continue

                logging.info("All tasks are in RUNNING state. The connector is healthy!")
                return

        else:
            logging.error("Too many attempts waiting for connector to become healthy. Exiting...")
            logging.debug(status_result)
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
