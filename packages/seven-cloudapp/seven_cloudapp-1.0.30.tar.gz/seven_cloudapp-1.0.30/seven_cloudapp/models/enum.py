# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-06-02 14:32:40
@LastEditTime: 2020-06-16 11:30:16
@LastEditors: HuangJingCan
@Description: 枚举类
"""

from enum import Enum, unique


class TagType(Enum):
    """
    @description: 标签类型
    """
    无 = 0
    限定 = 1
    稀有 = 2
    绝版 = 3
    隐藏 = 4


class SourceType(Enum):
    """
    @description: 用户次数配置来源类型
    """
    购买 = 1
    任务 = 2
    手动配置 = 3


class OperationType(Enum):
    """
    @description: 用户操作日志类型
    """
    add = 1
    update = 2
    delete = 3