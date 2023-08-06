# coding:utf-8
import json
import logging
import math
import os
from random import random
from typing import Optional

from apscheduler.events import EVENT_JOB_EXECUTED, EVENT_JOB_ERROR
from apscheduler.job import Job
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.schedulers.blocking import BlockingScheduler
import datetime
from apscheduler.jobstores.memory import MemoryJobStore
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from apscheduler.jobstores.sqlalchemy import SQLAlchemyJobStore

"""
apscheduler 任务调度
提供了基于日期、固定时间间隔以及 crontab 类型的任务，并且可以持久化任务、并以 daemon 方式运行应用。
https://zhuanlan.zhihu.com/p/46948464

# 方法一：
        # scheduler = BackgroundScheduler({
        #     'apscheduler.jobstores.mongo': {
        #         'type': 'mongodb'
        #     },
        #     'apscheduler.jobstores.default': {
        #         'type': 'sqlalchemy',
        #         'url': 'sqlite:///jobs.sqlite'
        #     },
        #     'apscheduler.executors.default': {
        #         'class': 'apscheduler.executors.pool:ThreadPoolExecutor',
        #         'max_workers': '20'
        #     },
        #     'apscheduler.executors.processpool': {
        #         'type': 'processpool',
        #         'max_workers': '5'
        #     },
        #     'apscheduler.job_defaults.coalesce': 'false',
        #     'apscheduler.job_defaults.max_instances': '3',
        #     'apscheduler.timezone': 'UTC',
        # })
        
        # 方法三：
        # jobstores = {
        #     'mongo': {'type': 'mongodb'},
        #     'default': SQLAlchemyJobStore(url='sqlite:///jobs.sqlite')
        # }
        # executors = {
        #     'default': {'type': 'threadpool', 'max_workers': 20},
        #     'processpool': ProcessPoolExecutor(max_workers=5)
        # }
        # job_defaults = {
        #     'coalesce': False,
        #     'max_instances': 3
        # }
        # scheduler = BackgroundScheduler()
        
        # 方法二：
        # 使用内存保存任务
        # jobstores = {
        #     'default': MemoryJobStore()
        # }
        
"""


def my_job(id='my_job'):
    print(id, '-->', datetime.datetime.now())


