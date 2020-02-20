#!/usr/bin/env python

# author Huy
# date 9/3/2019
import re

import math
import pandas
from rest_framework.exceptions import ValidationError

from api.models import User
from api.services import BaseService


class ImportService(BaseService):
    """
    FILE EXCEL READER SERVICE
    """

    @staticmethod
    def read_excel(file):
        try:
            return pandas.read_excel(file)
        except:
            raise ValidationError("Input file is not valid")

    @staticmethod
    def get_service(file):
        try:
            df = pandas.read_excel(file)
            instance = ExcelImportService()
            return df, instance
        except:
            raise ValidationError('Input file is not valid')

    def check_import(self, df, data):
        raise Exception("Must be implemented")

    def run_import(self):
        raise Exception("Must be implemented")


class ExcelImportService(ImportService):
    """
    CHECK IMPORT METHOD
    """

    def __init__(self):
        self.rows = []
        self.valid_email = []
        self.invalid_email = []
        self.current_row = None
        self.status = None
        self.email = None
        self.name = None
        self.phone = None

    def check_import(self, df, data):
        email_regex = "^\w+([\.-]?\w+)*@\w+([\.-]?\w+)*(\.\w{2,3})+$"
        email_col = data['email']
        name_col = data['name']
        phone_col = data['phone']
        for i in df.index:
            self.phone = None
            self.current_row = str(i + 2)
            self.email = str(df[email_col][i])
            self.name = str(df[name_col][i])
            if phone_col and re.search('\d{9,11}', str(df[phone_col][i])) and not math.isnan(int(df[phone_col][i])):
                self.phone = str((df[phone_col][i]))
            if not (re.search(email_regex, self.email)):
                self.status = 'Invalid email format'
                self.append_status(email_list=self.invalid_email,
                                   success=False)
                continue
            existed = User.objects.filter(email=self.email).count()
            if existed:
                self.status = 'Already existed'
                self.append_status(email_list=self.invalid_email,
                                   success=False)
                continue
            if self.email in self.valid_email:
                self.status = 'Duplicate in file'
                self.append_status(email_list=self.invalid_email,
                                   success=False)
                continue
            self.status = 'Valid email'
            self.append_status(email_list=self.valid_email,
                               success=True)
        return {'rows': self.rows,
                'valid': self.valid_email,
                'invalid': self.invalid_email}

    def append_status(self, email_list, success):
        email_list.append(self.email)
        self.rows.append({
            'row': self.current_row,
            'email': self.email,
            'name': self.name,
            'phone': self.phone,
            'status': self.status,
            'success': success
        })
