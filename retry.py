#!/usr/bin/env python3

import requests
import time
import json
from requests.adapters import HTTPAdapter
from requests.packages.urllib3.util.retry import Retry
from pathlib import Path
import yagmail
from datetime import datetime

while True:

	try:
		retries = Retry(total=1, backoff_factor=10, status_forcelist=[429, 500, 502, 503, 504])
		http = requests.Session()
		http.mount("http://", HTTPAdapter(max_retries=retries))
		response = http.get("http://192.168.1.148")
		# print(response)

	except:
		yag = yagmail.SMTP(user='pchapin71@gmail.com', password='temppass#1')
		yag.send(to='deuthling@gmail.com', subject='IotaNOT', contents = 'The IotaWatt webserver is not responding. Monitoring program has closed.')
		break

	else:
		file = Path("size.txt")
		size = (file.read_text())
		if size == "stop":
			break

		outputs = requests.get("http://192.168.1.148/status?outputs=yes")
		power = json.loads(outputs.text)
		crab = float(((power['outputs'][0]['value'])))
		prawn = float(((power['outputs'][1]['value'])))

		def notification(message,message2,size):
			report = {}
			report["value1"] = message
			report["value2"] = message2
			report["value3"] = size
			requests.post("https://maker.ifttt.com/trigger/amps1/with/key/bE0GzE8o6ggBv5fvnDWCD9", data=report)
			# yag = yagmail.SMTP(user='pchapin71@gmail.com', password='temppass#1')
			# yag.send(to='deuthling@gmail.com', subject='Amp Alert', contents = f'Crab: {message} Prawn: {message2} Size: {size}')

		if ((crab > 27 or prawn > 27) and size == "small") or ((crab > 70 or prawn > 70) and size == "medium") or ((crab > 150 or prawn > 150) and size == "big"):
			notification(prawn, crab, size)
			print("prawn=", prawn)
			print("crab=", crab)
			print(size)
			print(datetime.now().time())


	time.sleep(10)