# -*- coding: utf-8 -*-
"""
@Author: HuangJingCan
@Date: 2020-06-02 11:08:39
@LastEditTime: 2020-11-04 15:16:13
@LastEditors: HuangJingCan
@Description: 订单相关
"""
from seven_cloudapp.handlers.seven_base import *

from seven_cloudapp.models.db_models.pay.pay_order_model import *
from seven_cloudapp.models.db_models.prize.prize_order_model import *
from seven_cloudapp.models.db_models.prize.prize_roster_model import *
from seven_cloudapp.models.seven_model import *

from seven_cloudapp.libs.customize.seven import *


class PayOrderListHandler(SevenBaseHandler):
    """
    @description: 用户购买订单
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 用户购买订单
        @param page_index：页索引
        @param page_size：页大小
        @param act_id：活动id
        @param user_open_id：用户唯一标识
        @param pay_date_start：订单支付时间开始
        @param pay_date_end：订单支付时间结束
        @param nick_name：用户昵称
        @return: 列表
        @last_editors: HuangJingCan
        """
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 10))
        act_id = int(self.get_param("act_id", 0))
        user_open_id = self.get_param("user_open_id")
        pay_date_start = self.get_param("pay_date_start")
        pay_date_end = self.get_param("pay_date_end")
        nick_name = self.get_param("nick_name")
        condition = "act_id=%s"
        params = [act_id]
        field = "id,order_no,user_nick,goods_name,sku_name,buy_num,pay_price,pay_date,main_order_no"
        if user_open_id:
            condition += " AND open_id=%s"
            params.append(user_open_id)
        if pay_date_start:
            condition += " AND pay_date>=%s"
            params.append(pay_date_start)
        if pay_date_end:
            condition += " AND pay_date<=%s"
            params.append(pay_date_end)
        if nick_name != "":
            user_nick = f"%{nick_name}%"
            condition += " AND user_nick LIKE %s"
            params.append(nick_name)

        page_list, total = PayOrderModel().get_dict_page_list("*", page_index, page_size, condition, "", "pay_date desc", params)

        page_info = PageInfo(page_index, page_size, total, page_list)

        self.reponse_json_success(page_info)


class PrizeOrderListHandler(SevenBaseHandler):
    """
    @description: 用户奖品订单
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 用户奖品订单
        @param page_index：页索引
        @param page_size：页大小
        @param act_id：活动id
        @param order_no：订单号
        @param nick_name：用户昵称
        @param real_name：用户名字
        @param telephone：联系电话
        @param adress：收货地址
        @param order_status：订单状态
        @param create_date_start：订单创建时间开始
        @param create_date_end：订单创建时间结束
        @return: 列表
        @last_editors: HuangJingCan
        """
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 10))
        act_id = int(self.get_param("act_id", 0))
        order_no = self.get_param("order_no")
        user_nick = self.get_param("nick_name")
        real_name = self.get_param("real_name")
        telephone = self.get_param("telephone")
        adress = self.get_param("adress")
        order_status = self.get_param("order_status")
        create_date_start = self.get_param("create_date_start")
        create_date_end = self.get_param("create_date_end")
        condition = "act_id=%s"
        params = [act_id]
        field = "id,order_no,user_nick,real_name,telephone,province,city,county,street,adress,order_status,create_date,remarks,deliver_date,express_no,express_company"
        if order_no:
            condition += " AND order_no=%s"
            params.append(order_no)
        if user_nick:
            user_nick = f"%{user_nick}%"
            condition += " AND user_nick LIKE %s"
            params.append(user_nick)
        if real_name:
            real_name = f"%{real_name}%"
            condition += " AND real_name LIKE %s"
            params.append(real_name)
        if telephone:
            condition += " AND telephone=%s"
            params.append(telephone)
        if adress:
            adress = f"%{adress}%"
            condition += " AND adress LIKE %s"
            params.append(adress)
        if order_status or order_status == "-1":
            condition += " AND order_status=%s"
            params.append(order_status)
        if create_date_start:
            condition += " AND create_date>=%s"
            params.append(create_date_start)
        if create_date_end:
            condition += " AND create_date<=%s"
            params.append(create_date_end)

        page_list, total = PrizeOrderModel().get_dict_page_list("*", page_index, page_size, condition, "", "id desc", params)

        page_info = PageInfo(page_index, page_size, total, page_list)

        self.reponse_json_success(page_info)


