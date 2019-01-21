import re
from time import sleep, time
from httptools import HttpTools
from functions import *

class Spider(HttpTools):

    def __init__(self):
        '''初始化'''

        self.time  = time

        self.sleep = sleep

        self.methods = list(filter(lambda m: m.startswith("cc_"), dir(self)))

        self.__Proxy_ip_list = []

    #1
    def cc_usproxys1(self):

        url = 'https://www.us-proxy.org/'

        res = self.get(url)

        if not res: return []

        ptn = r'<td>(\d+\.\d+\.\d+\.\d+?)</td><td>(\d+?)</td>'

        ips = re.findall(ptn, res)

        if not ips:

            print('匹配失败:[%s]' % ptn)

            return []

        ips = ['%s:%s' % (ip[0], ip[1]) for ip in ips]

        self.__Proxy_ip_list.extend(ips)

        return self.__Proxy_ip_list

    #2
    def cc_proxynova(self):

        url = 'https://www.proxynova.com/proxy-server-list/country-us/'

        res = self.get(url)

        if not res: return []

        ptn = "write\('12345678([\d\.]+?)'\.substr\(8\)\s\+\s'([\d\.]+?)'\);</script>\s</abbr>[\s\S]*?</td>[\s\S]*?<td align=\"left\">([\s\S]+?)</td>"

        ips = re.findall(ptn, res)

        if not ips:

            print('匹配失败:[%s]' % ptn)

            return []

        for ip in ips:

            port  = ip[2].strip()

            port  = re.compile(r'<[^>]+>',re.S).sub('',port)

            proxy = '%s%s:%s' % (ip[0], ip[1], port)

            self.__Proxy_ip_list.append(proxy)

        return self.__Proxy_ip_list

    #3
    def cc_xroxy(self):

        url = 'http://www.xroxy.com/free-proxy-lists/'

        res = self.get(url)

        if not res: return []

        ptn = '<td tabindex="0" class="sorting_1">(\d+\.\d+\.\d+\.\d+?)</td>[\s\S]*?<td>(\d+?)</td>'

        ips = re.findall(ptn, res)

        if not ips:

            print('匹配失败:[%s]' % ptn)

            return []

        ips = ['%s:%s' % (ip[0], ip[1]) for ip in ips]

        self.__Proxy_ip_list.extend(ips)

        return self.__Proxy_ip_list

    #4
    def cc_gatherproxy(self, page = 3):

        url = 'http://www.gatherproxy.com/proxylist/country/?c=United%20States'

        for n in range(1, page):

            data={
                'Country': 'united states',
                'PageIdx': '%s' % n,
                'Filter':'',
                'Uptime': '0'
            }

            res = self.post(url,data=data)

            if not res: continue

            ptn = r"write\('(\d+\.\d+\.\d+\.\d+?)'\)</script></td>[\s\S]*?<td><script>document\.write\(gp\.dep\('([\dA-F]+?)'\)\)</script></td>"
            #提取数据
            ips = re.findall(ptn, res)

            if not ips:

                print('匹配失败:[%s]' % ptn)
                break

            #数据清洗
            ips = ['%s:%s' %(ip[0], int(ip[1], 16)) for ip in ips]

            self.__Proxy_ip_list.extend(ips)

            self.sleep(5)

        return self.__Proxy_ip_list

    #5
    def cc_hidemyna(self, page = 3):

        for n in range(0,page):

            url = 'https://hidemyna.me/en/proxy-list/?country=US&type=hs&start=%s#list' %(n*64)

            res = self.get(url)

            if not res: continue

            ptn = r'class=tdl>(\d\.\d\.\d\.\d+?)</td><td>(\d+)</td>'

            ips = re.findall(ptn, res)

            if not ips:

                print('匹配失败:[%s]' % ptn)
                break

            ips = ['%s:%s' %(ip[0],ip[1]) for ip in ips]

            self.__Proxy_ip_list.extend(ips)

            self.sleep(5)

        return self.__Proxy_ip_list

    #6
    def cc_sockslist(self, page = 3):

        for n in range(1,page):

            html = self.get('https://sockslist.net/proxy/server-socks-hide-ip-address/%s#proxylist' % n)

            if not html: continue

            str1 = re.findall(r'<\!\[CDATA\[([^\]]+?)\/', html)

            if not str1: break

            str1 = str1[0].replace(' ', '').strip().strip(';')
            lists= str1.split(';')

            #动态定义变量
            variable = locals()
            for items in lists:

                item = items.split('=')
                variable[item[0]] = eval(item[1] * 1)

            # ptn = r't_ip">(\d+\.\d+\.\d+\.\d+?)</td>[\s\S]*?write\((.*?)\);' #匹配全部
            ptn = r't_ip">(\d+\.\d+\.\d+\.\d+?)</td>[\s\S]*?write\((.*?)\);[\s\S]*alt="us"' #只匹配美国

            ips = re.findall(ptn, html)

            if not ips:

                print('匹配失败:[%s]' % ptn)
                continue

            for ip in ips:

                port = eval(ip[1]*1)

                proxy= '%s:%s' %(ip[0], port)

                self.__Proxy_ip_list.append(proxy)

            self.sleep(4)

        return self.__Proxy_ip_list

    #7
    def cc_apiproxy1(self):

        self.sleep(1)

        import json

        res = self.get('https://api.getproxylist.com/proxy')

        if not res: return []

        data= json.loads(res)

        ip  = '%s:%s'%(data.get('ip'),data.get('port'))

        self.__Proxy_ip_list.append(ip)

        return self.__Proxy_ip_list

    #8
    def cc_coolproxy(self,page = 3):

        import base64

        headers = {
            # 'Cookie':'__utmc=51815611; __utmz=51815611.1547904609.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __utma=51815611.1635626206.1547904609.1547904609.1547907825.2; __utmt=1; __utmb=51815611.1.10.1547907825',
            'Host': 'www.cool-proxy.net',
            # 'Upgrade-Insecure-Requests': '1',
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/71.0.3578.98 Safari/537.36'
        }

        for n in range(1, page):

            url = 'https://www.cool-proxy.net/proxies/http_proxy_list/country_code:US/port:/anonymous:/page:%s' % n

            res = self.get(url)

            if not res: continue

            ptn = r'str_rot13\("(.*?)"\)\)\)</script></td>[\s\S]*?<td>(\d+?)</td>'

            ips = re.findall(ptn, res)

            if not ips:

                print('匹配失败:[%s]' % ptn)

                continue

            for ip in ips:

                agent = base64.b64decode(rot13(ip[0])).decode('utf-8')

                proxy = '%s:%s' %(agent,ip[1])

                self.__Proxy_ip_list.append(proxy)

            self.sleep(5)

        return self.__Proxy_ip_list




if __name__ == '__main__':

    cra = Spider()
    sss = cra.cc_gatherproxy()
    print(len(sss))
    print(sss)
