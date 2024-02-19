# -*- coding: utf-8 -*-
"""
# @项目名称 :mitmproxy_demo
# @文件名称 :deal_message.py
# @作者名称 :sxzhang1
# @日期时间 :2024/1/23 17:34
# @文件介绍 :
"""
import sqlite3
import queue
import time


class MessageDict:
    def __init__(self, agreement, url, request_headers, request_body, response_headers, response_body, message):
        self._agreement = agreement
        self._url = url
        self._request_headers = request_headers
        self._request_body = request_body
        self._response_headers = response_headers
        self._response_body = response_body
        self._message = message

    @property
    def agreement(self):
        return self._agreement

    @agreement.setter
    def agreement(self, agreement):
        if not isinstance(agreement, str):
            pass
        else:
            self._agreement = agreement

    @property
    def url(self):
        return self._url

    @url.setter
    def url(self, url):
        if not isinstance(url, str):
            pass

    @property
    def request_headers(self):
        return self._request_headers

    @request_headers.setter
    def request_headers(self, request_header):
        if not isinstance(request_header, str):
            pass

    @property
    def request_body(self):
        return self._request_body

    @request_body.setter
    def request_body(self, request_body):
        if not isinstance("", str):
            pass

    @property
    def response_headers(self):
        return self._response_headers

    @response_headers.setter
    def response_headers(self, response_headers):
        pass

    @property
    def response_body(self):
        return self._response_body

    @response_body.setter
    def response_body(self, response_body):
        pass

    @property
    def message(self):
        return self._message

    @message.setter
    def message(self, message):
        pass

    def __iter__(self):
        return self


# 把获取到的数据存进数据库,写入数据线程类WriteThread。
class WriteThread():
    def __init__(self):
        super(WriteThread, self).__init__()
        self.queue = queue.Queue()  # 定义自身队列
        self.conn = sqlite3.connect("datebase.db", check_same_thread=False)
        self.cn = self.conn.cursor()
        self.create_tb()
        self.field_dict = {
            "id": "bigint auto_increment primary key",
            # 创建时间
            "crt_time": "DATETIME DEFAULT CURRENT_TIMESTAMP",
            # 协议
            "agreement": "varchar(20) NOT NULL",
            # 链接
            "url": "text NOT NULL",
            # 请求头
            "request_headers": "text",
            "request_body": "text",
            "response_headers": "text",
            "response_body": "text",
            "message": "text not null"
        }

    def create_tb(self):
        self.cn.execute("""CREATE TABLE IF NOT EXISTS Inter_Info(
                                id bigint auto_increment primary key,
                                crt_time DATETIME DEFAULT CURRENT_TIMESTAMP,-- 创建时间
                                agreement varchar(20) NOT NULL ,-- 协议
                                url text NOT NULL, --链接
                                request_headers text ,--请求头
                                request_body text ,--请求体
                                response_headers text ,--响应头
                                response_body text ,--响应体
                                message text not null    -- 抖音订单id 
                            )
                        """)
        self.conn.commit()
        time.sleep(15)

    def run(self):
        """
        """

        while True:
            list_data = self.queue.get()  # 实时获取数据
            md = MessageDict(*list_data)
            # 插入数据库
            self.cn.execute("insert into Inter_Info({0}}) values('{1}')".format(*md))
            self.conn.commit()
            time.sleep(15)

    def start(self):
        pass


if __name__ == '__main__':
    wt = WriteThread()
    wt.start()
