class Logging_Service(object):
    def __init__(self):
        from google.cloud import logging

        # Instantiates a client
        logging_client = logging.Client()

        # The name of the log to write to
        # log_name = "application-log"
        # Selects the log to write to
        # self.logger = logging_client.logger(log_name)
        logging_client.setup_logging()

    def info(self, text: str) -> None:
        import logging

        # Writes the log entry
        logging.info(text)

    def warning(self, text: str) -> None:
        import logging

        # Writes the log entry
        logging.warning(text)

    def error(self, text: str) -> None:
        import logging

        # Writes the log entry
        logging.error(text)
