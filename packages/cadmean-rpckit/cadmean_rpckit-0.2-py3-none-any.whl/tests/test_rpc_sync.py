from unittest import TestCase
import dateutil.parser
from rpckit.rpc import RpcClient


class SyncRpcTestCase(TestCase):
    
    def setUp(self):
        self.rpc = RpcClient("http://testrpc.cadmean.ru")
        
    def test_call_sum(self):
        expected = 3
        a = 1
        b = 2
        result = self.rpc.f("sum").call(a, b)
        print(result)
        self.assertEqual(expected, result)

    def test_call_square(self):
        expected = 0.09
        actual = self.rpc.f("square").call(0.3)
        print(actual)
        self.assertEqual(expected, actual)

    def test_call_concat(self):
        expected = "Hello, world!"
        actual = self.rpc.f("concat").call("Hello", ", ", "world!")
        print(actual)
        self.assertEqual(expected, actual)

    def test_call_get_date(self):
        actual = self.rpc.f("getDate").call()
        d = dateutil.parser.parse(actual)
        print(d.strftime("%A, %d. %B %Y %I:%M%p"))

    def test_call_authorized_function(self):
        actual = self.rpc.f("auth").call("email@example.com", "password")
        print(actual)
        self.assertIsNotNone(self.rpc.config.auth_ticket_holder.get_ticket())
        actual = self.rpc.f("user.get").call()
        print(actual)
        self.assertIsNotNone(actual)
