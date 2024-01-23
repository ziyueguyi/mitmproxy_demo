# -*- coding: utf-8 -*-
"""
# @项目名称 :mitmproxy_demo
# @文件名称 :installation_package.py
# @作者名称 :sxzhang1
# @日期时间 :2024/1/23 15:37
# @文件介绍 :
"""
import os
from pip import main as pip_main


def install_requirements(self):
    """Resolve and install requirements. This function will read
    the file ``requirements.txt`` from path passed as argument, and
    then use pip to install them.
    """
    requirements = os.path.abspath(
        os.path.join(self.new_version_path, "..", "requirements.txt")
    )
    if os.path.exists(requirements):
        pip_main(["-q", "install", "-r", requirements])
