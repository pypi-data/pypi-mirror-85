# -*- coding: utf-8 -*-
"""
@Author: CaiYouBin
@Date: 2020-05-12 20:04:54
@LastEditTime: 2020-11-05 09:05:07
@LastEditors: HuangJingCan
@Description: 基础接口
"""
import random
from seven_cloudapp.handlers.seven_base import *
from seven_cloudapp.handlers.top_base import *
from seven_framework.qr_code import *

from seven_cloudapp.models.db_models.machine.machine_info_model import *
from seven_cloudapp.models.db_models.behavior.behavior_orm_model import *
from seven_cloudapp.models.db_models.act.act_prize_model import *
from seven_cloudapp.models.db_models.act.act_info_model import *
from seven_cloudapp.models.db_models.act.act_type_model import *
from seven_cloudapp.models.db_models.app.app_info_model import *
from seven_cloudapp.models.db_models.theme.theme_info_model import *
from seven_cloudapp.models.db_models.skin.skin_info_model import *
from seven_cloudapp.models.db_models.base.base_info_model import *
from seven_cloudapp.models.seven_model import PageInfo
from seven_cloudapp.models.behavior_model import *
from seven_cloudapp.models.enum import *


class ActTypeHandler(SevenBaseHandler):
    """
    @description: 活动类型相关
    """
    def post_async(self):
        """
        @description: 活动类型入库
        @param type_id：类型id
        @param type_name：类型名称
        @param act_title：活动标题
        @param act_img：活动图
        @param experience_img：体验码二维码图
        @param play_process：玩法流程
        @param applicable_behavior：适用行为
        @param market_function：营销功能
        @return: 
        @last_editors: HuangJingCan
        """
        type_id = int(self.get_param("type_id", "0"))
        type_name = self.get_param("type_name")
        act_title = self.get_param("act_title")
        act_img = self.get_param("act_img")
        experience_img = self.get_param("experience_img")
        play_process = self.get_param("play_process")
        applicable_behavior = self.get_param("applicable_behavior")
        market_function = self.get_param("market_function")

        # 数据入库
        act_type_model = ActTypeModel()
        act_type = None
        if type_id > 0:
            act_type = act_type_model.get_entity_by_id(type_id)

        is_add = False
        if not act_type:
            is_add = True
            act_type = ActType()

        act_type.type_name = type_name
        act_type.act_title = act_title
        act_type.act_img = act_img
        act_type.experience_img = experience_img
        act_type.play_process = play_process
        act_type.applicable_behavior = applicable_behavior
        act_type.market_function = market_function
        act_type.modify_date = self.get_now_datetime()

        if is_add:
            act_type.create_date = act_type.modify_date
            act_type_model.add_entity(act_type)
        else:
            act_type_model.update_entity(act_type)

        self.reponse_json_success()

    def get_async(self):
        """
        @description: 活动类型获取
        @param 
        @return: 列表
        @last_editors: HuangJingCan
        """
        act_type_model = ActTypeModel()
        act_type_list = act_type_model.get_list()

        new_list = []

        for info in act_type_list:
            if info.play_process:
                info.play_process = ast.literal_eval(info.play_process)
            if info.applicable_behavior:
                info.applicable_behavior = ast.literal_eval(info.applicable_behavior)
            if info.market_function:
                info.market_function = ast.literal_eval(info.market_function)
            new_list.append(info.__dict__)

        self.reponse_json_success(new_list)


class ActCreateHandler(TopBaseHandler):
    """
    @description: 创建活动（业务各自实现）
    """
    @filter_check_params("act_type")
    def get_async(self):
        """
        @description: 创建活动（业务各自实现）
        @param act_type：活动类型
        @return: 
        @last_editors: HuangJingCan
        """
        pass


class ActHandler(SevenBaseHandler):
    """
    @description: 活动信息保存（业务各自实现）
    """
    @filter_check_params("act_id,act_name")
    def post_async(self):
        """
        @description: 活动信息保存（业务各自实现）
        @param 
        @return 
        @last_editors: HuangJingCan
        """
        pass


class ActListHandler(SevenBaseHandler):
    """
    @description: 获取活动列表（业务各自实现）
    """
    def get_async(self):
        """
        @description: 获取活动列表（业务各自实现）
        @param act_name：活动名称
        @param is_del：是否删除
        @param page_index：页索引
        @param page_size：页大小
        @return: 列表
        @last_editors: HuangJingCan
        """
        pass


