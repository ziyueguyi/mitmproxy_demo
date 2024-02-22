# -*- coding: utf-8 -*-
"""
# @项目名称 :demo
# @文件名称 :new_log.py
# @作者名称 :sxzhang1
# @日期时间 :2024/1/18 10:10
# @文件介绍 :
"""
import importlib
import inspect
import json
import math
import os
import platform
import secrets
import string
import sys
import threading
import time
import traceback
import uuid
import warnings
from datetime import datetime
from colorama import init, Fore, Back, Style



class CommonHelper:
    def __init__(self):
        pass

    @staticmethod
    def read_target(target, keychain: tuple, default: any = None):
        if not keychain:
            return default

        c_target, empty = target.copy(), object()
        for i in keychain:
            if isinstance(c_target, dict):
                c_target = c_target.get(i, empty)
            elif isinstance(c_target, (tuple, list)):
                c_len = len(c_target)
                if isinstance(i, int) and -c_len <= i <= c_len - 1:
                    c_target = c_target[i]
                else:
                    c_target = empty
            else:
                break
        ret = default if c_target is empty else c_target
        return ret

    @classmethod
    def read_dictionary(cls, dictionary: dict, keychain: tuple, default: any = None):
        if len(keychain) <= 0:
            return default
        elif len(keychain) == 1:
            return dictionary.get(keychain[0], default)
        else:
            current_key = keychain[0]
            if dictionary.keys().__contains__(current_key):
                sub_dictionary = dictionary.get(current_key, None)
                if type(sub_dictionary) is dict:
                    return cls.read_dictionary(sub_dictionary, keychain[1:], default)
                elif type(sub_dictionary) is tuple or type(sub_dictionary) is list:
                    return cls.read_array(sub_dictionary, keychain[1:], default)
                else:
                    return default
            else:
                return default

    @classmethod
    def read_array(cls, array: tuple, keychain: tuple, default: any = None):
        if len(keychain) <= 0:
            return default
        elif len(keychain) == 1:
            current_key = int(keychain[0])
            if len(array) > current_key:
                return array[int(keychain[0])]
            else:
                return default
        else:
            current_key = int(keychain[0])
            if len(array) > current_key:
                sub_array = array[current_key]
                if type(sub_array) is tuple or type(sub_array) is list:
                    return cls.read_array(sub_array, keychain[1:], default)
                elif type(sub_array) is dict:
                    return cls.read_dictionary(sub_array, keychain[1:], default)
                else:
                    return default
            else:
                return default

    @classmethod
    def write_dictionary(cls, target_dict: dict, keychain: tuple, value: any):
        keychain_length = len(keychain)
        if keychain_length > 1:
            current_key = keychain[0]
            current_target = target_dict.get(current_key)
            if type(current_target) is not dict:
                target_dict[current_key] = {}
            cls.write_dictionary(target_dict[current_key], keychain[1:], value)
        elif keychain_length == 1:
            target_dict[keychain[0]] = value

        return target_dict

    @staticmethod
    def class_with_class_path(module_path: str, class_name: str = None):
        """
        Since 0.1.22
        Since 0.2.19 When the class name is the same with PY file name, `class_name` is optional.

        For a/b.py -> class b
        class_with_namespace is like 'package.sub_package.class', 'a.b'
        class_name is 'b'
        return a CLASS definition, to be used with parameters to make instance
        """
        module = importlib.import_module(module_path)
        if class_name is None:
            class_name = module_path.split('.')[-1]
        a_class = getattr(module, class_name)
        return a_class

    @staticmethod
    def class_with_module_and_name(module_base: str, sub_module_name: str):
        """
        Since 0.1.21
        Since 0.2.19 It is not so convinence to use, consider using `class_with_class_path`.

        For a/b.py -> class b
        module_base is a
        sub_module_name is b
        """
        warnings.warn('Use `class_with_class_path` instead.')

        module = __import__(module_base)
        a_class = getattr(module, sub_module_name)
        return a_class

    @staticmethod
    def generate_random_uuid_hex():
        """
        Generate a random UUID.
        Since 0.4.15
        """
        return uuid.uuid4().hex

    @classmethod
    def generate_a_password_string(cls, length=8, least_special_ascii_letters=-1, least_lower_case_letters=1,
                                   least_upper_case_letters=1, least_digits=1):
        """
        Since 0.4.21
        Parameters named as `least_*` are following one rule:
        - if it is less than 0, this kind of chars would not appear;
        - else, the total appearence count in generated password would be no less than it.
        The sum of them (if less than 0, count it as 0) should not be longer than `length`.
        """

        options = ''
        if least_lower_case_letters < 0:
            least_lower_case_letters = 0
        else:
            options += string.ascii_lowercase

        if least_upper_case_letters < 0:
            least_upper_case_letters = 0
        else:
            options += string.ascii_uppercase

        if least_digits < 0:
            least_digits = 0
        else:
            options += string.digits

        if least_special_ascii_letters < 0:
            least_special_ascii_letters = 0
        else:
            special = r"!#()*,-.:;<>@[]^_{}"
            options += special

        if least_upper_case_letters + least_lower_case_letters + least_digits + least_special_ascii_letters > length:
            raise RuntimeError("generate_secure_password error: check parameters")

        password = "".join(secrets.choice(options) for _ in range(length))

        total_s = 0
        total_l = 0
        total_u = 0
        total_d = 0
        for c in password:
            if c.islower():
                total_l += 1
            elif c.isupper():
                total_u += 1
            elif c.isdigit():
                total_d += 1
            else:
                total_s += 1

        if total_d >= least_digits \
                and total_u >= least_upper_case_letters \
                and total_l >= least_lower_case_letters \
                and total_s >= least_special_ascii_letters:
            return password

        return cls.generate_a_password_string(
            length=length,
            least_special_ascii_letters=least_special_ascii_letters,
            least_lower_case_letters=least_lower_case_letters,
            least_upper_case_letters=least_upper_case_letters,
            least_digits=least_digits,
        )

    @staticmethod
    def get_python_version():
        """
        Since 0.4.25
        """
        return platform.python_version()

    @staticmethod
    def is_python_version_at_least(big_version: int, middle_version: int = 0, small_version: int = 0):
        """
        Since 0.4.25
        """
        x = platform.python_version_tuple()
        return int(x[0]) >= big_version and int(x[1]) >= middle_version and int(x[2]) >= small_version


