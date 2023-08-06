from collections.abc import Iterable

from ..dns.record import Record, RecordType


def format_ttl(ttl):
    """
    format_ttl converts given ttl string to Windows-DnsServer module's
    time to live format.

    "1h" -> 01:00:00 # a hour

    "30m" -> 00:30:00 # half an hour

    "1h 30m" -> 01:30:00 # an hour and half an hour

    "1h 30m 45s" -> 01:30:45 # an hour, 30 minutes and 45 seconds

    At least one time unit must be provided

    :param ttl: time to live
    :return: formatted time to live for Windows-DnsServer module
    """
    assert isinstance(ttl, str)
    assert len(ttl) > 0, "empty ttl value"

    hour = 0
    minute = 0
    seconds = 0

    units = ttl.split(' ')
    for unit in units:
        if 'h' in unit:
            hour = int(unit[:-1])
            continue
        elif 'm' in unit:
            minute = int(unit[:-1])
            continue
        elif 's' in unit:
            seconds = int(unit[:-1])
            continue

        raise Exception("time unit could not be determined [%s]" % unit)

    assert hour < 24, 'hour can not be more than 23'
    assert minute < 60, 'minute can not be more than 59'
    assert seconds < 60, 'seconds can not be more than 59'

    assert hour >= 0 and minute >= 0 and seconds >= 0, 'Time unit can not be negative'
    assert hour > 0 or minute > 0 or seconds > 0, 'At least one time unit must be provided'

    return '%02d:%02d:%02d' % (hour, minute, seconds)


def parse_ttl(time_to_live):
    """

    :param time_to_live: DnsServer module's TimeToLive object
    :return: Windows DNS Server ttl format
    """
    hours = time_to_live['Hours']
    minutes = time_to_live['Minutes']
    seconds = time_to_live['Seconds']

    ttl_str = ''
    if hours:
        ttl_str += '%sh ' % hours

    if minutes:
        ttl_str += '%sm ' % minutes

    if seconds:
        ttl_str += '%ss ' % seconds

    return ttl_str[:-1]


def is_record_type_supported(recordType):
    return recordType in RecordType.list()


def transform_dns_server_result(zone, cmdlet_results):
    if not isinstance(cmdlet_results, list):
        cmdlet_results = [cmdlet_results]

    record_results = []
    for result in cmdlet_results:
        name = result['HostName']
        record_type = result['RecordType']

        if not is_record_type_supported(record_type):
            continue

        record_data_props = result['RecordData']['CimInstanceProperties']

        record_data = dict()
        if isinstance(record_data_props, str):
            key, value = record_data_props.split('=')
            # value's has quotes at beginning and end of value -- remove it
            record_data[key.strip()] = value[1:-1]
        else:
            for props in record_data_props:
                key, value = props.split('=')
                record_data[key.strip()] = value

        assert len(record_data) < 2, "Unexpected data record, expected only one property, actual: [%s]" % record_data

        content = next(iter(record_data.values()))
        ttl = parse_ttl(result['TimeToLive'])

        record_results.append(Record(zone, name, RecordType.value_of(record_type), content, ttl))

    return record_results
