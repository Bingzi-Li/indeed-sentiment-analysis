from urllib.request import urlopen, urlretrieve
import os
import re
from shutil import copyfile
from selenium import webdriver
from time import sleep
import base64
from bs4 import BeautifulSoup, NavigableString
import pandas as pd
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from io import BytesIO
from PIL import Image
from selenium.webdriver.common.action_chains import ActionChains
import os, ssl
if (not os.environ.get('PYTHONHTTPSVERIFY', '') and getattr(ssl, '_create_unverified_context', None)):
	ssl._create_default_https_context = ssl._create_unverified_context

options = webdriver.ChromeOptions()
options.add_argument('--disable-notifications')
#options.add_argument("user-data-dir=selenium")

options.add_argument("start-maximized")
options.add_argument("disable-infobars")
options.add_argument("headless")
options.add_argument("--disable-extensions")
options.add_argument("--disable-gpu")
options.add_argument("--disable-dev-shm-usage")
options.add_argument("--no-sandbox")
options.add_argument("--window-size=1920,1080")
browser = webdriver.Chrome(options=options)


SCRAPED_PATH = "scrape.csv"

BASE_DIR = "out/"
Review_DIR = "reviews/"
META_PATH = "metadata.csv"

meta_list = []

id = 0

# Get scraped links
frame = pd.read_csv(SCRAPED_PATH)
sr = list(frame["URL"])

def process_urls(urls):
	# Process links

	for url in urls:
		category = frame.loc[frame['URL'] == url]['Category'].values[0]
		print(category)
		process_url(category,url+'/reviews')
		process_url(category,url + '/reviews?start=20')
		process_url(category,url + '/reviews?start=40')
		process_url(category,url + '/reviews?start=60')
		process_url(category,url + '/reviews?start=80')
		process_url(category, url + '/reviews?start=100')
		process_url(category, url + '/reviews?start=120')
		process_url(category, url + '/reviews?start=140')
		process_url(category, url + '/reviews?start=160')
		process_url(category, url + '/reviews?start=180')


	# Store meta lists
	meta_df = pd.DataFrame(meta_list)
	meta_df.to_csv(index=False, path_or_buf=META_PATH)
 
	print("complete")

def process_url(cat,url):
	global id
	print(url)
	category=cat

	try:
		html = urlopen(url).read()
		soup = BeautifulSoup(html, "html.parser")

		if not soup.body:
			print("not soup.body")
			return

		# got reviews
		review = ""
		reviews = soup.body.find_all(class_='cmp-Review-container')

		if not reviews:
			print("no reviews")
			return

		browser.get(url)

		S = lambda X: browser.execute_script("return document.body.parentNode.scroll" + X)
		browser.set_window_size(S("Width"), S("Height"))
		# # Handle cookies
		# cookieButton = browser.find_elements_by_css_selector("#onetrust-accept-btn-handler")
		# print(cookieButton)
		# if len(cookieButton) > 0:
		# 	cookieButton[0].click()

		# # Handle Expand button
		# ExpandButton = browser.find_elements_by_css_selector(".button.button--primary.lightButton.lightButton--hollow.margin-top-20.font-size-15px")
		# print(ExpandButton)
		# if len(ExpandButton) > 0:
		# 	print("press Expand Button")
		# 	ExpandButton[0].click()
		# 	otherPlace = browser.find_element_by_css_selector(".highcharts-axis-labels")
		# 	print(otherPlace)
		# 	action = ActionChains(browser)
		# 	action.move_to_element(otherPlace).perform()
		# sleep(1)

		for rev in reviews:
			# Get title
			titleElement = rev.find(class_='cmp-Review-title')
			print(titleElement)
			title = titleElement.get_text() if titleElement else ""

			# Get review elements
			review = ""
			review = rev.find(class_='cmp-Review-text')
			# remove /n, /r, /t
			regex = re.compile(r'[\n\r\t]')
			cleanText = regex.sub(" ", review.get_text())
			# remove extra whitespace
			cleanText = re.sub("\s\s+", " ", cleanText)
			review=cleanText
			print(review)

			# get author information
			author=""
			author= rev.find(class_='cmp-Review-author')
			# remove /n, /r, /t
			regex = re.compile(r'[\n\r\t]')
			cleanText = regex.sub(" ", author.get_text())
			# remove extra whitespace
			cleanText = re.sub("\s\s+", " ", cleanText)
			author = cleanText
			print(author)
			info=author.split('-')
			if(len(info)>3):
				date = info[-1]
				place = info[-2]
				job = '-'.join(info[-3::-1])
			else:
				job=info[0]
				place=info[1]
				date=info[2]
			print("job:",job,"place:",place,"date:",date)

			id += 1
			print("id:", id)
			process_data(id, category, url, review, title, job, place, date)

	except Exception as ex:
		print(ex)


def process_data(id, category, url, reviewText, title, job, place, date):
	# Paths

	reviewPath = BASE_DIR + Review_DIR + str(id) + ".txt"

	# Save reviews
	with open(reviewPath, "w", encoding='utf-8') as f:
		f.write(reviewText)

	meta_list.append({
		'category':category,
		'id': id,
		'title': title,
		'review': reviewText,
		'job':job,
		"place":place,
		"date":date,
		'URL': url
	})
process_urls(sr)
