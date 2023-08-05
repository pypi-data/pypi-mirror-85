#coding=utf-8


# 免责声明：此程序仅作为学习交流使用，禁止作为商业用途, 禁止作为违法犯罪用途。

import re
import os
import random
from HiborCrawl import info
import json
import time
import requests
from bs4 import BeautifulSoup
from urllib import parse
from datetime import datetime
import csv
from pymongo import MongoClient
import urllib3
import numpy as np




rootPath=r'./'


class Hibor():
    def __init__(self):
        self.urls = {}
        self.headers = {}
        self.param = {}
        self.cachePool={}
        self.stamp = datetime.now().strftime('%Y-%m-%d')
        self.client = MongoClient("localhost", 27017)
        self.db=self.client['hibor']
        self.cookie=requests.cookies.RequestsCookieJar()
        self.session = requests.session()

    # 从配置文件中更新登录链接信息
    def update_info(self):
        self.urls = info.loginUrls
        self.headers = info.loginHeaders
        self.param = info.loginParam
        self.cookie.set("cookie", info.loginCookie)
        self.session.cookies.update(self.cookie)

    # 发送Get请求
    def requests_get(self, url, data=None, headers=None):
        try:
            url = url if data is None else url+parse.urlencode(data)
            time.sleep(random.random() * 1 + 0.1)  # 0-1区间随机数
            #没有缓存就开始抓取
            # print(self.urls['proxies']['http'] + ' --> ' + url)
            response = requests.get(url, headers=headers, verify=False)
            # response = self.session.get(url, headers=headers, verify=False, proxies=self.urls['proxies'])
            # self.session.keep_alive = False
            response.encoding = 'utf-8'
            value = response if response.status_code == requests.codes.ok else None
        except Exception as e:
            value = None
        finally:
            return value


    # 发送Post请求
    def requests_post(self, url, data=None, headers=None):
        try:
            url = url if data is None else url+parse.urlencode(data)
            time.sleep(random.random() * 1 + 0.1)  # 0-1区间随机数
            #没有缓存就开始抓取
            # print(self.urls['proxies']['https'] + ' --> ' + url)
            # response = requests.post(url, data=data,  headers=headers, verify=False)
            response = self.session.post(url, data=data, headers=headers, verify=False)
            # self.session.keep_alive = False
            response.encoding = 'utf-8'
            value = response if response.status_code == requests.codes.ok else None
        except Exception as e:
            value = None
        finally:
            return value


    # 保存
    def write_file(self, path, page):
        f=open(path, 'a')
        f.write(page.encode('utf-8').decode('utf-8'))
        f.write("\n")
        f.close()

    # 从文件读出字典数据
    def open_wx(self, path):
        if not os.path.exists(path):
            return False
        with open(path,'r') as load_f:
            parm_dict = json.load(load_f)
            load_f.close()
        return parm_dict
    # 字典数据写入文件
    def save_wx(self, path, parm_dict):
        with open(path,'w') as dump_f:
            json.dump(parm_dict, dump_f)
            dump_f.close()

    # 字符串转换成datetime
    def strptime(self, str):
        return datetime.strptime(str, '%Y-%m-%d')
    # datetime转换为字符串
    def strftime(self, time):
        return time.strftime('%Y%m%d')

    def headers_eval(self, headers):
        """
        headers 转换为字典
        :param headers: 要转换的 headers
        :return: 转换成为字典的 headers
        """
        try:
            headers = headers.splitlines()  # 将每行独立为一个字符串
            headers = [item.strip() for item in headers if item.strip() and ":" in item]  # 去掉多余的信息 , 比如空行 , 非请求头内容
            headers = [item.split(':') for item in headers]  # 将 key value 分离
            headers = [[item.strip() for item in items] for items in headers]  # 去掉两边的空格
            headers = {items[0]: items[1] for items in headers}  # 粘合为字典
            headers = json.dumps(headers, indent=4, ensure_ascii=False)  # 将这个字典转换为 json 格式 , 主要是输出整齐一点
        except Exception:
            print("headers eval get error ...")
            headers = dict()

        return headers

    # 获取代理ip
    def get_iplist(self,url):
        response=requests.get(url)
        msg=response.json()['data']
        msg_ip=msg['protocol']+'://'+msg['ip']+':'+msg['port']
        return msg_ip
    # 切换ip代理
    def switchProxy(self):
        proxy_ip=self.get_iplist(self.urls['proxyJson'])
        self.urls['proxies']['http']=proxy_ip

    def getStamp(self):
        return self.utc2local(self.local2utc(datetime.now())).strftime('%Y%m%d')



    # 获取公众号文章正文
    def article_query(self, url):
        result=[None]
        response = self.requests_get(url, headers=self.headers['hibor'])
        # print(response.text)
        soup=BeautifulSoup(response.text, "lxml")
        try:
            abstruct_info = soup.find('div', class_='abstruct-info')
            content=abstruct_info.text.strip()

            doc_info = soup.find('div', class_='doc-info')
            spans=doc_info.find_all('span')
            article_time=spans[0].text.strip()
            article_source=spans[1].text.strip()

            doc_info = soup.find('div', class_='doc-info-list')
            spans=doc_info.find_all('span')
            lable=spans[0].a.text.strip()
            author=spans[1].a.text.strip()
            fenlei = spans[2].text.strip()
            page_num = spans[3].text.strip()
            page_size = spans[4].text.strip()
            sharer = spans[5].text.strip()

            result=[content, article_time, article_source, lable, author, fenlei, page_num, page_size, sharer]
        except:
            pass
        finally:
            return result


    def csv_export(self, path):
        self._records = self.db['hibor_records']

        self.csvfile = open(path + '/hibor_' + self.stamp + '.csv', 'w', encoding='utf-8-sig', newline='')
        self.csvwriter = csv.writer(self.csvfile)
        titleFlag = True

        recordObj = self._records.find()
        for record in recordObj:

            self._matches = self.db[record['name']]
            matchObj = self._matches.find({'posttime': self.stamp})
            for match in matchObj:
                if titleFlag:
                    self.csvwriter.writerow(match.keys())
                    titleFlag=False
                self.csvwriter.writerow(match.values())

        self.csvfile.close()


    # 读取配置文件，逐一爬取
    def hibor_crawl(self):
        # 同步配置参数
        self.update_info()
        self._records = self.db['hibor_records']

        response = self.requests_get('http://www.hibor.com.cn/')
        soup = BeautifulSoup(response.text, "lxml")

        list_nav = soup.find('li', attrs={'class': 'list_nav'})
        list_ul = list_nav.find_all('a', attrs={'target': '_blank'})
        for target in list_ul:
            fenlei = target.text
            target_url = 'http://www.hibor.com.cn' + target['href']
            print(fenlei + '    --等待更新')

            if fenlei in ['外文报告', '公司公告', '定期财报']:
                continue
            # if fenlei not in ['宏观经济']:
            #     continue

            record = self._records.find_one({'symbol': target.text})
            flag = (record is None)
            if flag:
                record = {}
                record['symbol'] = fenlei
                record['name'] = fenlei
                record['url'] = target_url

            if flag:
                self._records.insert_one(record)
            else:
                # self._matches.update_one({'symbol': match['symbol']}, {"$set": match}, True)
                pass

            self._matches = self.db[fenlei]

            response = self.requests_get(target_url, headers=self.headers['hibor'])
            soup = BeautifulSoup(response.text, "lxml")

            main_div = soup.find('table', attrs={'id': 'tableList'})

            child_list = [x for x in main_div.children]
            np_chile = np.array(child_list, dtype=object)
            np_list1 = np_chile[1:np_chile.size:2]
            np_list2 = np_list1.reshape(np_list1.size // 4, 4)

            for item in np_list2:
                item0 = item[0]
                title = item0.text.strip()
                item1 = item[1]
                summary = item1.text.strip()
                arc_url = self.urls['hibor'] + item1.td.a['href']
                item2 = item[2]
                posttime = item2.td.span.text.strip()
                spans = item2.find_all('span')
                sharer = spans[1].text.strip()
                author = spans[2].text.strip()
                pingji = spans[3].text.strip()
                page_num = spans[4].text.strip()

                # row = [title, summary, arc_url, posttime, share, author, lable, page_num]
                # print(row)

                # 更新数据库
                match = self._matches.find_one({'symbol': arc_url})  # 代码
                flag = (match is None)
                if flag:
                    self.headers['hibor']['Referer'] = target_url
                    article = ''

                    # res_arc = self.article_query(arc_url)
                    # article = res_arc[0]
                    # article_time = res_arc[1]
                    # article_source = res_arc[2]
                    # fenlei = res_arc[5]
                    # page_size = res_arc[-2]
                    # sharer = res_arc[-1]

                    match = {}
                    match['symbol'] = arc_url
                    match['lable'] = fenlei
                    match['title'] = title
                    match['summary'] = summary
                    match['arc_url'] = arc_url
                    match['posttime'] = posttime
                    match['sharer'] = sharer
                    match['author'] = author
                    match['pingji'] = pingji
                    match['page_num'] = page_num
                    match['article'] = article
                    match['keywords'] = ''
                    match['star'] = ''

                if flag:
                    self._matches.insert_one(match)
                    try:
                        linew = '   '.join([posttime, author, title])
                        print(linew)
                    except:
                        pass
                else:
                    # self._matches.update_one({'symbol': match['symbol']}, {"$set": match}, True)
                    pass



# 主程序入口
if __name__ == '__main__':
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

    spider = Hibor()
    spider.hibor_crawl()
    spider.csv_export(spider.stamp)




