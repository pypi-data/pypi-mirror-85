#!user/bin/python
# _*_ coding: utf-8 _*_
# @Author      :   Jesper
# @Time        :   2020/10/29 15:05
# @Description :
import json
from nlp_utils_ch.utils.logger import log

def show_json(data, prefix=None, is_indent=False):
	show_str = ""
	if is_indent:
		show_str = json.dumps(data, ensure_ascii=False, indent=4)
	else:
		show_str = json.dumps(data, ensure_ascii=False)

	if prefix and isinstance(prefix, str):
		show_str = prefix + ":"  + show_str

	log.info(show_str)
