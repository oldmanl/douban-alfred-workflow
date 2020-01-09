# encoding: utf-8

import requests
import execjs 
import re
import io
from urllib import quote


def search(p):
	url = 'https://search.douban.com/movie/subject_search?search_text=' + quote(p) + '&cat=1002'
	response = requests.get(url)

	r = re.search('window.__DATA__ = "([^"]+)"', response.text).group(1)  # 加密的数据
	# 导入js
	with io.open('main.js', 'r', encoding='gbk') as f:
	    decrypt_js = f.read()

	ctx = execjs.compile(decrypt_js)
	data = ctx.call('decrypt', r)
	return data['payload']['items']



