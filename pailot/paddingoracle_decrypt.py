import requests

# session = requests.Session()
# burp0_url = "http://128.199.157.172:20678/validate"
# burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded", "Origin": "http://128.199.157.172:20678", "Connection": "close", "Referer": "http://128.199.157.172:20678/", "Upgrade-Insecure-Requests": "1"}
# burp0_data = {"username": "", "password": "", "submit": "submit"}
# resp = session.post(burp0_url, headers=burp0_headers, data=burp0_data)

# password = session.cookies['session_password'].decode('base64').replace('iv: ', '').split(', enc(input_password+valid_password): ')
# username = session.cookies['session_username'].decode('base64').replace('iv: ', '').split(', enc(input_username+valid_username): ')


# username_iv = username[0]
# username_enc = username[1]

username_iv = '\xa3d\x94<\xbe1\xcb~>1\x85p\x81Mo\xe1'
username_enc = 'A\x90\xec\xc0\xe9\xd1\xef\x12\x89\xdeN\x1c\x91/F\xcc'

# password_iv = password[0]
# password_enc = password[1]

password_iv = '\xbc\xac\xf80\xa7__\xe2h\xb2_p-{\xe7\xbe'
password_enc = '\x1f+\x9c\x8d\xef\x95\x1aa<:d\x8c@\xd9\x9b`\xaf\xeb\x08\x99\xffK\xa4\xb8\x85Z\t"\xee\x01\xc3d\xc4\x87\x91<\xe0\xfd\xcf\xb9\xacM\xc2\r|^\xf6\xe7'

print repr(username_iv)
print repr(username_enc)
print len(username_enc)
print repr(password_iv)
print repr(password_enc)
print len(password_enc)

# exit()

# len username = 3
# len password = 40

def create_cookie(username_iv, username_enc, password_iv, password_enc):
    return {
        'session_username': 'iv: {}, enc(input_username+valid_username): {}'.format(username_iv, username_enc).encode('base64').replace('\n',''),
        'session_password': 'iv: {}, enc(input_password+valid_password): {}'.format(password_iv, password_enc).encode('base64').replace('\n',''),
    }

# ct = username_enc
# ct = [ct[i:i+16] for i in range(0, len(ct), 16)]

ct = password_iv+password_enc
ct = [ct[i:i+16] for i in range(0, len(ct), 16)]

original_block = []
for c in ct:
    original_block.append(c)

pt = ''
for n_block in range(len(original_block)-2,-1,-1):
    zero_byte = 15
    pad_str = ord('\x01')
    inter_state = []
    pad_bytes = ''
    for i in range(16):
        print 'Guessing [{}] bytes...'.format(15-i)
        for j in range(0, 256):
            guess_c2 = ('\x00'*zero_byte + chr(j) + pad_bytes)
            payload = guess_c2 + ct[-1]

            cookies = create_cookie(username_iv, username_enc, password_iv, payload)
            # print cookies

            burp0_url = "http://128.199.157.172:20678/"
            burp0_headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:79.0) Gecko/20100101 Firefox/79.0", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8", "Accept-Language": "en-US,en;q=0.5", "Accept-Encoding": "gzip, deflate", "Content-Type": "application/x-www-form-urlencoded", "Origin": "http://128.199.157.172:20678", "Connection": "close", "Referer": "http://128.199.157.172:20678/", "Upgrade-Insecure-Requests": "1"}
            resp = requests.get(burp0_url, headers=burp0_headers, cookies=cookies)

            if 'Your password is wrong!' in resp.text:
                temp = chr(pad_str ^ ord(original_block[n_block][zero_byte]) ^ j)
                inter_state.append(temp)

                print 'Found plaintext :', repr(temp)

                pt = temp + pt
                pad_bytes = ''
                for k in range(i+1):
                    pad_bytes += chr((pad_str+1) ^ ord(original_block[n_block][15-k]) ^ ord(inter_state[k]))
                pad_bytes = pad_bytes[::-1]
                break
            elif 'Your password is not properly padded!' in resp.text: 
                print 'incorrect pad'
                # print resp.text
            else:
                print resp.text
                exit()


        pad_str += 1
        zero_byte -= 1
        print 'PLAINTEXT so far', repr(pt)

    print 'Moving to the prev block..'
    del ct[-1]

print 'Decrypted:', repr(pt)
