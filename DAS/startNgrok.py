import subprocess
import time
from getNgrokUrl import getNgrokUrl
from urllib.error import URLError


url = ''
while True:
	''' Keep Ngrok running at all time '''
	
	# If ngrok not available, start ngrok
	try:
		url = getNgrokUrl()
		time.sleep(10)
		continue
	except URLError:
		pass

	t = subprocess.Popen(['/home/tung/ngrok', 'http', '5000'], stdout=subprocess.PIPE)
	print('Ngrok started')
	time.sleep(10)
	