class ApschedulerUtils:
    scheduler = None

    def __init__(self):
        self.init()

    def checkNone(self) -> bool:
        if self.scheduler is None:
            print('Scheduler object is None.Please use init methon first.')
            return True
        else:
            return False

    def init(self):

        # 使用sql存储调度任务
        jobstores = {
            'default': MemoryJobStore()
        }
        executors = {
            'default': ThreadPoolExecutor(20),
            'processpool': ProcessPoolExecutor(10)
        }
        job_defaults = {
            'coalesce': True,
            'max_instances': 3
        }
        self.scheduler = BlockingScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)

        # self.scheduler = AsyncIOScheduler(jobstores=jobstores, executors=executors, job_defaults=job_defaults)
        # 异常调度
        def my_listener(event):
            if event.exception:
                print('任务出错了！！！！！！')
            # else:
                # print('任务执行...')

        # 添加事件监听
        self.scheduler.add_listener(my_listener, EVENT_JOB_EXECUTED | EVENT_JOB_ERROR)

        logging.basicConfig(level=logging.INFO,
                            format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                            datefmt='%Y-%m-%d %H:%M:%S',
                            filename='SchedulerLog.txt',
                            filemode='a')
        self.scheduler._logger = logging

    def init_job(self, path='./conf/task.conf'):
        jobs = self.file2dict(path)
        intervalJobs = jobs['IntervalJob']
        for item in intervalJobs:
            def job():
                os.system(item['cmd'])
            self.registIntervalJob(job, job_id=item['task-name'], seconds=item['seconds'])

    def getScheduler(self):
        return self.scheduler

    def registIntervalJob(self, fun, args=None, job_id: str = '', seconds: int = 0) -> Optional[Job]:
        """
        注册间隔任务
        :param fun: 回调的函数
        :param args: 回调的函数参数列表
        :param job_id: 任务标识
        :param seconds: 单位：秒
        :return:
        """
        if args is None:
            args = []
        if self.checkNone():
            return
        if job_id == '':
            job_id = f'default{random.random()}'
        return self.scheduler.add_job(fun, args=args, id=job_id, trigger='interval', seconds=seconds,
                                      replace_existing=True)

    def registCronJob(self, fun, args=None, job_id='', day_of_week=0, hour=19, minute=0, second=0) -> \
            Optional[Job]:
        """
        注册指定时间间隔任务
        year (int|str) – 4-digit year
        month (int|str) – month (1-12)
        day (int|str) – day of the (1-31)
        week (int|str) – ISO week (1-53)
        day_of_week (int|str) – number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
        hour (int|str) – hour (0-23)
        minute (int|str) – minute (0-59)
        econd (int|str) – second (0-59)

        start_date (datetime|str) – earliest possible date/time to trigger on (inclusive)
        end_date (datetime|str) – latest possible date/time to trigger on (inclusive)
        timezone (datetime.tzinfo|str) – time zone to use for the date/time calculations (defaults to scheduler timezone)

        表达式 	参数类型 	描述
        * 	所有 	通配符。例：minutes=*即每分钟触发
        */a 	所有 	可被a整除的通配符。
        a-b 	所有 	范围a-b触发
        a-b/c 	所有 	范围a-b，且可被c整除时触发
        xth y 	日 	第几个星期几触发。x为第几个，y为星期几
        last x 	日 	一个月中，最后个星期几触发
        last 	日 	一个月最后一天触发
        x,y,z 	所有 	组合表达式，可以组合确定值或上方的表达式

        (year=None, month=None, day=None, week=None, day_of_week=None, hour=None, minute=None, second=None
        , start_date=None, end_date=None, timezone=None)
        除了week和 day_of_week，它们的默认值是*
        例如day=1, minute=20，这就等于year='*', month='*', day=1, week='*', day_of_week='*', hour='*', minute=20
        , second=0，工作将在每个月的第一天以每小时20分钟的时间执行

        :param day_of_week:
        :param fun: 回调的函数
        :param args: 回调的函数参数列表
        :param job_id: 任务标识
        :param month: 月，4-8,11-12
        :param day:1-31
        :param week:1-53
        :param hour: 时，7-11
        :param minute:0-59
        :param second: 秒，*/10
        :return:
        """
        if self.checkNone():
            return None
        if job_id == '':
            job_id = f'default{random.random()}'
        return self.scheduler.add_job(fun, args=args, id=job_id, trigger='cron', day_of_week=day_of_week, hour=hour,
                                      minute=minute, second=second, coalesce=True,
                                      misfire_grace_time=30,
                                      replace_existing=True)

        # misfire_grace_time，假如一个作业本来 08:00 有一次执行，但是由于某种原因没有被调度上，现在 08:01 了，这
        # 个 08:00 的运行实例被提交时，会检查它预订运行的时间和当下时间的差值（这里是1分钟），大于我们设置的 30 秒限
        # 制，那么这个运行实例不会被执行。
        # 最常见的情形是 scheduler 被 shutdown 后重启，某个任务会积攒了好几次没执行，如 5 次，下次这个作业被提交给
        # 执行器时，执行 5 次。设置 coalesce=True 后，只会执行一次。

    def registOnceJob(self, fun, args=None, job_id: str = '') -> Optional[Job]:
        """
        注册一次性任务
        :param fun: 回调的函数
        :param args: 回调的函数参数列表
        :param job_id: 任务标识
        :return:
        """
        if self.checkNone():
            return
        if job_id == '':
            job_id = f'default{random.random()}'
        return self.scheduler.add_job(fun, args=args, id=job_id)

    def registDateJob(self, fun, args: list, job_id: str = '', run_date: str = '') -> Optional[Job]:
        """
        注册固定日期执行任务
        :param fun: 回调的函数
        :param args: 回调的函数参数列表
        :param job_id: 任务标识
        :param run_date: '2020-09-30 07:48:05'
        :return:
        """
        if self.checkNone():
            return
        if job_id == '':
            job_id = f'default{random.random()}'
        return self.scheduler.add_job(fun, args=args, id=job_id, trigger='date',
                                      run_date=run_date)

    def pause(self, job_id: str):
        """
        暂停
        :param job_id:
        :return:
        """
        self.scheduler.pause_job(job_id)

    def resume(self, job_id: str):
        """
        恢复
        :param job_id:
        :return:
        """
        self.scheduler.resume_job(job_id)

    def start(self) -> bool:
        """
        启动任务调度
        设置完任务再调用
        :return:
        """
        try:
            if self.checkNone():
                return False
            self.scheduler.start()
            return True
        except SystemExit:
            print('SystemExit')
            return False

    def file2dict(self, path):
        # 读取配置文件
        with open(path) as f:
            return json.load(f)


# scheduler.remove_job(job_id,jobstore=None)#删除作业
# scheduler.remove_all_jobs(jobstore=None)#删除所有作业
# scheduler.pause_job(job_id,jobstore=None)#暂停作业
# scheduler.resume_job(job_id,jobstore=None)#恢复作业
# scheduler.modify_job(job_id, jobstore=None, **changes)#修改单个作业属性信息
# scheduler.reschedule_job(job_id, jobstore=None, trigger=None,**trigger_args)#修改单个作业的触发器并更新下次运行时间
# scheduler.print_jobs(jobstore=None, out=sys.stdout)#输出作业信息
if __name__ == '__main__':
    sch = ApschedulerUtils()
    sch.init()
    sch.registIntervalJob(my_job, job_id='test', seconds=3)
    sch.start()
