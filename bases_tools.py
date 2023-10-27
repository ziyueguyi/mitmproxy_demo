# -*- coding: utf-8 -*-
"""
# @Project  :mitmproxy_demo
# @File     :bases_tools.py
# @Author   :sxzhang1
# @Date     :2023/10/25 17:54
# @Desc     :
"""
import importlib
import inspect
import os

from events_base import EventsBase


class BasesTools:
    def __init__(self):
        """
        工具类
        """
        self._ignore_class = list()
        self._class_set = set()

    def __get_child_class(self):
        """
        通过循环处理子类并进行调用
        :return:
        """
        current_path = os.path.dirname(os.path.abspath(__file__))
        current_files = [f.split('.')[0] for f in os.listdir(current_path) if f.endswith(".py")
                         and os.path.isfile(os.path.join(current_path, f))]
        for f in current_files:
            module = importlib.import_module(f)
            for name, sub in inspect.getmembers(module):
                if inspect.isclass(sub):  # 类别是class，并且父类是A
                    if sub.__bases__[0].__name__ == EventsBase.__name__:
                        self._class_set.add(sub())

    def __sel_child_class(self):
        """
        根据匹配顾泽对所选类进行移除
        :return:
        """
        new_set = set()
        for cs in self._class_set:
            if cs.name in self._ignore_class:
                new_set.add(cs)
        self._class_set -= new_set

    @property
    def class_set(self):
        return self._class_set

    @class_set.getter
    def class_set(self):
        self.__child_class()
        return self._class_set

    @property
    def ignore_class(self):
        return self._ignore_class

    @ignore_class.setter
    def ignore_class(self, value):
        if isinstance(value, list):
            self._ignore_class = value

    @ignore_class.getter
    def ignore_class(self):
        return self._ignore_class

    def __child_class(self):
        """
        获取子类
        :return:
        """
        self.__get_child_class()
        self.__sel_child_class()
