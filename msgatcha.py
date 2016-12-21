# -*- coding: utf-8 -*-
import re
import binascii
import time
import urllib
import random
import urllib.request
import html.parser
import requests
from requests.exceptions import HTTPError
from socket import error as SocketError
from http.cookiejar import CookieJar
from bs4 import BeautifulSoup
import gzip
import io
import json
import mysql.connector
import sys

#字典，用来显示珠的名称
dict = {'2241' : '南丁格尔', '1936' : '罗宾', '2257' : '但丁', '2251' : '安徒生', '890' : '米迦勒', '2216' : '伦勃朗', 
	'2063' : '圣盾', '566' : '生成神', '1030' : '暗天', '1742' : '木天', '2125' : '茶茶', '2280' : '珊瑚', '226' : '真珠', '2307' : '蔵马', '929' : '光天', '374' : '兰斯x',
	'214' : '莉娜'
	}
#需要抽的珠id，二维数组，可以同时统计一只珠的进化、神化编码
monstid = [['374'],['890']]
#每个要抽的珠15分钟内出了超过condcount次就打印出来
condcount = 1
#检查抽珠情况的间隔时间，单位秒
timeinterval = 15
#是否显示机率描述
showHint = False

jsonBegin = '''renderCards({
      raw: \''''
jsonEnd = '''\',
      layout:'''

while 1:
	try:
		url = 'http://monnsutogatya.com/v2/kako30.php?' + str(random.random())

		req = urllib.request.Request(url, None, {'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
			'Accept-Encoding':'gzip, deflate, sdch','Accept-Language':'zh-CN,zh;q=0.8', 'Cache-Control':'max-age=0', 
			'Connection':'keep-alive', 'Cookie':'__cfduid=d0c3393e3eb7afc0842b7dfd49567d5f41474721630; template=v1; gw_access=1474721674328; crtg_amoad_rta=; _gat=1; _ga=GA1.2.649995010.1474721621', 
			'Host':'monnsutogatya.com', 'If-Modified-Since':'Fri, 14 Oct 2016 04:45:01 GMT','If-None-Match':'580062cd-a0bf', 
			'Upgrade-Insecure-Requests':'1','User-Agent':'Mozilla/5.0 (Windows NT 5.2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.112 Safari/537.36'})
		cj = CookieJar()
		opener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cj))
		response = opener.open(req)
		if url != response.geturl():
			print(response.geturl())
		bs = response.read()
		bi = io.BytesIO(bs)
		raw_response = gzip.GzipFile(fileobj=bi, mode="rb").read()
		response.close()
		
		soup = BeautifulSoup(raw_response, 'html.parser')
		
		script = soup.find_all(class_='cards-render-script')
		script = script[0].string.strip()
		script = script[len(jsonBegin) : script.find(jsonEnd)].strip()
		script = script.replace('\\', '')
		dataHtml = BeautifulSoup(script, 'html.parser')
		monsters = dataHtml.find_all('div')

		istime = False

		for mid in monstid:
			mcount = 0
			timeg = []
			for m in monsters:
				href = m.find('a').get('href')
				
				for midd in mid:
					if href.count('/' + midd + '.') > 0:
						mcount = mcount + 1
						p = m.find('p').string
						timeg.append(p)
			
			if mcount > condcount:
				istime = True
				print(dict[mid[0]] + ': ' + str(timeg))

		if istime == True:
			report = soup.find(id='tab_3m')
			gccount = str(report.find_all(class_='font13')[0]).replace('<span class="font9">回</span>', '').replace('<span class="font13">', '').replace('</span>', '').strip()
			fscount = str(report.find_all(class_='font13')[1]).replace('<span class="font9">回</span>', '').replace('<span class="font13">', '').replace('</span>', '').strip()
			percent = str(report.find_all(class_='font14')[0]).replace('<span class="font-theme font14 emphasis">', '').replace('</span>', '').replace('<span class="font9">回</span>', '').strip()

			print('ガチャ回数:' + gccount + '    ★5当たり回数:' + fscount + '    ★5の確率:' + percent + '%')
			print('')

		if showHint and soup.find(src='http://image.monnsutogatya.com/himg/monst/r04.jpg'):
			print(time.strftime('%H:%M:%S',time.localtime(time.time())) + '——极大')
			print('')

		time.sleep(timeinterval)
	except urllib.request.HTTPError as inst:
		output = format(inst)
		print(output)
