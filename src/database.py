#!/usr/bin/env python
# -*- coding: utf-8 -*-


class Database:
    def __init__(self):
        self.records = []

    def add_record(self, record):
        self.records.append(record)

    def get_records(self):
        return self.records
