class RpcException(Exception):
    def __init__(self, code, message):
        self.code = code
        self.message = message

    def __str__(self):
        return self.message


class FunctionException(RpcException):

    def __init__(self, error):
        super().__init__(error, f"Function call finished with an error: {error}")
