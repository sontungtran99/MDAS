#!/usr/bin/python
# -*- coding: utf8 -*-

from bs4 import BeautifulSoup
import urllib.request
import re
from data.Location import db_locations, Location
import time
from itertools import permutations

sac = 'á ắ ấ é ế ó ố ớ í ú ứ ý'.split()
huyen = 'à ầ ằ è ề ò ố ớ ì ù ừ ỳ'.split()
nang = 'ạ ặ ậ ẹ ệ ọ ộ ợ ị ụ ự ỵ'.split()
nga = 'ã ẵ ẫ ẽ ễ õ ỗ ỡ ĩ ũ ữ ỹ'.split()
hoi = 'ả ẩ ẳ ẻ ể ỏ ổ ở ỉ ủ ử ỷ'.split()
accents = []
accents.extend(sac)
accents.extend(huyen)
accents.extend(nang)
accents.extend(nga)
accents.extend(hoi)
vowels = 'u e o a i'.split()

def getInfo(prevAlertLink):
	''' Returns a string of message and a list of:
		location[0] (a district), and
		location[1] (a province) 
	 Ex: locations = [['Thanh Xuân', 'Hà Nội'], 
					   ['Đống Đa', 'Hà Nội']]
	'''

	root = 'http://www.nchmf.gov.vn'
	link = 'http://www.nchmf.gov.vn/Web/vi-VN/69/50/Default.aspx'
	raw = urllib.request.urlopen(link).read()
	soup = BeautifulSoup(raw, features='lxml')
	alertNews = soup.find_all('a', class_='tieude_tintuc')
	alertLatest = alertNews[0]
	
	alertLatestName = alertLatest.find('strong').text
	alertLatestTime = alertLatest.parent.find('span', class_='Time_News')\
			       .text.strip().strip('()')
	alertLatestLink = root + alertLatest['href']

	if alertLatestLink == prevAlertLink or alertName[:9].lower() != 'tin nhanh':
		return '', ['','']
	else:
		pass

	alertRaw = urllib.request.urlopen(alertLink).read()
	alertSoup = BeautifulSoup(alertRaw, features='lxml')

	# Problems with acquiring content TODO
	content = alertSoup.find('td', class_='ContentNews')
	content = content.text.strip()

	return textProcessing(content, alertName)	# (message, locations)
	

def textProcessing(content, alertName):
	# This returns a message and a list of locations
	warning = re.findall(u'(Cảnh báo.*)', content)[0]
	print(warning)
	warningLvl = re.findall('ủi ro thiên tai(.*)', content)[0]
	warningLvl = rmv(warningLvl) #TODO

	issueTimeStr = re.findall(u'Tin phát lúc(.*)', content)[0]
	issueTimeStr = re.findall('([0-2]?[0-9][h|:][0-5][0-9])', issueTimeStr)[0]	
	currentTimeStruct = time.localtime(time.time())
	currentTime = (currentTimeStruct.tm_hour, currentTimeStruct.tm_min)
	issueTime = (int(issueTimeStr[:issueTimeStr.lower().index('h')]), int(issueTimeStr[:len(issueTimeStr)-3]))
	if (issueTime[0]-currentTime[0]) == 0 and (issueTime[1] - currentTime[1]) < 15:
		#timeOccur = 
		pass
	timeOccur = '3 đến 6 giờ'

	locations = findLocations(warning)
	message = 'Trong ' + timeOccur + ' tới, ' + alertName[10:] + ' với cấp độ ' +  warningLvl # TODO
	return message, locations

