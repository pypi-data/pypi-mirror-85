from rpckit.exceptions import FunctionException
from rpckit.auth import JwtAuthorizationTicket
from rpckit.constants import RpcDataType


class FunctionCall:
    def __init__(self, *args, auth=""):
        self.args = args
        self.auth = auth


class FunctionOutput:
    def __init__(self, *, error, result, metaData):
        self.result = result
        self.error = error
        self.meta_data = metaData


class Function:

    def __init__(self, name, rpc):
        self.name = name
        self.rpc = rpc

    async def call_async(self, *args):
        c = FunctionCall(*args, auth=self._authorize_call_if_possible())

        data = self.rpc.config.codec.encode(c.__dict__)
        url = self.rpc.config.url_provider(self)
        ct = self.rpc.config.codec.content_type

        r = await self.rpc.config.transport.send(f"{self.rpc.server_url}/{url}", data, ct)

        return self._get_result(r)

    def call(self, *args):
        c = FunctionCall(*args, auth=self._authorize_call_if_possible())

        data = self.rpc.config.codec.encode(c.__dict__)
        url = self.rpc.config.url_provider(self)
        ct = self.rpc.config.codec.content_type

        r = self.rpc.config.transport.send_sync(f"{self.rpc.server_url}/{url}", data, ct)

        return self._get_result(r)

    def _get_result(self, response_data):
        output = FunctionOutput(**self.rpc.config.codec.decode(response_data))

        if output.error != 0:
            raise FunctionException(output.error)

        self._process_meta_data(output)

        return output.result

    def _authorize_call_if_possible(self):
        ticket = self.rpc.config.auth_ticket_holder.get_ticket()
        if ticket is None:
            return ""
        return ticket.access_token

    def _process_meta_data(self, output):
        meta = output.meta_data
        if meta is None:
            return

        if "resultType" in meta:
            result_type = meta["resultType"]
            if result_type == RpcDataType.Auth:
                self.rpc.config.auth_ticket_holder.set_ticket(JwtAuthorizationTicket(**output.result))
