# -*- coding: utf-8 -*-
"""
# @Project  :demo
# @File     :mitmproxy.py
# @Author   :sxzhang1
# @Date     :2023/10/11 11:11
# @Desc     :mitmproxy>=10.1.1
            mitmproxy_url:https://docs.mitmproxy.org/stable/
            mitmproxy_blog:https://zhuanlan.zhihu.com/p/371209542?utm_id=0
            mitmproxy_blog:https://www.wenjiangs.com/doc/6rzvlmcm
"""
import inspect
import os
from typing import Sequence

from mitmproxy import addonmanager, flow
from mitmproxy.proxy import layer


class EventsBase:

    def __init__(self, logger=None):
        """
        监听主机包的基础类，存在一些通用方法
        """
        self.logger = logger
        self.name = self.__class__.__name__

    @staticmethod
    def add_star(func):
        def add_print(*args, **kwargs):
            columns = os.get_terminal_size().columns
            print("*" * int(columns))
            print("[功能说明({0})：{1}]\n".format(func.__name__, inspect.getdoc(func).split(":")[0].strip()))
            func(*args, **kwargs)

        return add_print

    def get_class_name(self):
        return self.__class__.__name__

    def load(self, loader: addonmanager.Loader) -> None:
        """
        在第一次加载加载项时调用。此事件接收Loader对象，该对象包含用于添加选项和命令。这个方法是插件配置自身的地方。
        :return:
        """
        pass

    @staticmethod
    def running() -> None:
        """
        当代理完全启动并运行时调用。在这一点上，您可以期望加载所有插件，并要设置的所有选项。
        :return:
        """
        pass

    def configure(self, updated: set) -> None:
        """
        在配置更改时调用。更新后的参数是一个类似集合的对象，包含所有
        更改了选项。此事件在启动期间调用，其中包含更新集中的所有选项。
        :param updated:
        :return:
        """
        pass

    @staticmethod
    def done() -> None:
        """
        当加载项关闭时调用，无论是从mitmproxy实例中删除，还是在mitmproxy时
        它本身就关闭了。关闭时，在事件循环终止后调用此事件，以保证
        将是插件看到的最后一个事件。请注意，日志处理程序此时已关闭，因此调用log
        函数将不产生输出。
        :return:
        """
        pass

    def update(self, flows: Sequence[flow.Flow]) -> None:
        """
         当一个或多个 flow 对象被修改了，通常是来自一个不同的 addon。
        :param flows:
        :return:
        """
        pass

    @staticmethod
    def next_layer(data_flow: layer.NextLayer) -> None:
        """
        正在切换网络层。您可以通过设置data.layer来更改将使用的图层。
        （默认情况下，这是由mitmproxy.addons.NextLayer完成的）
        :param data_flow:
        :return:
        """
        pass
        # print("正在切换网络层:{0}".format(data_flow.layer.context))
