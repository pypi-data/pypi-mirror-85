"""
@author  : MG
@Time    : 2020/9/2 16:58
@File    : config.py
@contact : mmmaaaggg@163.com
@desc    : 用于配置文件
"""
import logging
from logging.config import dictConfig
from datetime import time

# log settings
logging_config = dict(
    version=1,
    formatters={
        'simple': {
            'format': '%(asctime)s %(name)s|%(module)s.%(funcName)s:%(lineno)d %(levelname)s %(message)s'}
    },
    handlers={
        'file_handler':
            {
                'class': 'logging.handlers.RotatingFileHandler',
                'filename': 'logger.log',
                'maxBytes': 1024 * 1024 * 50,
                'backupCount': 5,
                'level': 'INFO',
                'formatter': 'simple',
                'encoding': 'utf8'
            },
        'console_handler':
            {
                'class': 'logging.StreamHandler',
                'level': 'DEBUG',
                'formatter': 'simple'
            }
    },

    root={
        'handlers': ['console_handler', 'file_handler'],
        'level': logging.INFO,
    }
)
dictConfig(logging_config)
logging.info("加载配置文件")

_INSTRUMENT_TRADE_TIME_PAIR_DIC = {
    "IF": ["9:30:00", "15:00:00"],
    "IC": ["9:30:00", "15:00:00"],
    "IH": ["9:30:00", "15:00:00"],
    "T": ["9:30:00", "15:15:00"],
    "AU": ["21:00:00", "2:30:00"],
    "AG": ["21:00:00", "2:30:00"],
    "CU": ["21:00:00", "1:00:00"],
    "AL": ["21:00:00", "1:00:00"],
    "ZN": ["21:00:00", "1:00:00"],
    "PB": ["21:00:00", "1:00:00"],
    "NI": ["21:00:00", "1:00:00"],
    "SN": ["21:00:00", "1:00:00"],
    "RB": ["21:00:00", "23:00:00"],
    "I": ["21:00:00", "23:00:00"],
    "HC": ["21:00:00", "23:00:00"],
    "SS": ["21:00:00", "1:00:00"],
    "SF": ["9:00:00", "15:00:00"],
    "SM": ["9:00:00", "15:00:00"],
    "JM": ["21:00:00", "23:00:00"],
    "J": ["21:00:00", "23:00:00"],
    "ZC": ["21:00:00", "23:00:00"],
    "FG": ["21:00:00", "23:00:00"],
    "SP": ["21:00:00", "23:00:00"],
    "FU": ["21:00:00", "23:00:00"],
    "LU": ["21:00:00", "23:00:00"],
    "SC": ["21:00:00", "2:30:00"],
    "BU": ["21:00:00", "23:00:00"],
    "PG": ["21:00:00", "23:00:00"],
    "RU": ["21:00:00", "23:00:00"],
    "NR": ["21:00:00", "23:00:00"],
    "L": ["21:00:00", "23:00:00"],
    "TA": ["21:00:00", "23:00:00"],
    "V": ["21:00:00", "23:00:00"],
    "EG": ["21:00:00", "23:00:00"],
    "MA": ["21:00:00", "23:00:00"],
    "PP": ["21:00:00", "23:00:00"],
    "EB": ["21:00:00", "23:00:00"],
    "UR": ["9:00:00", "15:00:00"],
    "SA": ["21:00:00", "23:00:00"],
    "C": ["21:00:00", "23:00:00"],
    "A": ["21:00:00", "23:00:00"],
    "CS": ["21:00:00", "23:00:00"],
    "B": ["21:00:00", "23:00:00"],
    "M": ["21:00:00", "23:00:00"],
    "Y": ["21:00:00", "23:00:00"],
    "RM": ["21:00:00", "23:00:00"],
    "OI": ["21:00:00", "23:00:00"],
    "P": ["21:00:00", "23:00:00"],
    "CF": ["21:00:00", "23:00:00"],
    "SR": ["21:00:00", "23:00:00"],
    "JD": ["9:00:00", "15:00:00"],
    "AP": ["9:00:00", "15:00:00"],
    "CJ": ["9:00:00", "15:00:00"]
}
INSTRUMENT_TRADE_TIME_PAIR_DIC = {
    key: [
        time(*[int(_) for _ in values[0].split(':')]),
        time(*[int(_) for _ in values[1].split(':')]),
    ]
    for key, values in _INSTRUMENT_TRADE_TIME_PAIR_DIC.items()}

if __name__ == "__main__":
    pass