class LoggingLevel:
    CRITICAL = 50
    FATAL = 50
    ERROR = 40
    WARNING = 30
    WARN = 30
    NOTICE = 25
    INFO = 20
    DEBUG = 10
    NOTSET = 0

    @classmethod
    def get_label_of_level(cls, level: int):
        if level == cls.DEBUG:
            return 'DEBUG'
        elif level == cls.INFO:
            return 'INFO'
        elif level == cls.NOTICE:
            return 'NOTICE'
        elif level == cls.WARN or level == cls.WARNING:
            return 'WARNING'
        elif level == cls.ERROR:
            return 'ERROR'
        elif level == cls.CRITICAL or level == cls.FATAL:
            return 'CRITICAL'
        else:
            return 'NOTSET'

    @classmethod
    def get_level_by_label(cls, level_label: str):
        if level_label == 'DEBUG':
            return cls.DEBUG
        elif level_label == 'INFO':
            return cls.INFO
        elif level_label == 'NOTICE':
            return cls.NOTICE
        elif level_label == 'WARN' or level_label == 'WARNING':
            return cls.WARNING
        elif level_label == 'ERROR':
            return cls.ERROR
        elif level_label == 'CRITICAL' or level_label == 'FATAL':
            return cls.CRITICAL
        else:
            return cls.NOTSET


