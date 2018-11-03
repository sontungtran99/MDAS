from sendToLocations import sendToLocations
from getNgrokUrl import getNgrokUrl
from getInfo import getInfo
from changeWebhookUrl import changeWebhookUrl
import time


previousWarningUrl = input()
start = time.time()
ngrokUrl = ''
# Check for new warnings, ngrok url for each time looping through
while True:
	try:
		message, locations = getInfo(previousWarningUrl)
	except IndexError:
		time.sleep(10)
		continue

	if message != '':
		responses = sendToLocations(locations, message)
		for response in responses:
			if response['status'] == 'success':
				print(response)
			else:
				continue
	else:
		pass

	url = getNgrokUrl()
	print(url)
	if url != ngrokUrl:
		ngrokUrl = url
		changeWebhookUrl(url + '/response')

	time.sleep(10)
