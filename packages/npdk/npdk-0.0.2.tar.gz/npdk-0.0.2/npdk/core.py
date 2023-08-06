import abc
import argparse
import sys
import traceback
import typing
from dataclasses import dataclass

import attr

from npdk import exceptions


@attr.s
class Record:
    result = attr.ib(default=None)
    message: str = attr.ib(default='success')
    status: str = attr.ib(default='OK')
    exit_code: int = attr.ib(default=0)


class PluginTestCase(abc.ABC):

    def __init__(self, test_name='Nagios Test Case'):
        self.record = Record()
        parser = argparse.ArgumentParser(prog=test_name)
        # parser.add_argument('--debug', action='store_const', const=True, default=False)
        self.add_arguments(parser)
        self.setUp(parser.parse_args())
        self.handle()

    def add_arguments(self, parser):
        '''Hook method for subclassed test to add custom arguments.'''
        pass

    @abc.abstractmethod
    def setUp(self, arguments):
        pass

    @abc.abstractmethod
    def tearDown(self):
        pass

    @abc.abstractmethod
    def run(self):
        pass

    def handle(self):
        try:
            self.record.message = self.run()
        except exceptions.PluginException as e:
            self.record.message = str(e)
            self.record.status = e.status
            self.record.exit_code = e.exit_code
        except Exception as e:
            self.record.message = str(e)
            self.record.status = 'Other'
            self.record.exit_code = 3
        finally:
            try:
                self.record.result = self.response
                self.tearDown()
            except Exception as e:
                self.record.message = str(e) + ':=' + self.record.message
                self.record.status = 'TearDown Error'
                self.record.exit_code = 3

        # For Nagios
        print(f'[{self.record.status}] {self.record.message}')
        sys.exit(self.record.exit_code)