class ActInfoHandler(SevenBaseHandler):
    """
    @description: 活动信息获取（业务各自实现）
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 活动信息获取（业务各自实现）
        @param act_id：活动id
        @return: 活动信息
        @last_editors: HuangJingCan
        """
        pass


class ActDelHandler(SevenBaseHandler):
    """
    @description: 删除或者还原活动
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 删除或者还原活动
        @param act_id：活动id
        @param is_del：0-还原，1-删除
        @return: 
        @last_editors: HuangJingCan
        """
        act_id = int(self.get_param("act_id", "0"))
        is_del = int(self.get_param("is_del", "1"))
        modify_date = self.get_now_datetime()

        if act_id <= 0:
            return self.reponse_json_error_params()
        if is_del == 1:
            ActInfoModel().update_table("is_del=%s,modify_date=%s,is_release=0", "id=%s", [is_del, modify_date, act_id])
        else:
            ActInfoModel().update_table("is_del=%s,modify_date=%s,is_release=1", "id=%s", [is_del, modify_date, act_id])

        self.reponse_json_success()


class ActQrCodeHandler(SevenBaseHandler):
    """
    @description: 活动二维码获取
    """
    @filter_check_params("url")
    def get_async(self):
        """
        @description: 活动二维码获取
        @param act_id：活动id
        @return: 活动二维码图片
        @last_editors: HuangJingCan
        """
        url = self.get_param("url")

        img, img_bytes = QRCodeHelper.create_qr_code(url, fill_color="black")
        img_base64 = base64.b64encode(img_bytes).decode()

        self.reponse_json_success(f"data:image/jpeg;base64,{img_base64}")


class ActReviewHandler(SevenBaseHandler):
    """
    @description: 还原活动
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 还原活动
        @param act_id：活动id
        @return 
        @last_editors: HuangJingCan
        """
        act_id = self.get_param("act_id")
        modify_date = self.get_now_datetime()
        user_nick = self.get_taobao_param().user_nick
        store_user_nick = user_nick.split(':')[0]
        dict_app_id = AppInfoModel().get_dict("store_user_nick=%s", field="app_id", params=store_user_nick)
        if not dict_app_id:
            return self.reponse_json_error("NoAppId", "对不起，app_id不存在")

        act_info_model = ActInfoModel()
        act_info_total = act_info_model.get_total("app_id=%s and is_del=0", params=dict_app_id["app_id"])
        if act_info_total > 9:
            return self.reponse_json_error("OverAct", "对不起，活动不可超过10个")
        act_info_model.update_table("is_del=0,modify_date=%s,is_release=1", "id=%s", [modify_date, act_id])

        self.reponse_json_success()


class NextProgressHandler(SevenBaseHandler):
    """
    @description: 下一步
    """
    def get_async(self):
        """
        @description: 下一步
        @param act_id：活动id
        @param finish_key：finish_key
        @return 
        @last_editors: HuangJingCan
        """
        act_id = int(self.get_param("act_id"))
        finish_key = self.get_param("finish_key")
        base_info = BaseInfoModel().get_entity()
        if not base_info:
            return self.reponse_json_error("Error", "对不起，请与管理员联系")

        act_info_model = ActInfoModel()
        act_info = act_info_model.get_entity("id=%s", params=act_id)

        if not act_info:
            return self.reponse_json_error("NoAct", "对不起，找不到当前活动")

        menu_config = json.loads(base_info.menu_config)
        menu = [menu for menu in menu_config if menu["key"] == finish_key]
        if len(menu) == 0:
            return self.reponse_json_error("Error", "对不起，无此菜单")

        if act_info.menu_configed != "" and finish_key in act_info.menu_configed:
            return self.reponse_json_success()

        if act_info.menu_configed == "":
            act_info.menu_configed = "[]"

        menu_configed = json.loads(act_info.menu_configed)
        menu_configed.append(finish_key)

        result_menu_configed = []
        for item in menu_configed:
            is_exist = [item2 for item2 in menu_config if item2["key"] == item]
            if len(is_exist) > 0:
                result_menu_configed.append(item)
        if len(result_menu_configed) == len(menu_config) and act_info.finish_progress == 0:
            act_info.finish_progress = 1

        act_info.menu_configed = json.dumps(result_menu_configed)

        act_info_model.update_entity(act_info)

        self.reponse_json_success()