def findLocations(content):
	'''Task: Distinguish between other stuffs and legitimate locations 
	 Assume that locations don't start exactly after the first 
	 word in the sentence, e.g. "Tại Thanh Hóa, ..."
	   Solution: Split content by spaces
				Join words that is capitalized at the first char
				Stop joining more words if find special char at the last char
	   Special situation: first char is '(' as in '(Thanh Hóa)' would be
	ignored, find after that instead'''
	
	words = content.split()
	possibleLocations = []
	tempLoc = ''
	for word in words:
		if word[0].isupper():
			tempLoc += word + ' '
		elif len(word) > 1 and word[1].isupper():
			possibleLocations.append(tempLoc.strip())
			tempLoc = ''
			tempLoc += word[1:] + ' '
		else:
			possibleLocations.append(tempLoc.strip())
			tempLoc = ''
			continue

		if not word[-1].isalpha():
			possibleLocations.append(tempLoc[:len(tempLoc)-2].strip(')'))
			tempLoc = ''
		else:
			continue

	possibleLocations = [loc for loc in possibleLocations if loc != '']

	l = []
	for loc in possibleLocations:
		tempWords = [] # [['this', 'that'], ['these', 'those']] to combine into 'this these', 'this those' and so on.
		for word in loc.split():
			words = accentPermutations(word)
			tempWords.append(words)
		# Combinations of words.
		num = '' 
		for words in tempWords:
			num += str(len(words))

		combinePatterns = permutationSpecial(num)
		for pattern in combinePatterns:
			word = ''
			for i in range(len(pattern)):
				word += tempWords[i][int(pattern[i])-1] + ' '
			l.append(word[:len(word)-1])

	possibleLocations = l
	print(possibleLocations)

	locations = tracebackLoc(possibleLocations)
	return locations

def rmv(s):
	# Remove the ':' at the beginning then strip
	if s[0] == ':':
		return s[1:].strip()
	else:
		return s.strip()

def accentPermutations(s):
	# Create permutations based on possible location of
	# the accent:
	# vãi == "va"+"ĩ"
	#
	# First, for each word, find if there're more than 2 vowels
	# Second, find the type of accent available
	# Third, return permutations
	count = 0
	index = [-1,-1] # index[0] = index of word with accent
	for i in range(len(s)):
		if nav(s[i]) in vowels:
			count += 1
			if s[i] in accents:
				index[0] = i
			else:
				index[1] = i

	if count < 2:
		return [s]
	else:
		if s[index[0]] in sac:
			temp = accentize(s[index[1]], 'sac')
		elif s[index[0]] in huyen:
			temp = accentize(s[index[1]], 'huyen')
		elif s[index[0]] in nang:
			temp = accentize(s[index[1]], 'nang')
		elif s[index[0]] in nga:
			temp = accentize(s[index[1]], 'nga')
		elif s[index[0]] in hoi:
			temp = accentize(s[index[1]], 'hoi')
		else:
			return [s]

		s2_list = list(s)
		s2_list[index[1]] = temp
		s2_list[index[0]] = naev(s2_list[index[0]])
		s2 = ''.join(s2_list)
		return [s, s2]

def accentize(char, type):
	if type == 'sac':
		for i in range(len(sac)):
			if naev(sac[i]) == char:
				return sac[i]
	elif type == 'huyen':
		for i in range(len(huyen)):
			if naev(huyen[i]) == char:
				return huyen[i]
	elif type == 'nga':
		for i in range(len(huyen)):
			if naev(nga[i]) == char:
				return nga[i]
	elif type == 'nang':
		for i in range(len(huyen)):
			if naev(nang[i]) == char:
				return nang[i]
	elif type == 'hoi':
		for i in range(len(huyen)):
			if naev(hoi[i]) == char:
				return hoi[i]
	else:
		raise Exception('Type in accentize function is invalid')

		   
def permutationSpecial(s, l=[], count=0):
	# s is a number, e.g: '212'
	# l is a list of nums that will also be the result
	# count is the index currently processed
	# Example: '212' -> ['111', '211', '212', '112']
	#		   '332' -> ['111', '211', '311', '121', '131', '221', '231', ...]

	if count == len(s):
		return l
	else:
		if count == 0:
			l = ['1' * len(s)]

		lTemp = []
		for num in l:
			numTemp = list(num)
			for i in range(1,int(s[count])):
				numTemp[count] = str(int(numTemp[count]) + 1)
				lTemp.append(''.join(numTemp))
		count += 1
		l.extend(lTemp)
		return permutationSpecial(s, l=l, count=count)