class PrizeRosterListHandler(SevenBaseHandler):
    """
    @description: 用户奖品列表
    """
    @filter_check_params("act_id")
    def get_async(self):
        """
        @description: 用户奖品列表
        @param page_index：页索引
        @param page_size：页大小
        @param act_id：活动id
        @param prize_order_id：奖品订单id
        @param nick_name：用户昵称
        @param is_submit：是否提交
        @param order_status：订单状态
        @param create_date_start：订单创建时间开始
        @param create_date_end：订单创建时间结束
        @param user_open_id：用户唯一标识
        @return: 列表
        @last_editors: HuangJingCan
        """
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 10))
        act_id = int(self.get_param("act_id", 0))
        prize_order_id = int(self.get_param("prize_order_id", 0))
        user_nick = self.get_param("nick_name")
        is_submit = self.get_param("is_submit")
        order_status = self.get_param("order_status")
        create_date_start = self.get_param("create_date_start")
        create_date_end = self.get_param("create_date_end")
        user_open_id = self.get_param("user_open_id")
        condition = "act_id=%s"
        params = [act_id]
        field = "id,user_nick,machine_name,machine_price,prize_name,prize_price,properties_name,create_date,order_status,order_no,prize_order_id,prize_order_no,prize_pic,goods_code"
        if prize_order_id > 0:
            condition += " AND prize_order_id=%s"
            params.append(prize_order_id)
        if user_nick:
            user_nick = f"%{user_nick}%"
            condition += " AND user_nick LIKE %s"
            params.append(user_nick)
        if is_submit and is_submit != "-1":
            if is_submit == "0":
                condition += " AND prize_order_id=0"
            else:
                condition += " AND prize_order_id>0"
        if order_status:
            condition += " AND order_status=%s"
            params.append(order_status)
        if create_date_start:
            condition += " AND create_date>=%s"
            params.append(create_date_start)
        if create_date_end:
            condition += " AND create_date<=%s"
            params.append(create_date_end)
        if user_open_id:
            condition += " AND open_id=%s"
            params.append(user_open_id)

        page_list, total = PrizeRosterModel().get_dict_page_list("*", page_index, page_size, condition, "", "id desc", params)

        page_info = PageInfo(page_index, page_size, total, page_list)

        self.reponse_json_success(page_info)


class PrizeOrderStatusHandler(SevenBaseHandler):
    """
    @description: 更新用户奖品订单状态
    """
    @filter_check_params("prize_order_id,order_status")
    def post_async(self):
        """
        @description: 更新用户奖品订单状态
        @param prize_order_id：奖品订单id
        @param order_status：订单状态
        @param express_company：快递公司
        @param express_no：快递单号
        @return: 
        @last_editors: HuangJingCan
        """
        prize_order_id = int(self.get_param("prize_order_id", 0))
        order_status = int(self.get_param("order_status", 0))
        express_company = self.get_param("express_company")
        express_no = self.get_param("express_no")

        prize_order_model = PrizeOrderModel()

        if order_status == 1:
            update_sql = "order_status=1,express_company=%s,express_no=%s,deliver_date=%s"
            params = [express_company, express_no, self.get_now_datetime(), prize_order_id]
            prize_order_model.update_table(update_sql, "id=%s", params)

            self.reponse_json_success({"express_company": express_company, "express_no": express_no, "deliver_date": self.get_now_datetime()})
        else:
            prize_order_model.update_table("order_status=%s", "id=%s", [order_status, prize_order_id])

            self.reponse_json_success()


class PrizeOrderRemarksHandler(SevenBaseHandler):
    """
    @description: 更新用户奖品订单备注
    """
    @filter_check_params("prize_order_id,remarks")
    def post_async(self):
        """
        @description: 更新用户奖品订单备注
        @param prize_order_id：奖品订单id
        @param remarks：备注
        @return: 
        @last_editors: HuangJingCan
        """
        prize_order_id = int(self.get_param("prize_order_id", 0))
        remarks = self.get_param("remarks")

        PrizeOrderModel().update_table("remarks=%s", "id=%s", [remarks, prize_order_id])

        self.reponse_json_success()