class LoggerFile:
    """
    日志信息
    """

    def __init__(self, title='default', log_dir: str = None, log_level=None, categorize: bool = True,
                 date_rotate: bool = True, pht_tl=None, record_millisecond=False, file_encoding='utf-8',
                 is_color=True):
        """
        日志
        :param title:日志名称
        :param log_dir: 日志路径，
        :param log_level: 日志等级
        :param categorize:路径是否包含title
        :param date_rotate:是否添加日期路径
        :param pht_tl:控制台打印的最低等级
        :param record_millisecond:日志时间是否包含毫秒
        :param file_encoding:日志编码，默认为
        :param is_color:控制台输出是否彩色输出
        """
        self.categorize = categorize
        # 日志文件路径，如果包含路径及代表开启写入日志功能
        self.log_dir = log_dir
        # 日志名称
        self.title = title

        # This logic is since 0.4.19
        if self.categorize:
            x = title.split('/')
            last_title = None
            y = []
            for xx in x:
                if xx:
                    if last_title:
                        y.append(last_title)
                    last_title = xx
            if y and self.log_dir:
                self.log_dir = self.log_dir + '/' + ('/'.join(y))
            if last_title:
                self.title = last_title
        # 日志等级
        self.log_level = log_level if log_level else LoggingLevel.DEBUG

        self.date_rotate = date_rotate
        self.record_millisecond = record_millisecond
        self.pht_tl = pht_tl if pht_tl else LoggingLevel.NOTSET

        self.keep_file_open = True
        self.opened_files = {}
        self.file_encoding = file_encoding
        init()
        self.is_color = is_color

    def __del__(self):
        if len(self.opened_files.items()) > 0:
            for name, file in self.opened_files.items():
                file.close()

    def get_target_file(self, level):
        """
        创建日志文件
        :params:level
        :return:
        """
        if self.log_dir is None:
            return ''

        category_dir = self.log_dir

        if self.categorize:
            category_dir = os.path.join(self.log_dir, self.title)

        today = ''
        if self.date_rotate:
            localtime = time.localtime()
            today = os.path.join(str(localtime.tm_year), str(localtime.tm_mon), str(localtime.tm_mday))

        target_file = os.path.join(category_dir, today, r'{0}.{1}'.format(
            self.title, LoggingLevel.get_label_of_level(level).lower()))
        os.makedirs(os.path.dirname(target_file), exist_ok=True)
        return target_file

    def get_target_file_hander(self, target_file_path: str):
        if not target_file_path:
            return None

        if self.keep_file_open:
            file = self.opened_files.get(target_file_path)
            if not file:
                file = open(target_file_path, 'a', encoding=self.file_encoding)
                self.opened_files[target_file_path] = file
        else:
            file = open(target_file_path, 'a', encoding=self.file_encoding)

        return file

    def write_raw_line_to_log(self, text: str, level: int = LoggingLevel.INFO, flag=True, end=os.linesep):
        """
        Parameter `level` is only used to determine stdout or stderr when file empty.
        Since 0.2.8, Parameter `end` added.
        """
        target_file = self.get_target_file(level)
        if target_file != '' and flag:
            file = self.get_target_file_hander(target_file)
            file.write(text + end)
            file.flush()

            if not self.keep_file_open:
                file.close()
        if target_file == '' or level > self.pht_tl:
            color_dict = {
                50: Fore.LIGHTMAGENTA_EX,
                40: Fore.LIGHTRED_EX,
                30: Fore.LIGHTYELLOW_EX,
                25: Fore.LIGHTBLUE_EX,
                20: Fore.LIGHTGREEN_EX,
                10: Fore.LIGHTWHITE_EX,
                0: Fore.WHITE,
            }
            text = color_dict[level] + text if self.is_color else text
            print(text, end=end)
        return self

    def write_formatted_line_to_log(self, level: int, message: str, extra=None, flag=True, hide_extra: bool = False):
        """
        将写入的数据格式化
        :param level:日止级别
        :param message:日志信息
        :param extra:扩展信息
        :param flag:
        :param hide_extra:隐藏扩展信息
        :return:
        """
        if level < self.log_level:
            return self
        time_format_string = "%Y-%m-%d %H:%M:%S"
        if self.record_millisecond:
            time_format_string += '.%f'
        now = datetime.now().strftime(time_format_string)
        level_label = LoggingLevel.get_label_of_level(level)
        line = "{0} <{1}> [{2:>8s}]:{3}".format(now, self.title, level_label, message)
        if not hide_extra:
            frame = inspect.currentframe().f_back.f_back
            extend_params = {"file": os.path.split(frame.f_code.co_filename)[-1], "line": frame.f_lineno}
            if extra:
                extra.update(extend_params)
            else:
                extra = extend_params
            line += r' | {0}'.format(self.ensure_extra_as_dict(extra))
        return self.write_raw_line_to_log(line, level, flag)

    def debug(self, message: str, extra=None, flag=True):
        """
        调试信息
        :param message:日志信息
        :param extra: 扩展信息
        :param flag: 日志类型，是否写入文件
        :return: self
        """
        return self.write_formatted_line_to_log(LoggingLevel.DEBUG, message, extra, flag=flag)

    def info(self, message: str, extra=None, flag=True):
        """
        运行信息
        :param message:日志信息
        :param extra: 扩展信息
        :param flag: 日志类型，是否写入文件
        :return: self
        """
        return self.write_formatted_line_to_log(LoggingLevel.INFO, message, extra, flag=flag)

    def notice(self, message: str, extra=None, flag=True):
        """
        通知信息
        :param message:日志信息
        :param extra: 扩展信息
        :param flag: 日志类型，是否写入文件
        :return: self
        """
        return self.write_formatted_line_to_log(LoggingLevel.NOTICE, message, extra, flag=flag)

    def warning(self, message: str, extra=None, flag=True):
        """
        告警信息
        :param message:日志信息
        :param extra: 扩展信息
        :param flag: 日志类型，是否写入文件
        :return: self
        """
        return self.write_formatted_line_to_log(LoggingLevel.WARNING, message, extra, flag=flag)

    def error(self, message: str, extra=None, flag=True):
        """
        错误信息
        :param message:日志信息
        :param extra: 扩展信息
        :param flag: 日志类型，是否写入文件
        :return: self
        """
        return self.write_formatted_line_to_log(LoggingLevel.ERROR, message, extra, flag=flag)

    def exception(self, message: str, exception: BaseException, flag=True):
        """
        异常信息
        :param exception:
        :param message:日志信息
        :param flag: 日志类型，是否写入文件
        :return: self
        """
        just_the_string = self.get_traceback_info_from_exception(exception)
        return (
            self.write_formatted_line_to_log(LoggingLevel.ERROR, message, f'{type(exception).__name__}', flag=flag).
            write_raw_line_to_log(just_the_string, LoggingLevel.ERROR))

    def critical(self, message: str, extra=None, flag=True):
        """
        致命信息
        :param message:日志信息
        :param extra: 扩展信息
        :param flag: 日志类型，是否写入文件
        :return: self
        """
        frame = inspect.currentframe().f_back
        extend_params = {"file": os.path.split(frame.f_code.co_filename)[-1], "line": frame.f_lineno}
        if extra:
            extra.update(extend_params)
        else:
            extra = extend_params
        return self.write_formatted_line_to_log(LoggingLevel.CRITICAL, message, extra, flag=flag)

    @staticmethod
    def ensure_extra_as_dict(extra):
        """
        Since 0.1.25, add ensure_ascii as False to allow unicode chars
        """
        return json.dumps(extra, default=lambda inner_x: inner_x.__str__(), ensure_ascii=False)

    @staticmethod
    def get_traceback_info_from_exception(exception: BaseException) -> str:
        """
        从异常中获取信息
        """
        if CommonHelper.is_python_version_at_least(3, 10):
            return ''.join(traceback.format_exception(exception))
        else:
            return ''.join(
                traceback.format_exception(etype=type(exception), value=exception, tb=exception.__traceback__)
            )
