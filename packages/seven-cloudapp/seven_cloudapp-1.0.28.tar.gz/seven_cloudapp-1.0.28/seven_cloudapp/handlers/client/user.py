# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-05-19 11:33:16
@LastEditTime: 2020-11-05 16:44:19
@LastEditors: HuangJingCan
@Description: 用户处理
"""
from seven_cloudapp.handlers.seven_base import *

from seven_cloudapp.models.db_models.user.user_info_model import *
from seven_cloudapp.models.db_models.act.act_info_model import *
from seven_cloudapp.models.db_models.machine.machine_info_model import *
from seven_cloudapp.models.db_models.machine.machine_value_model import *
from seven_cloudapp.models.behavior_model import *

from seven_cloudapp.models.seven_model import PageInfo

from seven_cloudapp.libs.customize.seven import *


class LoginHandler(SevenBaseHandler):
    """
    @description: 登录处理
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 登录日志入库
        @param avatar：头像
        @param is_auth：是否授权（1是0否）
        @param owner_open_id：应用拥有者唯一标识
        @param login_token：登录令牌
        @param signin：签到信息
        @param act_id：活动id
        @return: 
        @last_editors: HuangJingCan
        """
        open_id = self.get_taobao_param().open_id
        user_nick = self.get_taobao_param().user_nick
        app_id = self.get_taobao_param().source_app_id
        avatar = self.get_param("avatar")
        is_auth = int(self.get_param("is_auth", 0))
        owner_open_id = self.get_param("owner_open_id")
        login_token = self.get_param("login_token")
        signin = self.get_param("signin")
        act_id = int(self.get_param("act_id", 0))

        user_info_model = UserInfoModel()
        user_info = user_info_model.get_entity("app_id=%s and act_id=%s and open_id=%s", params=[app_id, act_id, open_id])

        act_info_model = ActInfoModel()
        act_info = act_info_model.get_entity("id=%s", params=act_id)
        if not act_info:
            return self.reponse_json_error("NoAct", "对不起，活动不存在")

        machine_info_model = MachineInfoModel()
        machine_info_list = machine_info_model.get_list("app_id=%s and act_id=%s", params=[app_id, act_id])
        if not machine_info_list:
            return self.reponse_json_error("NoMachine", "对不起，盲盒不存在")

        is_add = False
        if not user_info:
            is_add = True
        if is_add:
            user_info = self.get_default_user(act_id)
            user_info.login_token = SevenHelper.get_random(16, 1)
            user_info.id = user_info_model.add_entity(user_info)
        else:
            user_info.modify_date = self.get_now_datetime()
            user_info.login_token = SevenHelper.get_random(16, 1)
            user_info.is_new = 0
            user_info_model.update_entity(user_info)

        machine_value_model = MachineValueModel()
        machine_value_list = machine_value_model.get_dict_list("open_id=%s", params=open_id)
        user_info_dict = user_info.__dict__
        user_info_dict["machine_value_list"] = machine_value_list

        behavior_model = BehaviorModel()
        # 访问次数
        behavior_model.report_behavior(app_id, act_id, open_id, owner_open_id, 'VisitCountEveryDay', 1)
        # 访问人数
        behavior_model.report_behavior(app_id, act_id, open_id, owner_open_id, 'VisitManCountEveryDay', 1)
        if user_info.is_new == 1:
            # 新增用户数
            behavior_model.report_behavior(app_id, act_id, open_id, owner_open_id, 'VisitManCountEveryDayIncrease', 1)

        self.reponse_json_success(user_info_dict)


class UserHandler(SevenBaseHandler):
    """
    @description: 更新用户信息
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 更新用户信息
        @param avatar：头像
        @param act_id：活动id
        @return: 
        @last_editors: HuangJingCan
        """
        try:
            open_id = self.get_taobao_param().open_id
            user_nick = self.get_taobao_param().user_nick
            source_app_id = self.get_taobao_param().source_app_id
            avatar = self.get_param("avatar")
            act_id = int(self.get_param("act_id", 0))

            user_info_model = UserInfoModel()
            user_info = user_info_model.get_entity("open_id=%s and app_id=%s and act_id=%s", params=[open_id, source_app_id, act_id])
            if not user_info:
                return self.reponse_json_error("NoUser", "对不起，用户不存在")
            user_info.user_nick = user_nick
            user_info.avatar = avatar
            user_info.is_auth = 1
            user_info.modify_date = self.get_now_datetime()
            user_info_model.update_entity(user_info)

            self.reponse_json_success("更新成功")
        except Exception as ex:
            self.reponse_json_error("Error", "更新失败")