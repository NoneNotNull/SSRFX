# /usr/bin/env python
# coding=utf-8


import re
import sys
import argparse
from IPy import IP, IPSet

def get_args():
    """
    :return: 返回参数信息
    """
    parser = argparse.ArgumentParser(description="SSRF Explotion Tools")
    parser.add_argument("--url", metavar="URL", help="Input the url u want to attack")
    parser.add_argument("--threads", type=int, help="Input the threads u want to set", default=10)
    parser.add_argument("--app", help="Input the website type,such as :weblogic", default="")
    parser.add_argument("--network", help="The internal network to scan,network[,network[,network]]")
    parser.add_argument("--type", help="Attack type,such as : portscan or livedetect", default="livedetect")
    parser.add_argument("--vulapp", help="vulnerable app,such as redis")
    parser.add_argument("--lhost", help="local host ip address")
    parser.add_argument("--lport", help="local host port")
    parser.add_argument("--rhost", help="remote host ip address")
    parser.add_argument("--rport", help="remote host port")
    if len(sys.argv) == 1:
        sys.argv.append("-h")
    args = parser.parse_args()  # 增加-h参数之后，最后就会exit
    check_args(args)
    return args

def check_args(args):
    """
    检测参数的格式是否正确，并进行处理
    :param args:
    :return:
    """
    if not args.url:
        msg = "U must set the url paramater!Such as:http://www.example.com"
        raise Exception(msg)
    if args.url:
        url = args.url
        url_regex = re.compile(
                r'^(?:http|ftp)s?://'
                r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+(?:[A-Z]{2,6}\.?|[A-Z0-9-]{2,}\.?)|'
                r'localhost|'
                r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'
                r'(?::\d+)?'
                r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        if not url_regex.match(url):
            msg = "The url format is not right!"
            raise Exception(msg)
        host_regex = re.compile(r'^https?://(.*?)/')
        match = host_regex.match(url)
        if match:
            args.host = match.group(1)
        else:
            msg = "Something went wrong"
            raise Exception(msg)

    if args.network:
        network = args.network.split(",")
        args.network = []
        for net in network:
            net = IP(net)
            for ip in net:
                args.network.append(ip.strNormal(0))

    if args.type == "getshell":
        if args.lhost and args.lport and args.rhost and args.rport:
            pass
        else:
            msg = "When you want to get shell,u should set the remote and local address:port"
            raise Exception(msg)
