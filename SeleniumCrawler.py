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
	def __init__(self):
		self.browser = webdriver.Chrome()
		self.wait = WebDriverWait(self.browser, 10) 
		self.browser.get("https://www.amazon.com/ZTE-Clamshell-Prepaid-Annual-Contract/product-reviews/B00Q1U31VI/ref=cm_cr_dp_d_show_all_btm?ie=UTF8&reviewerType=all_reviews")

		self.ASIN = 'B00Q1U31VI'
		self.CsvFileName = 'test.csv'
		self.CsvData = []
		self.CsvN = 1

		with open(self.CsvFileName, 'a', newline='') as csvfile:
			spamwriter = csv.writer(csvfile)
			spamwriter.writerow(["Asin", "reviewerName", "Rating", "reviewText"])

	def get_reviews(self):
		time.sleep(5)
		for x in range(1,8):
			j = x / 8
			js = "document.documentElement.scrollTop = document.documentElement.scrollHeight*%f"%j
			self.browser.execute_script(js)
			time.sleep(2)
		self.wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '#cm_cr-review_list .review'))) 
		html = self.browser.page_source
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

		with open(self.CsvFileName, 'a', encoding='utf-8', newline='') as csvfile:
			spamwriter = csv.writer(csvfile)
			for item in self.CsvData:
				spamwriter.writerow(item)
			print("成功导出CSV文件-" + str(self.CsvN))
		self.CsvN += 1
		self.CsvData = []
		self.next_page()

	def next_page(self):
		try:
			nextpage = self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "#cm_cr-pagination_bar > ul.a-pagination > li.a-last")))
			nextpage.click()
			wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "#cm_cr-pagination_bar > ul.a-pagination > li.a-selected.page-button > a"),str(page_number)))   #定位：下方当前页码块页数,判断元素中是否存在page_number文本
			self.get_reviews()
		except Exception as e:
			print("404 error!%s" % e)

a = AmazonSelenium()
a.get_reviews()
