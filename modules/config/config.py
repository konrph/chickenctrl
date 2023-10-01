#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

import configparser
import os

class Config:

    def __init__(self):
        self.conf = self.read_config()

    def read_config(self):
        config = configparser.ConfigParser(strict=True)
        config.read('../chickenctrl.conf')
        return config
