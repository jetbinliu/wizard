# -*- coding: UTF-8 -*-

import os
import configparser


from django.conf import settings

# Create your views here.
class Configuration(object):
    def __init__(self, filename):
        self.__BASE_DIR = settings.BASE_DIR
        self.__filename = os.path.join(self.__BASE_DIR, filename)

        try:
            self.__reader = configparser.ConfigParser()
            self.__reader.read(self.__filename)
        except Exception as e:
            print("get reader of ConfigParser failed.")
            self.__reader = None

    def get(self, section, option):
        if self.__reader == None:
            return None
        try:
            result = self.__reader.get(section, option)
        except Exception as e:
            # print("No [" + section +"]." + option + " in file " + self.__filename)
            print(e)
            return None
        return result

    def has_section(self, section):
        if self.__reader == None:
            return None
        try:
            result = self.__reader.has_section(section)
        except Exception as e:
            # print("No [" + section + "]." + " in file " + self.__filename)
            print(e)
            return None
        return result

    def has_option(self, section, option):
        if self.__reader == None:
            return None
        try:
            result = self.__reader.has_option(section, option)
        except Exception as e:
            # print("No [" + option +"]" + " in " + section + " in file " + self.__filename)
            print(e)
            return False
        return result
