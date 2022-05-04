import requests
from tqdm import tqdm
import os
from urllib.request import urlopen, quote, urlretrieve
from urllib.error import HTTPError
from bs4 import BeautifulSoup
import datetime
import random
import re
from urllib.request import urlopen
from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import time
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select

class target:
	def __init__(self,\
				 url,\
				 header = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36", "cookie":"thw=cn; ??????????????????????????????"},\
				 others):
		self.url = url
		self.header = header


	def downloadPage(self):
		data = requests.get(self.url, headers = self.header).content
		return data

	def getSiteHtml(self):
		try:
			html = downloadPage(self)
		except HTTPError as e:
			return None

		bsObj = BeautifulSoup(html.read(), features = 'lxml')
		return bsObj

	def getTitle(self):
		try:
			bsObj = getSiteHtml(self)
			title = bsObj.body.h1
		except AttributeError as e:
			return None
		return title

	


def download_from_url(url, dst):
	response = requests.get(url, stream=True)
	file_size = int(response.headers['content-length'])
	if os.path.exists(dst):
		first_byte = os.path.getsize(dst)
	else:
		first_byte = 0
	if first_byte >= file_size:
		return file_size
	header = {"Range": f"bytes={first_byte}-{file_size}"}
	pbar = tqdm(
		total=file_size, initial=first_byte,
		unit='B', unit_scale=True, desc=dst)
	req = requests.get(url, headers=header, stream=True)
	with(open(dst, 'ab')) as f:
		for chunk in req.iter_content(chunk_size=1024):
			if chunk:
				f.write(chunk)
				pbar.update(1024)
	pbar.close()
	return file_size
