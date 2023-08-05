#!/usr/bin/env python3.6
#! -*- coding: utf-8 -*-


class baicaoluexception(Exception):
    def __init__(self, msg):
        self.msg = msg


class InvalidSystemClock(Exception):
    """
    时钟回拨异常
    """
    pass
