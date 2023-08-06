"""
Setup coloredlogs
"""
import os
import logging
import coloredlogs


log = logging.getLogger("sdm")
fmt = "%(asctime)s:%(msecs)03d %(name)s [%(filename)s:%(lineno)s] %(levelname)s %(message)s"


def set_log_level(level="DEBUG"):
    coloredlogs.install(level=level, logger=log, fmt=fmt)
