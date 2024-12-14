import sys

import requests
import re
import argparse

RED = '\033[1;31m'
GREEN = '\033[1;32m'
DEFAULT = '\033[0m'


def login(userID, password, logintype, verbose=False):
    print(f'[{GREEN}+{DEFAULT}] Getting login url...')
    pkt = requests.get('http://www.baidu.com')
    ctt = pkt.content.decode()
    cookie = pkt.cookies
    url: str = re.findall("'(.*?)'", ctt)[0]
    if verbose:
        print(f'[{GREEN}+{DEFAULT}] Login url:', url)

    headers = {
        'Host': '211.87.158.84',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:95.0) Gecko/20100101 Firefox/95.0',
        'Accept': '*/*',
        'Accept-Language': 'zh-CN,zh;q=0.8,zh-TW;q=0.7,zh-HK;q=0.5,en-US;q=0.3,en;q=0.2',
        'Accept-Encoding': 'gzip, deflate',
        'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
        # 'Origin': 'http://211.87.158.84',
        'Origin': url[:url.find('/', 8)],
        'DNT': "1",
        'Connection': 'keep-alive',
        # 'Referer': 'http://211.87.158.84/eportal/index.jsp?wlanuserip=ce9bde2df665435edb85b1ffec327dc9&wlanacname=5538726b55215fab4241428c6bbf825d&ssid=&nasip=5ab529d50e00cdf64d40f63e5fd64af4&snmpagentip=&mac=5cdb13749f31415e6ef58e6c62785fb5&t=wireless-v2&url=c9673a58c390d25657e4c05c95a65e9b8df200c7c10b0463&apmac=&nasid=5538726b55215fab4241428c6bbf825d&vid=b403702dc8373411&port=1b83d6e46fd782a6&nasportid=5b9da5b08a53a5406447aa0a41d196f53fb18036c9f86b997d402f4cd6615939',
        'Referer': url,
        'Sec-GPC': '1',
        'Pragma': 'no-cache',
        'Cache-Control': 'no-cache',
    }
    print(f'[{GREEN}+{DEFAULT}] Setting headers...')
    if verbose:
        print(f'[{GREEN}+{DEFAULT}] Headers:', headers)

    data = {
        'userId': userID,
        'password': password,
        'service': logintype,  # local | internet
        'queryString': url[url.find('?') + 1:],
        'operatorPwd': '',
        'operatorUserId': '',
        'validcode': '',
        'passwordEncrypt': 'false'
    }
    print(f'[{GREEN}+{DEFAULT}] Setting data...')
    if verbose:
        print(f'[{GREEN}+{DEFAULT}] Data:', data)
    loginurl = url[:url.find('/', 8)] + "/eportal/InterFace.do?method=login"
    if verbose:
        print(f'[{GREEN}+{DEFAULT}] Sending login request to {RED}{loginurl}{DEFAULT}...')
    r = requests.post(loginurl, data=data, headers=headers, cookies=cookie)

    if r.ok:
        print(f'[{GREEN}+{DEFAULT}] Login success!')
        if verbose:
            print(r.text)
    else:
        print(f'[{RED}-{DEFAULT}] Login failed!')
        print(r.text)


def logout(verbose=False, url="http://211.87.158.84"):
    query_url = url + "/eportal/InterFace.do?method=getOnlineUserInfo"
    print(f'[{GREEN}+{DEFAULT}] Getting user index')

    headers = {
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'Accept-Encoding': 'gzip, deflate',
        'Accept-Language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'Connection': 'keep-alive',
        'Host': '211.87.158.84',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36 Edg/96.0.1054.62',
    }
    if verbose:
        print(f'[{GREEN}+{DEFAULT}] Query url:', query_url)
        print(f'[{GREEN}+{DEFAULT}] Headers:', headers)

    pkt = requests.get(query_url, headers=headers)
    if verbose:
        print(f'[{GREEN}+{DEFAULT}] Sending request to {RED}{url}{DEFAULT}...')
    res = pkt.json()
    if verbose:
        print(f'[{GREEN}+{DEFAULT}] Response:', res)

    userIndex = res['userIndex']
    if verbose:
        print(f'[{GREEN}+{DEFAULT}] User index:', userIndex)
    if not userIndex:
        print(f'{RED}Error: User Index is null.{DEFAULT}')
        return
    print(f'[{GREEN}+{DEFAULT}] Logout...')
    action_url = url + "/eportal/InterFace.do?method=logout"
    data = {
        'userIndex': userIndex,
    }
    if verbose:
        print(f'[{GREEN}+{DEFAULT}] Action url:', action_url)
        print(f'[{GREEN}+{DEFAULT}] Data:', data)
        print(f'[{GREEN}+{DEFAULT}] Sending logout request to {RED}{action_url}{DEFAULT}...')
    r = requests.post(action_url, data=data, headers=headers)
    if verbose:
        print(f'[{GREEN}+{DEFAULT}] Response:', r.text)
    if r.ok:
        print(f'[{GREEN}+{DEFAULT}] Logout success!')
        if verbose:
            print(r.content.decode("gbk", "ignore"))
    else:
        print(f'[{RED}-{DEFAULT}] Logout failed!')
        if verbose:
            print(r.content.decode("gbk", "ignore"))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Headless QUST Campus Web Service Client')
    parser.add_argument('-o', '--logout', action='store_true', help='Logout from Campus Web Service instead of login')
    parser.add_argument('--local', action='store_true', help='use local Ethernet instead of Internet')

    parser.add_argument('--url', help='Use customised url instead of default(http://211.87.158.84)',
                        required=False, default='http://211.87.158.84')

    parser.add_argument('-u', '--userid', help='User ID')
    parser.add_argument('-p', '--password', help='Password')
    parser.add_argument('-v', '--verbose', action='store_true', help='Verbose mode')

    args = parser.parse_args()

    if len(sys.argv) == 1:
        parser.print_help()
        sys.exit(1)

    if args.logout:
        logout(url=args.url, verbose=args.verbose)
    else:
        if not args.userid or not args.password:
            print(f"{RED} Error: User ID and Password are required while login. {DEFAULT}")
        else:
            login(args.userid, args.password, 'local' if args.local else 'internet', verbose=args.verbose)
