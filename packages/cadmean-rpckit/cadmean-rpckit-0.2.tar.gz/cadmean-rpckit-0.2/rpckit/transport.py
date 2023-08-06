from aiohttp import ClientSession
from aiohttp import ClientError

import requests
from requests import RequestException

from rpckit.exceptions import RpcException
from rpckit.constants import RpcErrorCode
from rpckit.constants import SUPPORTED_RPC_VERSION


class HttpTransport:

    async def send(self, url, data, content_type):
        try:
            async with ClientSession() as session:
                headers = {
                    "Content-Type": content_type,
                    "Cadmean-RPC-Version": SUPPORTED_RPC_VERSION
                }
                async with session.post(url, data=data, headers=headers, timeout=10) as resp:
                    if resp.status != 200:
                        raise RpcException(RpcErrorCode.UnsuccessfulStatusCode,
                                           f"Server failed to respond with a success status code. "
                                           f"Actual status code: {resp.status}")
                    return await resp.read()
        except ClientError:
            raise RpcException(RpcErrorCode.FailedToSendCall, "Connection problem occurred")

    def send_sync(self, url, data, content_type):
        headers = {
            "Content-Type": content_type,
            "Cadmean-RPC-Version": SUPPORTED_RPC_VERSION
        }

        try:
            response = requests.post(url, data, headers=headers, timeout=10)

            if response.status_code != 200:
                raise RpcException(RpcErrorCode.UnsuccessfulStatusCode,
                                   f"Server failed to respond with a success status code. "
                                   f"Actual status code: {response.status_code}")

            return response.content
        except RequestException:
            raise RpcException(RpcErrorCode.FailedToSendCall, "Connection problem occurred")
