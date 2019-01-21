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
    def cc_kuaidaili(self, page=20):

        for n in range(1, page):

            html = self.get('https://www.kuaidaili.com/free/inha/%s/' % n)

            if html == False: continue

            ptn = r'data-title="IP">(.*?)</td>[\s\S]*?<td data-title="PORT">(.*?)<'

            ips = re.findall(ptn, html)

            if not ips:

                print('匹配失败:[%s]' % ptn)
                break

            ips = ['%s:%s' % (ip[0], ip[1]) for ip in ips]

            self.__Proxy_ip_list.extend(ips)

            self.sleep(5)

        return self.__Proxy_ip_list

    #2
    def cc_xicidaili(self, page = 3):

        urls = ['https://www.xicidaili.com/nt/%s' % n for n in range(1,page)]

        for url in urls:

            html= self.get(url)

            if html == False: continue

            ptn  = r'<td>(\d+\.\d+\.\d+\.\d+?)</td>[\s\S]*?<td>(\d+?)</td>[\s\S]*?<a'

            ips = re.findall(ptn, html)

            if not ips:

                print('匹配失败:[%s]' % ptn)
                break

            ips = ['%s:%s' %(ip[0], ip[1]) for ip in ips]

            self.__Proxy_ip_list.extend(ips)

            self.sleep(3)

        return self.__Proxy_ip_list

    #3
    def cc_31f(self):

        html = self.get('http://31f.cn/')

        if html == False: return []

        ptn = r'<td>(\d+\.\d+\.\d+\.\d+?)</td>\n<td>(\d+?)</td>'

        ips = re.findall(ptn, html)

        if not ips:

            print('匹配失败:[%s]' % ptn)
            return []

        ips = ['%s:%s' % (ip[0], ip[1]) for ip in ips]

        self.__Proxy_ip_list.extend(ips)

        return self.__Proxy_ip_list

    #4
    def cc_89ip(self):

        url = 'http://www.89ip.cn/tqdl.html?api=1&num=500&port=&address=&isp='

        html= self.get(url)

        if html == False: return []

        ptn = r'(\d+\.\d+\.\d+\.\d+:\d+)'

        ips = re.findall(ptn, html)

        if not ips:
            print('匹配失败:[%s]' % ptn)
            return []

        self.__Proxy_ip_list.extend(ips)

        return self.__Proxy_ip_list

    #5
    def cc_free(self):

        url = 'http://lab.crossincode.com/proxy/'

        html = self.get(url)

        if html == False: return []

        pattern = r'<td>(\d+\.\d+\.\d+\.\d+?)</td>[\s\S]*?<td>(\d+?)</td>'

        ips = re.findall(pattern, html)

        ips = ['%s:%s' % (ip[0], ip[1]) for ip in ips]

        if not ips:

            print('匹配失败:[%s]' % pattern)
            return []

        self.__Proxy_ip_list.extend(ips)

        return self.__Proxy_ip_list


if __name__ == '__main__':

    cra = Spider()

    ss = cra.cc_free()

    print(len(ss))

    print(ss)
