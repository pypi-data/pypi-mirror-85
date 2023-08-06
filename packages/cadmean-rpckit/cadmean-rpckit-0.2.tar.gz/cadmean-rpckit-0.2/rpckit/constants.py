SUPPORTED_RPC_VERSION = "2.1"


class RpcErrorCode:
    NoError = 0

    FunctionNotCallable = -100
    FunctionNotFound = -101
    IncompatibleRpcVersion = -102

    InvalidFunctionArguments = -200

    FailedToEncode = -300
    FailedToDecode = -301

    FailedToSendCall = -400
    UnsuccessfulStatusCode = -401

    InternalServerError = -500

    NotAuthorized = -600

    PreCallChecksFailed = -700


class RpcDataType:
    String = "string"
    Integer = "int"
    Float = "float"
    Date = "date"
    List = "list"
    Object = "Object"
    Auth = "auth"
    Null = "null"
