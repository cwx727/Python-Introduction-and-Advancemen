'''
爬取页面需要的字段，并进行输出
'''

import requests
import json
import re

class Spider():
	def __init__(self, url, pattern_root, pattern_tclose, pattern_tradedate):
		self.url = url
		self.pattern_root = pattern_root
		self.pattern_tclose = pattern_tclose
		self.pattern_tradedate = pattern_tradedate

	def __response_get(self):
		'''
		获取html
		'''
		return requests.get(self.url).text

	def __analysis(self, response_str):
		'''
		正则获取需要的字段，并返回字典列表
		'''
		root_html = re.findall(self.pattern_root, response_str)
		anchors = []
		for html in root_html:
			tclose = re.findall(self.pattern_tclose, html)
			tradedate = re.findall(self.pattern_tradedate, html)
			anchor = {'tclose' : tclose, 'tradedate' : tradedate}
			anchors.append(anchor)
		return anchors

	def __refine(self, anchors):
		'''map和lambda处理analysis中的字段，并返回需要的格式的字典'''
		l = lambda anchor : { 'tradedate' : anchor['tradedate'][0], 'tclose' : anchor['tclose'][0]}
		return map(l, anchors)

	def __sort(self, anchors):
		'''按sort_seed中定义的字段进行排序'''
		anchors = sorted(anchors, key = self.__sort_seed)
		return anchors

	def __sort_seed(self, anchor):
		'''定义排序的字段'''
		return anchor['tradedate']

	def __show(self,anchors):
		'''按想要的格式进行打印'''
		for anchor in anchors:
			print(anchor['tradedate'] + '    ' + anchor['tclose'])


	def go(self):
		'''程序入口，进行执行'''
		response_str = self.__response_get()
		anchors = self.__analysis(response_str)
		anchors = list(self.__refine(anchors))
		anchors = self.__sort(anchors)
		self.__show(anchors)



if __name__ == '__main__':
	url = 'http://www.csindex.com.cn/zh-CN/indices/index-detail/000300?earnings_performance=5%E5%B9%B4&data_type=json'
	pattern_root = '"indx_code":"000300",(.*?),"changes"'
	pattern_tclose = '"tclose":"(.*?)"'
	pattern_tradedate = '"tradedate":"(.*?) 00:00:00"'
	res = Spider(url, pattern_root, pattern_tclose, pattern_tradedate).go()
	#print(res)
