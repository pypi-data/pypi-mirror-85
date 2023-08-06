#!/usr/bin/env python

import sys
import concurrent.futures
import CheckSSL as cssl


def prepare_host_list() -> list:
    args_hosts = sys.argv[1:]
    hosts = list()
    for item in args_hosts:
        hps = item.split(":")
        hosts.append((hps[0], int(hps[1]) if len(hps) == 2 else 443))
    return hosts


def print_basic_info(hostinfo):
    s = '''» {hostname} « … {peername}
    \tcommonName: {commonname}
    \tSAN: {SAN}
    \tissuer: {issuer}
    \tnotBefore: {notbefore}
    \tnotAfter:  {notafter}
    '''.format(
            hostname=hostinfo.hostname,
            peername=hostinfo.peername,
            commonname=cssl.get_common_name(hostinfo.cert),
            SAN=cssl.get_alt_names(hostinfo.cert),
            issuer=cssl.get_issuer(hostinfo.cert),
            notbefore=hostinfo.cert.not_valid_before,
            notafter=hostinfo.cert.not_valid_after
    )
    print(s)


def check_it_out(hostname, port):
    hostinfo = cssl.get_certificate(hostname, port)
    print_basic_info(hostinfo)


if __name__ == '__main__':
    HOSTS = prepare_host_list()
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as e:
        for hostinfo in e.map(lambda x: cssl.get_certificate(x[0], x[1]), HOSTS):
            print_basic_info(hostinfo)
