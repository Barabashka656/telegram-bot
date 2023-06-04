class InvalidResponseStatusCodeError(Exception):
    "Raised when the status code is not 200"
    def __init__(self, message):
        self.message = message

class InvalidWeatherServiceError(Exception):
    "Raised when the weather service is not supported"
    def __init__(self, service):
        self.message = service

class InvalidCityNameError(Exception):
    "Raised when the city is not supported"
    def __init__(self, city):
        self.message = city
