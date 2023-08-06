## windowsdnsserver-py

windowsdnsserver-py is a wrapper Python library for [DnsServer](https://docs.microsoft.com/en-us/powershell/module/dnsserver/?view=win10-ps) module.

Subprocess module is used to perform process calls to interact with DnsServer module.

## Features
 - Convenient as a Python library
 - Supports A and Txt record
 - Query DNS records

## Installation

```shell
pip install windowsdnserver-py
```

## Limitations
 - Python 3 supported, but Python 2 is not tested 
 - This library is not able to work remotely, currently, it is merely able to call DnsServer module on localhost. 
 Since, the remote session feature is not on the table, the software that uses this module
 must be installed on windows server where Windows Server/Dns Server is located.
