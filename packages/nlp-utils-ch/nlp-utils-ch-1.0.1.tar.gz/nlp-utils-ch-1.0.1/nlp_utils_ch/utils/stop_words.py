#!user/bin/python
# _*_ coding: utf-8 _*_
# @Author      :   Jesper
# @Time        :   2020/11/11 20:31
# @Description :

import os
current_dir = os.path.dirname(__file__)

symbol_path = os.path.join(current_dir, "../resources/symbol.txt")

symbol_chars = list()


with open(symbol_path, "r") as f:
	for line in f.readlines():
		symbol_chars.append(line.strip())
