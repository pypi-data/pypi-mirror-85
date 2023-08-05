#coding=utf-8

# 免责声明：此程序仅作为学习交流使用，禁止作为商业用途, 禁止作为违法犯罪用途。


loginParam={

    'query': {
        'q': 'csdn',
    },
}

loginUrls =  {
    'proxyWeb': 'https://www.xicidaili.com/nn/',
    'proxyJson': 'https://ip.jiangxianli.com/api/proxy_ip',
    'proxies': {
        "http": 'http://127.0.0.1:1080',
        # "https": 'https://127.0.0.1:1080'
    },
    'url':'http://www.hibor.com.cn/data/0ce2ab43c688a2546b1cbaa9c8813f4a.html',
    'hibor': 'http://www.hibor.com.cn',


}
loginHeaders = {

    "hibor": {
        "Host": "www.hibor.com.cn",
        "Connection": "keep-alive",
        # "Content-Length": "0",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36",
        # "X-Requested-With": "XMLHttpRequest",
        # "Origin": "http://www.gsdata.cn",
        "Referer": "http://www.hibor.com.cn",
        "Accept-Encoding": "gzip, deflate",
        "Accept-Language": "zh-CN,zh;q=0.9",
        "Cache-Control": "max-age=0",
        "Upgrade-Insecure-Requests": "1",
        "Cookie": "",
    },

    'proxy':
    '''
Host: ip.jiangxianli.com
Connection: keep-alive
Cache-Control: max-age=0
Upgrade-Insecure-Requests: 1
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36
Accept: text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9
Sec-Fetch-Site: none
Sec-Fetch-Mode: navigate
Sec-Fetch-User: ?1
Sec-Fetch-Dest: document
Accept-Encoding: gzip, deflate, br
Accept-Language: zh-CN,zh;q=0.9


'''

}

loginCookie=''

