# -*- coding: utf-8 -*-
from  config_manager import Config

config  = Config()
options = config.parse_section("OPTION")
paths   = config.parse_section("PATH")
pc_w = config.parse_section("PARAMS_W")
pc_c = config.parse_section("PARAMS_C")
pc_a = config.parse_section("PARAMS_A")
nb = config.parse_section("NETBOX")
disp = config.parse_section("DISPLAY")
shapes  = ["","ellipsoid","paralellipiped","cilindr"]