"""
@author  : MG
@Time    : 2020/11/16 10:20
@File    : template.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
import pandas as pd
from ibats_utils.mess import datetime_2_str
from vnpy.app.cta_strategy import TargetPosTemplate as TargetPosTemplateBase
from vnpy.trader.object import OrderData, BarData

from quant_vnpy.backtest.cta_strategy.run import get_output_file_path
from quant_vnpy.config import logging


class TargetPosTemplate(TargetPosTemplateBase):

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.logger = logging.getLogger(strategy_name)
        self.orders = []
        self.current_bar = None

    def on_bar(self, bar: BarData):
        super().on_bar(bar)
        self.current_bar = bar

    def on_order(self, order: OrderData):
        super().on_order(order)
        self.write_log(
            f"{order.direction.value} {order.offset.value} {order.price:.1f}"
            if order.datetime is None else
            f"{datetime_2_str(order.datetime)} {order.direction.value} {order.offset.value} {order.price:.1f}"
        )
        self.orders.append(order)

    def on_stop(self):
        super().on_stop()
        order_df = pd.DataFrame([{
            "datetime": _.datetime,
            "symbol": _.symbol,
            "direction": _.direction.value,
            "offset": _.offset.value,
            "price": _.price,
            "volume": _.volume,
            "order_type": _.type.value,
        } for _ in self.orders])
        file_path = get_output_file_path(
            "data", "orders.csv",
            root_folder_name=self.strategy_name,
        )
        order_df.to_csv(file_path)
        self.logger.info('运行期间下单情况明细：\n%s', order_df)

    def write_log(self, msg: str):
        msg = f"{self.strategy_name} {msg}"
        super().write_log(msg)
        self.logger.info(msg)


if __name__ == "__main__":
    pass