def naev(s):
        # No Accent Extended Vietnamese
        s = re.sub(u'[àáạảã]', 'a', s)
        s = re.sub(u'[âầấậẩẫ]', 'â', s)
        s = re.sub(u'[ăằắặẳẵ]', 'ă', s)
        s = re.sub(u'[ÀÁẠẢÃ]', 'A', s)
        s = re.sub(u'[ĂẰẮẶẲẴ]', 'Ă', s)
        s = re.sub(u'[ÂẦẤẬẨẪ]', 'Â', s)
        s = re.sub(u'[èéẹẻẽ]', 'e', s)
        s = re.sub(u'[êềếệểễ]', 'ê', s)
        s = re.sub(u'[ÈÉẸẺẼ]', 'E', s)
        s = re.sub(u'[ÊỀẾỆỂỄ]', 'Ê', s)
        s = re.sub(u'[òóọỏõ]', 'o', s)
        s = re.sub(u'[ôồốộổỗ]', 'ô', s)
        s = re.sub(u'[ơờớợởỡ]', 'ơ', s)
        s = re.sub(u'[ÒÓỌỎÕ]', 'O', s)
        s = re.sub(u'[ÔỒỐỘỔỖ]', 'Ô', s)
        s = re.sub(u'[ƠỜỚỢỞỠ]', 'Ơ', s)
        s = re.sub(u'[ìíịỉĩ]', 'i', s)
        s = re.sub(u'[ÌÍỊỈĨ]', 'I', s)
        s = re.sub(u'[ùúụủũưừứựửữ]', 'u', s)
        s = re.sub(u'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
        s = re.sub(u'[ỳýỵỷỹ]', 'y', s)
        s = re.sub(u'[ỲÝỴỶỸ]', 'Y', s)
        return s

def nav(s):
        # No Accent Vietnamese
        s = re.sub(u'[àáạảãâầấậẩẫăằắặẳẵ]', 'a', s)
        s = re.sub(u'[ÀÁẠẢÃĂẰẮẶẲẴÂẦẤẬẨẪ]', 'A', s)
        s = re.sub(u'[èéẹẻẽêềếệểễ]', 'e', s)
        s = re.sub(u'[ÈÉẸẺẼÊỀẾỆỂỄ]', 'E', s)
        s = re.sub(u'[òóọỏõôồốộổỗơờớợởỡ]', 'o', s)
        s = re.sub(u'[ÒÓỌỎÕÔỒỐỘỔỖƠỜỚỢỞỠ]', 'O', s)
        s = re.sub(u'[ìíịỉĩ]', 'i', s)
        s = re.sub(u'[ÌÍỊỈĨ]', 'I', s)
        s = re.sub(u'[ùúụủũưừứựửữ]', 'u', s)
        s = re.sub(u'[ƯỪỨỰỬỮÙÚỤỦŨ]', 'U', s)
        s = re.sub(u'[ỳýỵỷỹ]', 'y', s)
        s = re.sub(u'[ỲÝỴỶỸ]', 'Y', s)
        s = re.sub(u'[Đ]', 'D', s)
        s = re.sub(u'[đ]', 'd', s)
        return s
	
def tracebackLoc(locations):
	# compare found words with real districts and provinces
	realLoc = []
	byDistricts = []
	byProvinces = []

	i = 0
	while i < len(locations):
		words = locations[i]
		byDistricts, byProvinces = compareWithDb(words, byDistricts, byProvinces)
		i += 1

	byDistricts = [loc for loc in byDistricts if loc]
	byProvinces = [loc for loc in byProvinces if loc]

	for loc in byDistricts:	
		if loc in byProvinces:
			if loc[0] == loc[1]:
				continue
			realLoc.append(loc)
		else:
			continue

	if not [loc for loc in realLoc if loc]:
		return byProvinces

	return realLoc

def compareWithDb(words, districts, provinces):
	tempDists = Location.query.filter_by(district=words).all()
	tempProvs = Location.query.filter_by(province=words).all()

	districts.extend([(dist.district, dist.province) for dist in tempDists if (dist.district, dist.province) not in districts])
	provinces.extend([(prov.district, prov.province) for prov in tempProvs if (prov.district, prov.province) not in provinces])

	return districts, provinces




	
	


