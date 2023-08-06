# -*- coding: utf-8 -*-
"""
@Author: CaiYouBin
@Date: 2020-06-01 14:07:23
@LastEditTime: 2020-11-05 17:57:35
@LastEditors: HuangJingCan
@Description: 商品相关
"""

from seven_cloudapp.handlers.seven_base import *
from seven_cloudapp.handlers.top_base import *

from seven_cloudapp.models.db_models.machine.machine_info_model import *
from seven_cloudapp.models.db_models.price.price_gear_model import *
from seven_cloudapp.models.db_models.act.act_info_model import *


class GoodsListHandler(TopBaseHandler):
    """
    @description: 获取商品列表
    """
    def get_async(self):
        """
        @description: 获取商品列表
        @param goods_name：商品名称
        @param order_tag：order_tag
        @param order_by：排序类型
        @param page_index：页索引
        @param page_size：页大小
        @return: 列表
        @last_editors: HuangJingCan
        """
        access_token = self.get_taobao_param().access_token
        goods_name = self.get_param("goods_name")
        order_tag = self.get_param("order_tag", "list_time")
        order_by = self.get_param("order_by", "desc")
        page_index = int(self.get_param("page_index", 0))
        page_size = self.get_param("page_size", 10)

        if self.get_is_test() == True:
            return self.reponse_json_success(self.test_goods_list())

        self.get_goods_list(page_index, page_size, goods_name, order_tag, order_by, access_token)


class GoodsInfoHandler(TopBaseHandler):
    """
    @description: 获取商品信息
    """
    @filter_check_params("goods_id")
    def get_async(self):
        """
        @description: 获取商品信息
        @param goods_id：商品id
        @param machine_id：机台id
        @param is_check_exist：是否存在
        @return: 商品信息
        @last_editors: HuangJingCan
        """
        access_token = self.get_taobao_param().access_token
        num_iid = self.get_param("goods_id")
        machine_id = int(self.get_param("machine_id", 0))
        is_check_machine_exist = int(self.get_param("is_check_exist", 0))

        if self.get_is_test() == True:
            return self.reponse_json_success(self.test_goods_info())

        if is_check_machine_exist > 0:
            machine_info_model = MachineInfoModel()
            exist_machineed = machine_info_model.get_entity("goods_id=%s and id<>%s", params=[num_iid, machine_id])
            if exist_machineed:
                return self.reponse_json_error("ExistGoodsID", "对不起，当前商品ID已应用到其他盒子中")

        self.get_goods_info(num_iid, access_token)


class GoodsCheckHandler(TopBaseHandler):
    """
    @description: 校验商品
    """
    @filter_check_params("goods_id,act_id")
    def get_async(self):
        """
        @description: 校验商品
        @param goods_id：商品id
        @param act_id：活动id
        @return: 商品信息
        @last_editors: HuangJingCan
        """
        access_token = self.get_taobao_param().access_token
        num_iid = self.get_param("goods_id")
        act_id = int(self.get_param("act_id", 0))
        price_gear_model = PriceGearModel()
        act_info_model = ActInfoModel()

        condition = "act_id!=%s and goods_id=%s"
        price_gear_goodsid = price_gear_model.get_entity(condition, params=[act_id, num_iid])
        if price_gear_goodsid:
            act_info = act_info_model.get_entity("id=%s", params=[price_gear_goodsid.act_id])
            actName = act_info.act_name if act_info else ""
            self.reponse_json_error("ParamError", f"此商品ID已关联活动{actName},无法使用！")
        else:
            self.get_goods_info(num_iid, access_token)