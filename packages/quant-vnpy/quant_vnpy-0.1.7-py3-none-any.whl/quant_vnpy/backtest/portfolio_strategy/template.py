"""
@author  : MG
@Time    : 2020/11/16 10:20
@File    : template.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""
from datetime import datetime
from typing import List, Dict

import pandas as pd
from ibats_utils.mess import datetime_2_str
from vnpy.app.portfolio_strategy import StrategyTemplate as StrategyTemplateBase
from vnpy.trader.constant import Direction, Offset
from vnpy.trader.object import BarData

from quant_vnpy.backtest.cta_strategy.run import get_output_file_path
from quant_vnpy.config import logging


class StrategyTemplate(StrategyTemplateBase):

    def __init__(self, cta_engine, strategy_name, vt_symbol, setting):
        super().__init__(cta_engine, strategy_name, vt_symbol, setting)
        self.logger = logging.getLogger(strategy_name)
        self.orders = []
        self.current_bars = None

    def on_bars(self, bars: Dict[str, BarData]) -> None:
        super().on_bars(bars)
        self.current_bars = bars

    def send_order(self,
                   vt_symbol: str,
                   direction: Direction,
                   offset: Offset,
                   price: float,
                   volume: float,
                   lock: bool = False
                   ) -> List[str]:
        order_datetime = self.current_bars[vt_symbol].datetime if vt_symbol in self.current_bars else None
        self.write_log(f"{direction.value} {offset.value} {price:.1f}"
                       if order_datetime is None else
                       f"{datetime_2_str(order_datetime)} {direction.value} {offset.value} {price:.1f}")
        if order_datetime is None:
            order_datetime = datetime.now()

        self.orders.append({
            "datetime": order_datetime,
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
