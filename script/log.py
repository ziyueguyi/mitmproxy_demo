# -*- coding: utf-8 -*-
"""
# @项目名称 :pytorch
# @文件名称 :new_log.py
# @作者名称 :sxzhang1
# @日期时间 :2024/2/29 13:25
# @文件介绍 :
"""
import inspect
import os
import re
import time
from datetime import datetime

from colorama import Fore, init


class LogLevel:
    """
    日志登记
    """

    def __init__(self):
        ...

    @property
    def critical(self):
        return 50

    @property
    def fatal(self):
        return 50

    @property
    def error(self):
        return 40

    @property
    def warning(self):
        return 30

    @property
    def warn(self):
        return 30

    @property
    def notice(self):
        return 25

    @property
    def info(self):
        return 20

    @property
    def debug(self):
        return 10

    @property
    def notset(self):
        return 0

    def get_label_of_level(self, level: int):
        """
        获取此数值所对应的日志登记
        :param level: 日志数值
        :return:
        """
        __levelToName = {
            self.critical: 'critical',
            self.error: 'error',
            self.warning: 'warning',
            self.info: 'info',
            self.debug: 'debug',
            self.notset: 'notset',
        }
        if level in __levelToName.keys():
            return __levelToName[level].upper()
        else:
            raise KeyError("不包含此键值：{0}".format(level))

    def get_level_by_label(self, level_label: str):
        """
        获取次日志所对应的数值
        :param level_label:日志登记
        :return:
        """
        __nameToLevel = {
            'critical': self.critical,
            'fatal': self.fatal,
            'error': self.error,
            'warn': self.warn,
            'warning': self.warning,
            'info': self.info,
            'debug': self.debug,
            'notset': self.notset,
        }
        if level_label in __nameToLevel.keys():
            return __nameToLevel[level_label.lower()]
        else:
            raise KeyError("不包含此键值：{0}".format(level_label))


