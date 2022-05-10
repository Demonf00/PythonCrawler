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
	def __init__(self, url, header, others):
		self.url = url
		if header == None:
			self.header = {"user-agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.89 Safari/537.36", "cookie":"thw=cn; ??????????????????????????????"}
		else:
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


	def musicDownloader(self, originalPath, url="https://baidu.9ku.com/song/?key="):
		file = open(originalPath + 'songs.txt', 'r', encoding = 'utf-8')
		for line in file.readlines():
			line = line.strip('\n')
			line = re.findall('(?<=\.).*$', line)
			line = line[0]
			print(line)
			website = target(url + "{}".format(quote(line)), None, None)
			# bsObj = getSiteHtml("https://baidu.9ku.com/song/?key={}".format(quote(line)))
			try:
				bsObj = website.getSiteHtml()
				songList = bsObj.find("div", {"class":"songList"}).findAll("li")
				flag = 0
				for song in songList:
					songName = song.a.get_text()
					if (line in songName):
						songUrl = song.a["href"]
						try:
							newSite = target("https:" + songUrl, None, None)
							newObj = newSite.getSiteHtml()
							songNum = songUrl[len("//www.9ku.com/play/"):-4]
							newUrl = "https://m.9ku.com/play/{}.htm".format(songNum)				
							print(newUrl)
						except:
							continue
						driver = webdriver.Chrome(executable_path = "C://ChromeDriver/chromedriver.exe", chrome_options = chrome_options)
						driver.get(newUrl)
						wait = WebDriverWait(driver, 1000)
						html = driver.page_source
						newnewObj = BeautifulSoup(html, features = 'lxml')
						# print(newnewObj)
						original_window = driver.current_window_handle
						assert len(driver.window_handles) == 1
						# print(driver.current_url)
						driver.find_element_by_id("kw").send_keys("selenium")
						songSite = target(newUrl, None, None)
						newnewObj = songSite.getSiteHtml()
						# print(newnewObj)
						newnewUrl = newnewObj.find(re.compile("\.mp3$"))
						newnewUrl = newnewObj.findAll(re.compile("[A-Za-z]+"), src = re.compile(".+\.mp3.+$"))
						newnewUrl = newnewObj.find("audio", src = re.compile("\.mp3$"))["src"]
						print(newnewUrl)
						driver.close()
						try:
							# urlretrieve(newnewUrl, "D://music/lululu/" + songName + ".mp3")
							downloadFromUrl(newnewUrl, "D://music/lululu/" + songName + ".mp3")
							flag = 1
						except:
							print(newnewUrl, "\nCan not download!")
						newnewUrl = newnewObj.find("div", {"class":"player-wrap"}).find("div", {"style":"display: none;width: 0;height: 0;opacity: 0;"})
						if flag == 1:
							break
				if flag == 0:
					print(line, "not found!")
			except:
				print(line, "not found!")
				continue
		file.close()


def downloadFromUrl(url, dst):
	try:
		response = requests.get(url, stream=True)
		file_size = int(response.headers['content-length'])
		if file_size != 259:
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
		else:
			return file_size
	except:
		return None


