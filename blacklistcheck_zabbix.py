#!/usr/bin/python
#
# Author: Rene Diepstraten <rene@pcextreme.nl>
# Update: Robert Selaru <robert@pcextreme.nl>


from rblwatch import RBLSearch
import socket, ipaddress
import sys


# Returns
#  1 when listed
#  0 when not listed
#  2 when input is neither an IP or a hostname.


EXCEPTIONS = []
# TEST with ips from: https://myip.ms/browse/blacklist/


def check_ip(ip):
    listed = []

    searcher = RBLSearch(ip)

    for blacklist, report in searcher.listed.items():
        if isinstance(report, dict) and report['LISTED'] == True:
            if blacklist not in EXCEPTIONS:
                listed.append(blacklist)

    return set(listed)


def check_input(input):
    if not input:
        return []

    try:
        ipaddress.ip_address(input)
        output = [input]
        return output
    except:
        try:
            ips = set([r[4][0] for r in socket.getaddrinfo(input, None, 0, 1)])
            return ips
        except socket.error:
            print(2)
            sys.exit(1)


def usage():
    print('''
Usage: {} <hostname>

Checks <hostname> for listed RBLs, backscatterer excluded.
'''.format(sys.argv[0].split('/')[-1]))


def main():
    try:
        targets = sys.argv[1:]
    except IndexError:
        usage()
        sys.exit()

    rbls = list()
    for target in targets:
        for ip in check_input(target):
            for rbl in check_ip(ip):
                rbls.append((ip, rbl))

    if rbls:
        print(1)
    else:
        print(0)


if __name__ == '__main__':
    main()