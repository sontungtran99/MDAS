import requests
import time
import subprocess
from data.User import User, db


url = 'https://api.speedsms.vn/index.php/sms/send'
access_token = 'XXX' # SpeedSMS API token


def getNumbersInLocations(locations):
	''' Returns a list of numbers '''
	nums = []
	for loc in locations:
		victims = User.query.filter_by(district=loc[0], province=loc[1]).all()
		nums.extend([victim.phonenum for victim in victims])
	return nums

def sendToLocations(locations, message):
	''' Returns a list of responses '''

	numbers = getNumbersInLocations(locations)
	length = len(numbers)
	count = 0
	responses = []
	while length > 180:
		# Slice list into lists of numbers contains at most 180 nums
		responses.append(sendToNumbers(numbers[count:count+180]))
		count += 180
	
	responses.append(sendToNumbers(numbers[count:len(numbers)]))
	return response

def sendToNumbers(numbers):	
	phonenumsStr = ','.join(numbers)	
	content = message
	sender = ''
	data = {
		'to': phonenums,
		'content': content,
		'sender': brandname,
		'sms_type': sms_type,
	}

	getRequest = url + '?access-token={}&to={}&content={}'.\
						format(access_token, phonenumsStr, content)
	r = requests.get(getRequest)

	return r.text

def currentTime():
	currentTimeStruct = time.localtime(time.time())
	year = currentTimeStruct.tm_year
	month = currentTimeStruct.tm_mon
	day = currentTimeStruct.tm_mday
	hour = currentTimeStruct.tm_hour
	minute = currentTimeStruct.tm_min + 1
	return '{}-{}-{} {}:{}'.format(day, month, year, hour, minute)

