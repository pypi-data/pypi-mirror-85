# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-05-24 17:26:33
@LastEditTime: 2020-11-04 14:06:43
@LastEditors: HuangJingCan
@Description: App相关
"""
from seven_cloudapp.handlers.seven_base import *

from seven_cloudapp.models.db_models.base.base_info_model import *
from seven_cloudapp.models.db_models.app.app_info_model import *
from seven_cloudapp.models.enum import *


class HelperInfoHandler(SevenBaseHandler):
    """
    @description: 获取助手信息
    """
    def get_async(self):
        """
        @description: 获取助手信息
        @param 
        @return 字典信息
        @last_editors: HuangJingCan
        """
        # 基础信息配置
        base_info = BaseInfoModel().get_entity()

        if not base_info:
            self.reponse_json_error("BaseInfoError", "基础信息出错")

        #店铺主帐号名称
        store_user_nick = self.get_taobao_param().user_nick.split(':')[0]
        app_info = AppInfoModel().get_entity("store_user_nick=%s", params=store_user_nick)

        data = {}
        data["video_url"] = base_info.video_url
        data["study_url"] = base_info.study_url
        data["customer_service"] = base_info.customer_service
        data["is_remind_phone"] = base_info.is_remind_phone
        if app_info:
            data["app_telephone"] = app_info.app_telephone

        self.reponse_json_success(data)


class RenewInfoHandler(SevenBaseHandler):
    """
    @description: 获取续订信息
    """
    def get_async(self):
        """
        @description: 获取续订信息
        @param 
        @return 字典信息
        @last_editors: HuangJingCan
        """
        # 基础信息配置
        base_info = BaseInfoModel().get_entity()

        if not base_info:
            self.reponse_json_error("BaseInfoError", "基础信息出错")

        #店铺主帐号名称
        store_user_nick = self.get_taobao_param().user_nick.split(':')[0]
        app_info = AppInfoModel().get_entity("store_user_nick=%s", params=store_user_nick)

        data = {}
        if app_info:
            # 过期时间
            data["dead_date"] = app_info.dead_date
            # 订阅剩余天数
            data["surplus_day"] = app_info.surplus_day
            # 最后登录时间
            data["last_login_date"] = app_info.last_login_date
        if base_info.product_price:
            # 价格信息
            data["product_price"] = ast.literal_eval(base_info.product_price)

        self.reponse_json_success(data)


class UpdateInfoHandler(SevenBaseHandler):
    """
    @description: 获取软件更新信息
    """
    def get_async(self):
        """
        @description: 获取软件更新信息
        @param 
        @return 字典信息
        @last_editors: HuangJingCan
        """
        # 基础信息配置
        base_info = BaseInfoModel().get_entity()

        if not base_info:
            self.reponse_json_error("BaseInfoError", "基础信息出错")

        data = {}
        # 最新消费者端版本号
        data["client_ver"] = base_info.client_ver
        # 最新千牛端版本号
        data["server_ver"] = base_info.server_ver
        if base_info.update_function:
            # 消费者端更新内容
            data["update_function"] = ast.literal_eval(base_info.update_function)
        # 当前消费者端版本号
        data["template_ver"] = base_info.client_ver

        self.reponse_json_success(data)


class DecorationPosterHandler(SevenBaseHandler):
    """
    @description: 获取装修海报
    """
    def get_async(self):
        """
        @description: 获取装修海报
        @param 
        @return 字典信息
        @last_editors: HuangJingCan
        """
        # 基础信息配置
        base_info = BaseInfoModel().get_entity()

        if not base_info:
            self.reponse_json_error("BaseInfoError", "基础信息出错")

        data = {}
        if base_info.decoration_poster:
            data["decoration_poster"] = ast.literal_eval(base_info.decoration_poster)

        self.reponse_json_success(data)


class FriendLinkHandler(SevenBaseHandler):
    """
    @description: 获取友情链接
    """
    def get_async(self):
        """
        @description: 获取友情链接
        @param 
        @return 字典信息
        @last_editors: HuangJingCan
        """
        # 基础信息配置
        base_info = BaseInfoModel().get_entity()

        if not base_info:
            self.reponse_json_error("BaseInfoError", "基础信息出错")

        data = {}
        if base_info.friend_link:
            # 友情链接
            data["friend_link"] = ast.literal_eval(base_info.friend_link)

        self.reponse_json_success(data)


class OtherConfigHandler(SevenBaseHandler):
    """
    @description: 获取其它配置信息
    """
    def get_async(self):
        """
        @description: 获取其它配置信息
        @param 
        @return 字典信息
        @last_editors: HuangJingCan
        """
        # 基础信息配置
        base_info = BaseInfoModel().get_entity()

        if not base_info:
            self.reponse_json_error("BaseInfoError", "基础信息出错")

        data = {}
        # if base_info.other_config:
        #     data["other_config"] = ast.literal_eval(base_info.other_config)

        self.reponse_json_success(data)