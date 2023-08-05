# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-05-12 20:04:54
@LastEditTime: 2020-11-04 17:24:56
@LastEditors: HuangJingCan
@Description: 用户相关
"""
from seven_cloudapp.handlers.seven_base import *

from seven_cloudapp.models.db_models.app.app_info_model import *
from seven_cloudapp.models.db_models.login.login_log_model import *
from seven_cloudapp.models.db_models.user.user_info_model import *
from seven_cloudapp.models.db_models.machine.machine_value_model import *
from seven_cloudapp.models.seven_model import *

from seven_cloudapp.libs.customize.seven import *


class LoginHandler(SevenBaseHandler):
    """
    @description: 登录处理
    """
    @filter_check_params("open_id")
    def get_async(self):
        """
        @description: 登录日志入库
        @param open_id：用户唯一标识
        @param user_nick：用户昵称
        @return: 
        @last_editors: HuangJingCan
        """
        open_id = self.get_taobao_param().open_id
        user_nick = self.get_taobao_param().user_nick
        source_app_id = self.get_taobao_param().source_app_id

        request_params = str(self.request_params)

        if user_nick == "":
            return self.reponse_json_success()

        login_log_model = LoginLogModel()
        login_log = login_log_model.get_entity("open_id=%s", params=open_id)

        is_add = False
        if not login_log:
            is_add = True
            login_log = LoginLog()

        login_log.open_id = open_id
        login_log.user_nick = user_nick
        if user_nick.__contains__(":"):
            login_log.store_user_nick = user_nick.split(":")[0]
            login_log.is_master = 0
        else:
            login_log.store_user_nick = user_nick
            login_log.is_master = 1
        login_log.request_params = request_params
        login_log.modify_date = self.get_now_datetime()

        if is_add:
            login_log.create_date = login_log.modify_date
            login_log.id = login_log_model.add_entity(login_log)
        else:
            login_log_model.update_entity(login_log)

        self.reponse_json_success()


class UserStatusHandler(SevenBaseHandler):
    """
    @description: 更新用户状态
    """
    @filter_check_params("userid,user_state")
    def get_async(self):
        """
        @description: 更新用户状态
        @param userid：用户id
        @param user_state：用户状态
        @return: 
        @last_editors: HuangJingCan
        """
        user_id = int(self.get_param("userid"))
        user_state = int(self.get_param("user_state"))
        modify_date = self.get_now_datetime()
        relieve_date = self.get_now_datetime()

        UserInfoModel().update_table("user_state=%s,modify_date=%s,relieve_date=%s", "id=%s", [user_state, modify_date, relieve_date, user_id])

        self.reponse_json_success()


class UserListHandler(SevenBaseHandler):
    """
    @description: 用户列表（业务各自实现）
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 获取用户列表（业务各自实现）
        @param page_index：页索引
        @param page_size：页大小
        @param act_id：活动id
        @param nick_name：用户昵称
        @return：分页列表 
        @last_editors: HuangJingCan
        """
        pass