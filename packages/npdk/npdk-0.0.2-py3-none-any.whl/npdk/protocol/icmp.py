import json
from functools import wraps
from ipaddress import IPv4Address
from urllib.parse import urljoin

import attr
import pythonping
from npdk import core, exceptions


@attr.s
class Warning:
    rtt_avg: float = attr.ib(converter=float)
    miss_rate: float = attr.ib(converter=float)

    @classmethod
    def creator(cls, arg):
        return cls(*arg.split(':'))


@attr.s
class Error:
    rtt_avg: float = attr.ib(converter=float)
    miss_rate: float = attr.ib(converter=float)

    @classmethod
    def creator(cls, arg):
        return cls(*arg.split(':'))


@attr.s
class Arguments:
    host: str = attr.ib(converter=[IPv4Address, str])
    warning: type = attr.ib(validator=attr.validators.instance_of(Warning))
    error: type = attr.ib(validator=attr.validators.instance_of(Error))


@attr.s
class Request:
    target: str = attr.ib(converter=[IPv4Address, str])
    timeout: int = attr.ib(converter=int, default=2)
    count: int = attr.ib(converter=int, default=5)
    verbose: bool = attr.ib(converter=bool, default=False)


@attr.s
class Response(Arguments):
    rtt_avg: float = attr.ib()
    miss_rate: float = attr.ib()


class TestCase(core.PluginTestCase):

    def add_arguments(self, parser):
        parser.add_argument('host', type=str)
        parser.add_argument('--warning', type=str, help='{rtt_avg:miss_rate}')
        parser.add_argument('--error', type=str, help='{rtt_avg:miss_rate}')
        # parser.add_argument('--timeout', type=int)
        # parser.add_argument('--count', type=int)
        # parser.add_argument('--verbose', type=bool)

    def setUp(self, arguments):
        self.argument = Arguments(
            host=arguments.host,
            warning=Warning.creator(arguments.warning),
            error=Error.creator(arguments.error)
        )
        self.request = Request(target=arguments.host)

    def run(self):
        response = pythonping.ping(**attr.asdict(self.request))
        # TODO miss_rate
        # GitHub pythonping/commit/3b27565b19eb2d1be5582751db6975fb29e33bea
        failed = [x for x in response._responses if not x.success]
        miss_rate = round(len(failed) / self.request.count, 2)
        self.response = Response(
            rtt_avg=response.rtt_avg_ms, miss_rate=miss_rate,
            host=self.argument.host,
            warning=self.argument.warning,
            error=self.argument.error)

        if self.response.miss_rate > self.argument.error.miss_rate:
            raise exceptions.PluginError(
                f'ICMP Error. miss_rate: {self.response.miss_rate}')
        if self.response.rtt_avg > self.argument.error.rtt_avg:
            raise exceptions.PluginError(
                f'ICMP Error. rtt_avg: {self.response.rtt_avg}')
        if self.response.miss_rate > self.argument.warning.miss_rate:
            raise exceptions.PluginWarning(
                f'ICMP Warning. miss_rate: {self.response.miss_rate}')
        if self.response.rtt_avg > self.argument.warning.rtt_avg:
            raise exceptions.PluginWarning(
                f'ICMP Warning. rtt_avg: {self.response.rtt_avg}')

        return f'rtt_avg: {self.response.rtt_avg}, miss_rate: {self.response.miss_rate}'
