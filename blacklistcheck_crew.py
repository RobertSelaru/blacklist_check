#!/usr/bin/python
#
# Author: Rene Diepstraten <rene@pcextreme.nl>
# Update: Robert Selaru <robert@pcextreme.nl>
# Test with ips from  <https://myip.ms/browse/blacklist>

from rblwatch import RBLSearch
import socket, ipaddress
import sys

EXCEPTIONS = []

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
            print('Please insert a valip IP or a resolvable hostname.')
            sys.exit(1)


def usage():
    print('''
Usage: {} <hostname>/<ip>

Checks <hostname> or <ip> for listed RBLs.
'''.format(sys.argv[0].split('/')[-1]))


def main():
    try:
        target = sys.argv[1]
    except IndexError:
        usage()
        sys.exit()

    rbls = list()
    for ip in check_input(target):
        for rbl in check_ip(ip):
            rbls.append((ip, rbl))

    if rbls:
       for ip, blacklist in rbls:
           print(ip + ' is blacklisted on ' + blacklist)
    else:
        print(str(target) + ' is not blacklisted')


if __name__ == '__main__':
    main()