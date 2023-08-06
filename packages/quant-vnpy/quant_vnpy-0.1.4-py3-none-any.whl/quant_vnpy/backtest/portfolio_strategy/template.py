"""
@author  : MG
@Time    : 2020/11/16 10:20
@File    : template.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
from typing import List

import pandas as pd
from vnpy.app.portfolio_strategy import StrategyTemplate as StrategyTemplateBase
from vnpy.trader.constant import Direction, Offset

from quant_vnpy.backtest.cta_strategy.run import get_output_file_path
from quant_vnpy.config import logging


class StrategyTemplate(StrategyTemplateBase):

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.logger = logging.getLogger(strategy_name)
        self.orders = []

    def send_order(self,
                   vt_symbol: str,
                   direction: Direction,
                   offset: Offset,
                   price: float,
                   volume: float,
                   lock: bool = False
                   ) -> List[str]:
        self.orders.append({
            "vt_symbol": vt_symbol, "direction": direction.value,
            "offset": offset.value, "price": price, "volume": volume
        })
        return super(StrategyTemplate, self).send_order(vt_symbol, direction, offset, price, volume, lock)

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

    def on_stop(self):
        super().on_stop()
        order_df = pd.DataFrame(self.orders)
        file_path = get_output_file_path(
            "data", "orders.csv",
            root_folder_name=self.strategy_name,
        )
        order_df.to_csv(file_path)
        self.logger.info('运行期间下单情况明细：\n%s', order_df)


if __name__ == "__main__":
    pass
