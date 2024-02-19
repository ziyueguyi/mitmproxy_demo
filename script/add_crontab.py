# -*- coding: utf-8 -*-
"""
# @项目名称 :mitmproxy_demo
# @文件名称 :add_crontab.py
# @作者名称 :sxzhang1
# @日期时间 :2024/1/26 11:15
# @文件介绍 :
"""
from crontab import CronTab


class CrontabUpdate(object):
    def __init__(self):
        """
        添加和删除定时任务
        """
        # 创建当前用户的crontab，当然也可以创建其他用户的，但得有足够权限
        self.cron = CronTab(user=True)

    def add_crontab_job(self, cmd_line, time_str, com_name=None, user="root"):
        """
        添加定时任务
        :param cmd_line:任务命令
        :param time_str:cron时间
        :param com_name:任务标识
        :param user:用户，默认为root
        """
        # 创建任务
        job = self.cron.new(command=cmd_line)
        # 设置任务执行周期
        job.setall(time_str)
        # 给任务添加一个标识，给任务设置comment，这样就可以根据comment查询
        job.set_comment(com_name)
        # 将crontab写入配置文件
        self.cron.write_to_user(user=user)  # 指定用户，写入指定用户下的crontab任务

    def del_crontab_jobs(self, com_name, user="root"):
        # 按comment清除多个定时任务，一次write即可
        self.cron.remove_all(comment=com_name)
        self.cron.write_to_user(user=user)  # 指定用户,删除指定用户下的crontab任务