class PrizeOrderExportHandler(SevenBaseHandler):
    """
    @description: 批量导出
    """
    def get_async(self):
        """
        @description: 批量导出
        @param page_index：页索引
        @param page_size：页大小
        @param act_id：活动id
        @param order_no：订单号
        @param order_status：订单状态
        @param nick_name：用户昵称
        @return 字符串
        @last_editors: HuangJingCan
        """
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 500))
        act_id = int(self.get_param("act_id", 0))
        order_no = self.get_param("order_no")
        order_status = self.get_param("order_status")
        user_nick = self.get_param("nick_name")

        condition = "act_id=%s"
        params = [act_id]
        if order_no != "":
            condition = "order_no=%s"
            params.append(order_no)
        if user_nick != "":
            params.append(user_nick)
            if condition == "":
                condition = "user_nick=%s"
            else:
                condition += " and user_nick=%s"
        if order_status != "":
            params.append(int(order_status))
            if condition == "":
                condition = "order_status=%s"
            else:
                condition += " and order_status=%s"

        prize_order_model = PrizeOrderModel()
        prize_roster_model = PrizeRosterModel()

        #奖品订单
        prize_order_list_dict, total = prize_order_model.get_dict_page_list("*", page_index, page_size, condition, "", "create_date desc", params)

        data_columns = ["小程序订单号", "淘宝子订单号", "淘宝名", "盒子名称", "盒子价格", "奖品名称", "商家编码", "姓名", "手机号", "省份", "城市", "区县", "街道", "收货地址", "物流单号", "物流公司", "发货时间", "订单状态", "奖品价值", "奖品规格", "备注"]

        data_text = ",".join(list(map(lambda x: "\"" + x + "\"", data_columns))) + "\n"

        result_data = []
        if len(prize_order_list_dict) > 0:
            prize_order_id_list = [prize_order["id"] for prize_order in prize_order_list_dict]
            prize_order_ids = str(prize_order_id_list).strip('[').strip(']')
            #订单奖品
            prize_roster_list = prize_roster_model.get_dict_list("prize_order_id in (" + prize_order_ids + ")", order_by="id desc")

            for prize_order in prize_order_list_dict:
                prize_roster_list_filter = [prize_roster for prize_roster in prize_roster_list if prize_roster["prize_order_id"] == prize_order["id"]]
                for prize_roster in prize_roster_list_filter:

                    data_row = []
                    data_row.append("\'" + prize_order["order_no"])
                    data_row.append("\'" + prize_roster["order_no"])
                    data_row.append(prize_order["user_nick"])
                    data_row.append(prize_roster["machine_name"])
                    data_row.append(str(prize_roster["machine_price"]))
                    data_row.append(prize_roster["prize_name"])
                    data_row.append(prize_roster["goods_code"])
                    data_row.append(prize_order["real_name"])
                    data_row.append(prize_order["telephone"])
                    data_row.append(prize_order["province"])
                    data_row.append(prize_order["city"])
                    data_row.append(prize_order["county"])
                    data_row.append(prize_order["street"])
                    data_row.append(prize_order["adress"])
                    data_row.append(prize_order["express_no"])
                    data_row.append(prize_order["express_company"])
                    if str(prize_order["deliver_date"]) == "1900-01-01 00:00:00":
                        data_row.append("")
                    else:
                        data_row.append(str(prize_order["deliver_date"]))
                    data_row.append(self.get_status_name(prize_order["order_status"]))
                    data_row.append(str(prize_roster["prize_price"]))
                    data_row.append(prize_roster["properties_name"])
                    data_row.append(prize_order["remarks"])

                    data_text = data_text + ",".join(list(map(lambda x: "\"" + x + "\"", data_row))) + "\n"

        self.reponse_json_success(data_text)


