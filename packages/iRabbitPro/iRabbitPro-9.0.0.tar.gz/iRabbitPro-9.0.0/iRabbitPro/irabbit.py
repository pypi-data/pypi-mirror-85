#!/usr/bin/python
# -*- coding: utf-8 -*-
import random
import requests
from requests.adapters import HTTPAdapter
import re

import sys
import time
import hashlib


def randomIP():
    a = random.sample(list(range(1, 256)) * 4, 4)
    b = map(str, a)
    ip = '.'.join(b)
    return ip


def get_fake_headers():
    fakeHeaders = {"X-Forwarded-For": randomIP() + ',' + randomIP() + ',' + randomIP(), "X-Forwarded": randomIP(),
                   "Forwarded-For": randomIP(), "Forwarded": randomIP(),
                   "X-Forwarded-Host": randomIP(), "X-remote-IP": randomIP(),
                   "X-remote-addr": randomIP(), "True-Client-IP": randomIP(),
                   "X-Client-IP": randomIP(), "Client-IP": randomIP(), "X-Real-IP": randomIP(),
                   "Ali-CDN-Real-IP": randomIP(), "Cdn-Src-Ip": randomIP(), "Cdn-Real-Ip": randomIP(),
                   "X-Cluster-Client-IP": randomIP(),
                   "WL-Proxy-Client-IP": randomIP(), "Proxy-Client-IP": randomIP(),
                   "Fastly-Client-Ip": randomIP(), "True-Client-Ip": randomIP()
                   }
    return fakeHeaders


def get_random_string(num=32):
    ran_str = ''.join(random.sample('ABCDEFGHJKMNPQRSTWXYZabcdefhijkmnprstwxyz2345678', num))
    return ran_str


def get_random_mobile():
    prelist = ["130", "131", "132", "133", "134", "135", "136", "137", "138", "139", "147", "150", "151", "152",
               "153", "155", "156", "157", "158", "159", "186", "187", "188"]
    return random.choice(prelist) + "".join(random.choice("0123456789") for i in range(8))


def get_random_nick_and_avatar():
    nickName = ''
    try:
        while nickName == '':
            QQ = random.randint(888888, 99999999)
            avatar = 'http://q1.qlogo.cn/g?b=qq&nk={QQ}&s=100'.format(QQ=QQ)
            url = 'https://r.qzone.qq.com/fcg-bin/cgi_get_portrait.fcg?uins={QQ}'.format(QQ=QQ)
            try:
                resp = requests.get(url, timeout=3)
                nickName = re.findall('0,0,0,"(.*?)"', resp.content.decode('gbk'))[0]
            except Exception as e:
                pass
        return nickName, avatar
    except Exception as e:
        print(e)
        return '', ''


class RabbitHttp:
    def __init__(self, timeout=5, post_headers={}, get_headers={}, cookies={}, fake_ip=True, ):
        """
        :param timeout: : 每个请求的超时时间
        :param post_headers: POST协议头
        :param get_headers: GET协议头
        :param fake_ip: 是否开启随机ip
        """
        self.cookies = cookies
        self.get_headers = get_headers
        self.post_headers = post_headers
        s = requests.Session()
        #: 在session实例上挂载Adapter实例, 目的: 请求异常时,自动重试
        s.mount('http://', HTTPAdapter(max_retries=3))
        s.mount('https://', HTTPAdapter(max_retries=3))

        #: 设置为False, 主要是HTTPS时会报错, 为了安全也可以设置为True
        s.verify = True

        #: 公共的请求头设置
        fakeHeaders = {"X-Forwarded-For": randomIP() + ',' + randomIP() + ',' + randomIP(), "X-Forwarded": randomIP(),
                       "Forwarded-For": randomIP(), "Forwarded": randomIP(),
                       "X-Forwarded-Host": randomIP(), "X-remote-IP": randomIP(),
                       "X-remote-addr": randomIP(), "True-Client-IP": randomIP(),
                       "X-Client-IP": randomIP(), "Client-IP": randomIP(), "X-Real-IP": randomIP(),
                       "Ali-CDN-Real-IP": randomIP(), "Cdn-Src-Ip": randomIP(), "Cdn-Real-Ip": randomIP(),
                       "X-Cluster-Client-IP": randomIP(),
                       "WL-Proxy-Client-IP": randomIP(), "Proxy-Client-IP": randomIP(),
                       "Fastly-Client-Ip": randomIP(), "True-Client-Ip": randomIP()
                       }
        if fake_ip:
            post_headers.update(fakeHeaders)
            get_headers.update(fakeHeaders)

        #: 挂载到self上面
        self.s = s
        self.s.timeout = timeout

    def get(self, url):
        """GET

        :param url:
        :param query_dict: 一般GET的参数都是放在URL查询参数里面
        :return:
        """
        print('GET==>' + url)
        return self.s.get(url, headers=self.get_headers)

    def post(self, url, form_data=None, body_dict=None):
        """POST

        :param url:
        :param form_data: 有时候POST的参数是放在表单参数中
        :param body_dict: 有时候POST的参数是放在请求体中(这时候 Content-Type: application/json )
        :return:
        """
        if form_data:
            print('POST==>' + url)
            print('DATA==>', str(form_data))
            return self.s.post(url, data=form_data, headers=self.post_headers, cookies=self.cookies)
        if body_dict:
            print('POST==>' + url)
            print('JSON==>', str(body_dict))
            return self.s.post(url, json=body_dict, headers=self.post_headers, cookies=self.cookies)

    def __del__(self):
        """当实例被销毁时,释放掉session所持有的连接

        :return:
        """
        if self.s:
            self.s.close()


if __name__ == '__main__':
    pass
