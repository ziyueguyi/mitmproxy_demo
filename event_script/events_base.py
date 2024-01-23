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
import importlib
import inspect
import os
import sys
from typing import Sequence

from mitmproxy import addonmanager, flow
from mitmproxy.proxy import layer


class EventsBase:
    """
    监听主机包的基础类，存在一些通用方法
    """

    def __init__(self, ignore_class: list = None, logger=None):
        if ignore_class:
            self.ignore_class = ignore_class
        self.logger = logger

        self.ignore_class = []

    @classmethod
    def __get_chile_class(cls, base_path=os.path.join(os.path.dirname(sys.argv[0]), "event_script")) -> list:
        """
        获取所有子类
        :return:
        """
        """动态获取继承的子类"""
        if os.path.isfile(base_path):
            _, file_name = os.path.split(base_path)
            if file_name.endswith(".py"):
                module = importlib.import_module("event_script.{0}".format(file_name.replace(".py", "")))
                for name, sub in inspect.getmembers(module):
                    if inspect.isclass(sub) and sub.__base__ == cls:  # 类别是class，并且父类是A
                        return [sub]
            return list()

        else:
            new_list = list()
            for fl in os.listdir(base_path):
                new_list.extend(cls.__get_chile_class(os.path.join(base_path, fl)))
            return new_list

    def get_child_class(self) -> list:
        """
        通过循环处理子类并进行调用
        :return:
        """
        return [cls_name(self.logger) for cls_name in self.__get_chile_class() if
                cls_name.__name__ not in self.ignore_class]

    def load(self, loader: addonmanager.Loader) -> None:
        """
        在第一次加载加载项时调用。此事件接收Loader对象，该对象包含用于添加选项和命令。这个方法是插件配置自身的地方。
        :return:
        """
        pass

    def running(self) -> None:
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

    def done(self) -> None:
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
