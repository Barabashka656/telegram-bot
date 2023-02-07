class InvalidResponseStatusCodeError(Exception):
    "Raised when the status code is not 200"
    def __init__(self, message):
        self.message = message
