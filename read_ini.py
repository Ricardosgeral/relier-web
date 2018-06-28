#! /usr/bin/python3.6
# -*- coding: utf-8 -*-
#Ricardos.geral@gmail.com

import configparser
config = configparser.ConfigParser()
config.read("./inputs.ini")
config.sections()

def read_ini_path(): ###read the init file
    path = config['path']['lastpath']
    interval = config['settings']['interval']
    return  path, interval