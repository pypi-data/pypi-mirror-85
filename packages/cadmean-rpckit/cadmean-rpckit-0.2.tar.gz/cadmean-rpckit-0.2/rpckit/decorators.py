from rpckit.rpc import RpcClient
from rpckit.exceptions import RpcException
from rpckit.constants import RpcErrorCode


class RpcFunction:

    default_server_url = None

    _rpc_cache = {}

    def __init__(self, function_name, server_url=None, async_call=False):
        self.server_url = server_url
        self.function_name = function_name
        self.async_call = async_call

    def __call__(self, fn):
        if self.async_call:
            return self._get_async_wrapper(fn)
        else:
            return self._get_wrapper(fn)

    def _get_wrapper(self, fn):
        def wrapper(*args, **kwargs):
            u = self._get_url()
            rpc = RpcFunction._get_rpc(u)
            fn(*args, **kwargs)
            return rpc.f(self.function_name).call(*args)
        return wrapper

    def _get_async_wrapper(self, fn):
        async def wrapper(*args, **kwargs):
            u = self._get_url()
            rpc = RpcFunction._get_rpc(u)
            fn(*args, **kwargs)
            return await rpc.f(self.function_name).call_async(*args)
        return wrapper

    def _get_url(self):
        if self.server_url is not None:
            return self.server_url

        if RpcFunction.default_server_url is not None:
            return RpcFunction.default_server_url

        raise RpcException(RpcErrorCode.PreCallChecksFailed, "No server url specified")

    @staticmethod
    def _get_rpc(server_url):
        if server_url in RpcFunction._rpc_cache:
            return RpcFunction._rpc_cache[server_url]
        else:
            rpc = RpcClient(server_url)
            RpcFunction._rpc_cache[server_url] = rpc
            return rpc

    @staticmethod
    def clear_cache():
        RpcFunction._rpc_cache = {}
