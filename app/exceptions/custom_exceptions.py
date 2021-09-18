class CustomException(Exception):
    pass


class InvalidQueryParametersException(CustomException):
    pass


class InvalidS3ParametersException(CustomException):
    pass


class FileNotFoundException(Exception):
    pass
