import os
import json
from google.cloud import logging as cloud_logging

__version__ = "0.0.3"


class CloudLogger(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def __init__(self, **kwargs):

        credential_path = kwargs.get("credential_path") or os.environ.get(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )

        if credential_path is None:
            raise Exception("Please set GOOGLE_APPLICATION_CREDENTIALS")

        if not os.path.isfile(credential_path):
            raise Exception("Credential file path is not exists")

        __client = cloud_logging.Client.from_service_account_json(credential_path)

        self.__logger = __client.logger(kwargs.get("name", "google_cloud_logger"))

    def info(self, content):
        self.log_text(content, severity="INFO")

    def warn(self, content):
        self.log_text(content, severity="WARNING")

    def error(self, content):
        self.log_text(content, severity="ERROR")

    def critical(self, content):
        self.log_text(content, severity="CRITICAL")

    def log_text(self, content, **kwargs):
        if type(content) in (dict, list):
            content = json.dumps(content)

        self.__logger.log_text(content, severity=kwargs.get("severity", "INFO"))
