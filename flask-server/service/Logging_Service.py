class Logging_Service(object):
    def __init__(self):
        from google.cloud import logging

        # Instantiates a client
        logging_client = logging.Client()
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