class Logger(object):
    def __init__(self, title: str, log_dir: str = None, **kwargs):
        """
        日志
        :param title:日志名称
        :param log_dir: 日志路径，
        :param file_level: 日志等级
        :param categorize:路径是否包含title
        :param date_rotate:是否添加日期路径
        :param print_level:控制台打印的最低等级
        :param record_millisecond:日志时间是否包含毫秒
        :param file_encoding:日志编码，默认为
        :param is_color:控制台输出是否彩色输出
        """
        self.__log_level = LogLevel()
        self.params = {'title': title, 'log_dir': log_dir}
        self.params.update(kwargs)
        self.__init_params()

    def get_dt(self):
        return datetime.now().strftime(self.params["datetime_format"])

    def __init_params(self):
        """
        初始化参数
        """
        if not self.params.get("title"):
            raise ValueError("日志标题不能为空")
        self.params["date_rotate"] = self.params.get("date_rotate", False)
        self.params["log_dir"] = self.params.get("log_dir", os.path.join(os.getcwd(), "log"))
        self.params["print_level"] = self.params.get("print_level", self.__log_level.notset)
        self.params["file_level"] = self.params.get("file_level", self.__log_level.notset)
        self.params["is_color"] = self.params.get("is_color", False)
        self.params["file_encoding"] = self.params.get("file_encoding", "utf-8")
        self.params["datetime_format"] = self.params.get("datetime_format", "%Y-%m-%d %H:%M:%S")
        self.params["format"] = self.params.get("format", "[datetime] [[func_name]]|<[log_level]>|([lineno]):[message]")
        self.params_dict = {
            "[datetime]": self.get_dt(),
            "[func_name]": self.get_func_name(),
            "[lineno]": self.get_line(),
            "[log_level]": "",
            "[message]": "[message]",
        }
        init()

    def get_file_handler(self, log_level="debug"):
        """
        获取文件句柄
        :return:
        """
        if self.params.get("log_dir"):
            today = ""
            if self.params.get("date_rotate"):
                localtime = time.localtime()
                today = os.path.join(str(localtime.tm_year), str(localtime.tm_mon), str(localtime.tm_mday))
            filepath = os.path.join(self.params.get("log_dir"), today)
            os.makedirs(filepath, exist_ok=True)
            filepath = os.path.join(filepath, "{0}.{1}".format(self.params.get("title"), log_level.lower()))
            file = open(filepath, 'a', encoding=self.params.get("file_encoding"))
            return file
        else:
            return None

    @staticmethod
    def get_thread():
        """
        获取线程信息
        :return:
        """
        ...

    @staticmethod
    def get_process():
        """
        获取进程信息
        :return:
        """
        ...

    def get_func_name(self):
        """
        获取当前调用栈
        :return:
        """
        caller_locals = inspect.currentframe().f_back.f_back.f_back.f_locals
        caller_class_name = caller_locals.get('self', self).__class__.__name__
        return caller_class_name

    @staticmethod
    def get_line():
        """
        获取行号信息
        :return:
        """
        frame = inspect.currentframe().f_back.f_back
        return str(frame.f_lineno)

    @property
    def log_dir(self):
        return self.params.get("log_dir")

    @log_dir.setter
    def log_dir(self, log_dir: str):
        self.params["log_dir"] = log_dir

    @property
    def date_rotate(self):
        return self.params.get("date_rotate")

    @date_rotate.setter
    def date_rotate(self, date_rotate: str):
        self.params["date_rotate"] = date_rotate

    @property
    def is_color(self):
        return self.params.get("is_color")

    @is_color.setter
    def is_color(self, is_color: bool):
        self.params["is_color"] = is_color

    @property
    def format(self):
        return self.params.get("format")

    @format.setter
    def format(self, message_format: str):
        self.params["format"] = message_format

    def __del__(self):
        ...

    def format_message(self, log_level, message, extra, end=os.linesep):
        """
        格式化信息
        :param log_level:
        :param message:
        :param extra:
        :param end:
        :return:
        """
        format_str = self.params.get("format")
        self.params_dict["[log_level]"] = "{0:->8s}".format(self.__log_level.get_label_of_level(log_level))
        for fs in re.findall("(\\[\\w+])", format_str):
            format_str = format_str.replace(fs, self.params_dict.get(fs))
        message = "{0}|{1}".format(message, extra)
        format_str = format_str.replace("[message]", message)
        if log_level >= self.params.get("file_level"):
            __open_file = self.get_file_handler(self.__log_level.get_label_of_level(log_level))
            __open_file.write(format_str + end)
            __open_file.flush()
            __open_file.close()
        if log_level >= self.params.get("print_level"):
            color_dict = {
                50: Fore.LIGHTMAGENTA_EX,
                40: Fore.LIGHTRED_EX,
                30: Fore.LIGHTYELLOW_EX,
                25: Fore.LIGHTBLUE_EX,
                20: Fore.LIGHTGREEN_EX,
                10: Fore.LIGHTWHITE_EX,
                0: Fore.WHITE,
            }
            message = color_dict[log_level] + format_str + Fore.RESET if self.is_color else format_str
            print(message, end=end)

    def notset(self, message, extra=None):
        """

        :param message:
        :param extra:
        :return:
        """
        self.format_message(self.__log_level.notset, message, extra)

    def debug(self, message, extra=None):
        """

        :param message:
        :param extra:
        :return:
        """
        self.format_message(self.__log_level.debug, message, extra)

    def info(self, message, extra=None):
        """

        :param message:
        :param extra:
        :return:
        """
        self.format_message(self.__log_level.info, message, extra)

    def warning(self, message, extra=None):
        """

        :param message:
        :param extra:
        :return:
        """
        self.format_message(self.__log_level.warning, message, extra)

    def warn(self, message, extra=None):
        """

        :param message:
        :param extra:
        :return:
        """
        self.format_message(self.__log_level.warn, message, extra)

    def error(self, message, extra=None):
        """

        :param message:
        :param extra:
        :return:
        """
        self.format_message(self.__log_level.error, message, extra)

    def fatal(self, message, extra=None):
        """

        :param message:
        :param extra:
        :return:
        """
        self.format_message(self.__log_level.fatal, message, extra)

    def critical(self, message, extra=None):
        """
        致命错误
        :param message:
        :param extra:
        :return:
        """
        self.format_message(self.__log_level.critical, message, extra)
