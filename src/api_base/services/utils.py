#! /usr/bin/python
#
# Copyright (C) 2020 paradox.ai
#

__author__ = "huy.tran@paradox.ai"
__date__ = "03/06/2020 16:35"

import datetime
import json

from api_base.services import BaseService


class Utils(BaseService):

    @staticmethod
    def convert_to_int(string):
        try:
            number = int(string)
        except ValueError:
            number = 0
        return number

    @staticmethod
    def nextmonth(year, month):
        if month == 12:
            return year + 1, 1
        else:
            return year, month + 1

    @staticmethod
    def get_current_date():
        current_day = datetime.datetime.now()
        return current_day.month, current_day.year

    @staticmethod
    def safe_jsonloads(val, default=None):
        try:
            return json.loads(val)
        except:
            return default
