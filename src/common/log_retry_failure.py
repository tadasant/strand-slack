class log_retry_failure:
    """Wrapper class intended for logging tenacity retry failures"""

    def __init__(self, logger, level, message):
        self.logger = logger
        self.message = message
        self.level = level

    def __call__(self):
        self.logger.log(lvl=self.level, msg=self.message)
