import unittest
import json

from unittest.mock import patch

from windowsdnsserver.command_runner.runner import Result
from windowsdnsserver.dns.dnsserver import DnsServerModule
from windowsdnsserver.dns.record import RecordType
from windowsdnsserver.util.dns_server_utils import parse_ttl, format_ttl


class TestDnsServerUtils(unittest.TestCase):

    def test_convert_dns_server(self):
        mock_data = self.load_mock_data()

        with patch('windowsdnsserver.dns.dnsserver.DnsServerModule.run') as mock:
            mock.return_value = Result(True, 0, mock_data['GetDnsServerResponse1'], '')

            dns = DnsServerModule()
            results = dns.get_dns_records("zone")
            print(results)
            self.assertEqual(len(results), 1)

            result = results[0]
            self.assertEqual(result.zone, "zone")
            self.assertEqual(result.name, "@")
            self.assertEqual(result.type, RecordType.A)
            self.assertEqual(result.content, '34.65.234.38')

    def test_parse_ttl(self):
        def mock_time_to_live(h, m, s):
            mock = dict()

            mock['Hours'] = h

            mock['Minutes'] = m

            mock['Seconds'] = s
            return mock

        self.assertEqual(parse_ttl(mock_time_to_live(1, 23, 50)), '1h 23m 50s')

        self.assertEqual(parse_ttl(mock_time_to_live(0, 23, 50)), '23m 50s')
        self.assertEqual(parse_ttl(mock_time_to_live(1, 0, 50)), '1h 50s')
        self.assertEqual(parse_ttl(mock_time_to_live(1, 23, 0)), '1h 23m')
        self.assertEqual(parse_ttl(mock_time_to_live(1, 50, 2)), '1h 50m 2s')

    def test_format_ttl(self):
        self.assertEqual(format_ttl('10h 20m 30s'), '10:20:30')
        self.assertEqual(format_ttl('10h 30s'), '10:00:30')
        self.assertEqual(format_ttl('30s'), '00:00:30')
        self.assertEqual(format_ttl('20m 10h 30s'), '10:20:30')
        self.assertEqual(format_ttl('0s 10h 20m'), '10:20:00')

        with self.assertRaisesRegex(Exception, 'time unit could not be determined'):
            format_ttl('10n')

        with self.assertRaisesRegex(AssertionError, "empty ttl value"):
            format_ttl('')

        with self.assertRaises(AssertionError):
            format_ttl(111)

        with self.assertRaises(Exception):
            format_ttl('10h 20m 30')

        with self.assertRaises(Exception):
            format_ttl('10h 20')

        with self.assertRaises(Exception):
            format_ttl('0h 0m 0s')

        self.assertEqual(format_ttl('0h 0m 1s'), '00:00:01')

        with self.assertRaisesRegex(AssertionError, 'hour can not be more than'):
            format_ttl('25h')

        with self.assertRaisesRegex(AssertionError, 'minute can not be more than'):
            format_ttl('90m')

        with self.assertRaisesRegex(AssertionError, 'seconds can not be more than'):
            format_ttl('100s')

    def load_mock_data(self):
        fd = open('/tests/mock_data.json')
        r = json.load(fd)
        fd.close()
        return r


if __name__ == '__main__':
    unittest.main()
