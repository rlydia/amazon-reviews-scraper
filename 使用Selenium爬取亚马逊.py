from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from pyquery import PyQuery as pq  
import re
import csv
import time
import sys

class AmazonSelenium():
	# 初始化数据
	def __init__(self):
		self.browser = webdriver.Chrome()
		self.wait = WebDriverWait(self.browser, 10)  #等待10秒
		# （1）必须修改替换
		# .get("")中替换为所需爬取商品的评论页面链接
		self.browser.get("https://www.amazon.com/ZTE-Clamshell-Prepaid-Annual-Contract/product-reviews/B00Q1U31VI/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews")

		# 设置scv文件
		# （2）必须修改替换
		#  替换为所爬取商品的ASIN，
		self.ASIN = 'B00Q1U31VI'
		#  替换为自定义文件名称
		self.CsvFileName = 'test.csv'
		# 存储csv数据
		self.CsvData = []
		# （3）可修改替换
		#  CsvN用于计数--当前爬取页数
		self.CsvN = 1
		# 设置csv文件首行
		with open(self.CsvFileName, 'a', newline='') as csvfile:
			spamwriter = csv.writer(csvfile)
			spamwriter.writerow(["Asin", "reviewerName", "Rating", "reviewText"])

	#得到亚马逊评论信息
	def get_reviews(self):
		#等待页面显示
		time.sleep(5)
		#让浏览器滚动到底部
		for x in range(1,8):
			j = x / 8
			js = "document.documentElement.scrollTop = document.documentElement.scrollHeight*%f"%j
			self.browser.execute_script(js)
			#每次滚动等待2s
			time.sleep(2)
		self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#cm_cr-review_list .review'))) # 定位到页面全部单个评论信息
		html = self.browser.page_source  #页面源码
		doc = pq(html) 
		items = doc('#cm_cr-review_list .review').items()
		for item in items:
			d = [
				self.ASIN,
				item.find('.a-profile-content .a-profile-name').text(),
				int(item.find('.review-rating .a-icon-alt').text()[0]),
				item.find('.review-text').text(),
			]
			self.CsvData.append(d)

		# 将数据写入csv文件
		with open(self.CsvFileName, 'a', encoding='utf-8', newline='') as csvfile:
			spamwriter = csv.writer(csvfile)
			# 将CsvData中的数据循环写入CsvFileName文件中
			for item in self.CsvData:
				spamwriter.writerow(item)
			print("成功导出CSV文件-" + str(self.CsvN))
		self.CsvN += 1
		self.CsvData = []
		self.next_page()

	#跳转到下一页
	def next_page(self):
		try:
			nextpage = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#cm_cr-pagination_bar > ul.a-pagination > li.a-last")))  #定位：下方页码"Next"按钮
			nextpage.click()  #相当于鼠标左键点击
			wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#cm_cr-pagination_bar > ul.a-pagination > li.a-selected.page-button > a"),str(page_number)))   #定位：下方当前页码块页数,判断元素中是否存在page_number文本
			self.get_reviews()
		except Exception as e:
			print("404 error!%s" % e)

#实例化类
a = AmazonSelenium()
# 执行方法
a.get_reviews()
