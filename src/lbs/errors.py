class LbsError(Exception):
    """An error caused by invalid LBS source code or its execution."""

    def __init__(self, source, message):
        self.source = source
        self.message = message
        super().__init__(f'{source} error: {message}')


def error(source, msg):
    raise LbsError(source, msg)
