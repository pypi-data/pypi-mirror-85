"""
@author  : MG
@Time    : 2020/11/12 10:04
@File    : constants.py
@contact : mmmaaaggg@163.com
@desc    : 用于保存部分公共常数
"""
import collections

# 记录每个合约乘数的dict
SYMBOL_SIZE_DIC = {
    "CU": 5.0,
    "ZC": 100.0,
    "PP": 5.0,
    "V": 5.0,
    "C": 10.0,
    "SN": 1.0,
    "AL": 5.0,
    "P": 10.0,
    "IC": 200.0,
    "ZN": 5.0,
    "L": 5.0,
    "RB": 10.0,
    "M": 10.0,
    "T": 10000.0,
    "SR": 10.0,
    "CS": 10.0,
    "IH": 300.0,
    "CF": 5.0,
    "JM": 60.0,
    "TA": 5.0,
    "ME": 50.0,
    "RU": 10.0,
    "A": 10.0,
    "PB": 5.0,
    "B": 10.0,
    "OI": 10.0,
    "FG": 20.0,
    "JD": 10.0,
    "AU": 1000.0,
    "AG": 15.0,
    "RO": 5.0,
    "TF": 10000.0,
    "Y": 10.0,
    "TC": 200.0,
    "NI": 1.0,
    "BU": 10.0,
    "J": 100.0,
    "TS": 20000.0,
    "HC": 10.0,
    "SC": 1000.0,
    "IF": 300.0,
    "MA": 10.0,
    "RM": 10.0,
    "I": 100.0
}

# 记录每个合约每天分钟数的dict
SYMBOL_MINUTES_COUNT_DIC = collections.defaultdict(
    lambda: 350, [
        ('RB', 350),
        ('I', 380),
        ('HC', 350),
    ])
