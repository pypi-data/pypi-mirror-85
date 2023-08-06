import unittest

from windowsdnsserver.dns.record import RecordType
from windowsdnsserver.util import dns_server_utils


class TestRecords(unittest.TestCase):

    def test_supported_record_types(self):
        self.assertTrue(dns_server_utils.is_record_type_supported('A'))
        self.assertTrue(dns_server_utils.is_record_type_supported('Txt'))

        self.assertFalse(dns_server_utils.is_record_type_supported('SOA'))
        self.assertFalse(dns_server_utils.is_record_type_supported('TXT'))

    def test_record_type_value_of(self):
        record_type_a = RecordType.value_of('A')

        self.assertEqual(RecordType.A, record_type_a)

        record_type_txt = RecordType.value_of('Txt')

        self.assertEqual(RecordType.TXT, record_type_txt)


if __name__ == '__main__':
    unittest.main()
