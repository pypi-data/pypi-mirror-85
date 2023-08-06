# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-06-02 13:44:17
@LastEditTime: 2020-11-04 17:16:14
@LastEditors: HuangJingCan
@Description: 奖品相关
"""
from seven_cloudapp.handlers.seven_base import *
from seven_cloudapp.handlers.top_base import *

from seven_cloudapp.models.db_models.act.act_info_model import *
from seven_cloudapp.models.db_models.act.act_prize_model import *
from seven_cloudapp.models.db_models.prize.prize_roster_model import *
from seven_cloudapp.models.db_models.throw.throw_goods_model import *
from seven_cloudapp.models.db_models.machine.machine_info_model import *
from seven_cloudapp.models.throw_model import *
from seven_cloudapp.models.seven_model import *
from seven_cloudapp.models.enum import *

from seven_cloudapp.libs.customize.seven import *


class PrizeListHandler(SevenBaseHandler):
    """
    @description: 奖品列表（业务各自实现）
    """
    @filter_check_params("machine_id")
    def get_async(self):
        """
        @description: 奖品列表（业务各自实现）
        @param page_index：页索引
        @param page_size：页大小
        @param act_id：活动id
        @param machine_id：机台id
        @return: 
        @last_editors: HuangJingCan
        """
        pass


class PrizeHandler(SevenBaseHandler):
    """
    @description: 奖品保存（业务各自实现）
    """
    @filter_check_params("machine_id,prize_name")
    def post_async(self):
        """
        @description: 奖品保存（业务各自实现）
        @param prize_id：奖品id
        @return: 
        @last_editors: HuangJingCan
        """
        pass


class PrizeDelHandler(SevenBaseHandler):
    """
    @description: 删除奖品
    """
    @filter_check_params("prize_id")
    def get_async(self):
        """
        @description: 删除奖品
        @param prize_id：奖品id
        @return: 
        @last_editors: HuangJingCan
        """
        prize_id = int(self.get_param("prize_id", 0))

        if prize_id <= 0:
            return self.reponse_json_error_params()

        act_prize_model = ActPrizeModel()
        act_prize = act_prize_model.get_entity("id=%s", params=prize_id)

        if not act_prize:
            return self.reponse_json_success()

        act_prize_model.del_entity("id=%s", prize_id)

        #投放商品处理
        ThrowModel().throw_goods_update(act_prize.act_id, act_prize.goods_id, self.get_now_datetime())

        self.create_operation_log(OperationType.delete.value, "act_prize_tb", "PrizeDelHandler", None, prize_id)

        self.reponse_json_success()


class PrizeReleaseHandler(SevenBaseHandler):
    """
    @description: 上下架奖品
    """
    @filter_check_params("prize_id")
    def get_async(self):
        """
        @description: 上下架奖品
        @param prize_id：奖品id
        @param is_release：0-下架，1-上架
        @return: 
        @last_editors: HuangJingCan
        """
        prize_id = int(self.get_param("prize_id", 0))
        is_release = int(self.get_param("is_release", 0))
        modify_date = self.get_now_datetime()

        if prize_id <= 0:
            return self.reponse_json_error_params()

        ActPrizeModel().update_table("is_release=%s,modify_date=%s", "id=%s", [is_release, modify_date, prize_id])

        self.reponse_json_success()