class PrizeOrderImportHandler(SevenBaseHandler):
    """
    @description: 批量导入(批量发货)
    """
    @filter_check_params("content")
    def post_async(self):
        """
        @description: 批量导入(批量发货)
        @param content：内容
        @param act_id：活动id
        @return 
        @last_editors: HuangJingCan
        """
        content = self.get_param("content")
        act_id = int(self.get_param("act_id", 0))
        content_json = json.loads(content)

        prize_order_model = PrizeOrderModel()

        order_no_index = -1
        express_no_index = -1
        express_company_index = -1
        title_arr = content_json[0].replace("\'", "").split(",")
        if len(title_arr) == 0:
            return self.reponse_json_error("NoTitle", "对不起,未找到字段名称")

        title_arr_index = 0
        for title in title_arr:
            title = title.replace("\"", "").replace("\'", "")

            if "小程序订单号" == title:
                order_no_index = title_arr_index
            if "物流公司" == title:
                express_company_index = title_arr_index
            if "物流单号" == title:
                express_no_index = title_arr_index
            title_arr_index += 1

        if order_no_index == -1 or express_no_index == -1 or express_company_index == -1:
            return self.reponse_json_error("NoTitle", "对不起,缺少必要字段，无法导入订单")

        for i in range(1, len(content_json)):
            fields = content_json[i].replace("\'", "").split(",")
            if len(fields) == 0:
                continue

            #去掉多余的单（双）引号
            order_no = fields[order_no_index].replace("\"", "").replace("\'", "")
            express_no = fields[express_no_index].replace("\"", "").replace("\'", "")
            express_company = fields[express_company_index].replace("\"", "").replace("\'", "")

            if order_no and express_no and express_company:
                update_sql = "express_no=%s, express_company=%s, order_status=1, deliver_date=%s"
                params = [express_no, express_company, self.get_now_datetime(), order_no, act_id]
                prize_order_model.update_table(update_sql, "order_no=%s and act_id=%s ", params=params)

        self.reponse_json_success()


class PrizeRosterListExportHandler(SevenBaseHandler):
    """
    @description: 批量奖品列表导出
    """
    def get_async(self):
        """
        @description: 批量奖品列表导出
        @param page_index：页索引
        @param page_size：页大小
        @param act_id：活动id
        @param order_no：订单号
        @param order_status：订单状态
        @param nick_name：用户昵称
        @return 字符串
        @last_editors: HuangJingCan
        """
        page_index = int(self.get_param("page_index", 0))
        page_size = int(self.get_param("page_size", 500))
        act_id = int(self.get_param("act_id", 0))
        order_no = self.get_param("order_no")
        order_status = self.get_param("order_status")
        user_nick = self.get_param("nick_name")

        condition = "act_id=%s"
        params = [act_id]
        if order_no != "":
            condition = "order_no=%s"
            params.append(order_no)
        if user_nick != "":
            params.append(user_nick)
            if condition == "":
                condition = "user_nick=%s"
            else:
                condition += " and user_nick=%s"
        if order_status != "":
            params.append(int(order_status))
            if condition == "":
                condition = "order_status=%s"
            else:
                condition += " and order_status=%s"

        prize_order_model = PrizeOrderModel()
        prize_roster_model = PrizeRosterModel()

        #奖品订单
        prize_roster_list, total = prize_roster_model.get_dict_page_list("*", page_index, page_size, condition, order_by="id desc", params=params)

        data_columns = ["行为编号", "淘宝子订单号", "淘宝名", "盒子名称", "盒子价格", "奖品名称", "奖品价值", "SKU", "获得时间", "状态"]

        data_text = ",".join(list(map(lambda x: "\"" + x + "\"", data_columns))) + "\n"

        result_data = []
        if len(prize_roster_list) > 0:
            #订单奖品
            for prize_roster in prize_roster_list:
                data_row = []
                data_row.append(str(prize_roster["id"]))
                if prize_roster["order_no"] == "":
                    data_row.append(prize_roster["order_no"])
                else:
                    data_row.append("\'" + prize_roster["order_no"])
                data_row.append(prize_roster["user_nick"])
                data_row.append(prize_roster["machine_name"])
                data_row.append(str(prize_roster["machine_price"]))
                data_row.append(prize_roster["prize_name"])
                data_row.append(str(prize_roster["prize_price"]))
                data_row.append(prize_roster["properties_name"])
                data_row.append(TimeHelper.datetime_to_format_time(prize_roster["create_date"]))
                if prize_roster["prize_order_id"] == 0:
                    data_row.append("未下单")
                else:
                    data_row.append("已下单")
                data_text = data_text + ",".join(list(map(lambda x: "\"" + x + "\"", data_row))) + "\n"

        self.reponse_json_success(data_text)