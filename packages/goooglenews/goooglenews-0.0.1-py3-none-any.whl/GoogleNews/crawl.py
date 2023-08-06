# -*- coding:utf-8 -*-

import requests
from bs4 import BeautifulSoup
import time
import random
import pandas as pd


class GoogleNews():

    def __init__(self):
        self.url = 'https://news.google.com'
        self.base = 'https://news.google.com/search?q={:s}&hl=en-US&gl=US&ceid=US%3Aen'
        # self.search_url = 'https://news.google.com/search?q={:s}&hl=en-US&gl=US&ceid=US%3Aen'
        self.proxy={'https':'127.0.0.1:1080'}
        self.keyword=None
        self.df_search=None
        self.df_detail=None


    # 发送Get请求
    def requests_get(self, url):
        response = None
        try:
            print(url)
            # time.sleep(random.random() * 0.5 + 0.1)  # 暂停随机数
            response=requests.get(url, proxies=self.proxy)
        except Exception as e:
            print(e)
        finally:
            return response.text

    # 搜索新闻
    def search_news(self, keyword):
        self.keyword=keyword
        search_url = self.base.format(keyword.replace(' ','%20'))
        result=None
        try:
            self.df_search = pd.DataFrame(columns=["title", "url", "summary", "source", "stamp"])
            response = self.requests_get(search_url)
            # print(response)
            soup = BeautifulSoup(response, "html.parser")
            NiLAwe = soup.find_all('div', class_='NiLAwe y6IFtc R7GTQ keNKEd j7vNaf nID9nc', jslog='93789')
            # print(NiLAwe.__len__())
            for item in NiLAwe:
                ipQwMb = item.find('h3', class_='ipQwMb ekueJc RD0gLb')
                news_title=ipQwMb.a.text.strip()
                news_url = self.url+ipQwMb.a['href'][1:]
                jVqMGc = item.find('div', class_='Da10Tb Rai5ob', jsname='jVqMGc')
                news_summary=jVqMGc.span.text.strip()
                SVJrMe = item.find('div', class_='SVJrMe', jsname='Hn1wIf')
                news_source=SVJrMe.a.text.strip()
                try:
                    news_stamp = SVJrMe.time['datetime']
                except:
                    news_stamp = ""

                row=[news_title, news_url, news_summary, news_source, news_stamp]
                self.df_search.loc[len(self.df_search)]=row
                # print(row)
            result=self.df_search

        except Exception as e:
            print(e)
        finally:
            return result

    # 想看详情
    def news_detail(self):
        result=None
        try:
            self.df_detail = pd.DataFrame(columns=["title", "url", "summary", "source", "stamp", "html", "text"])
            for index, row in self.df_search.iterrows():
                response = self.requests_get(row['url'])
                soup = BeautifulSoup(response, "html.parser")
                gettext = soup.get_text().strip()
                row['html']=response
                row['text']=gettext

                self.df_detail.loc[len(self.df_detail)]=row
            result = self.df_detail

        except Exception as e:
            print(e)
        finally:
            return result

    # 保存
    def news_save(self):
        if self.df_detail is not None:
            self.df_detail.to_csv('detail_{:s}.csv'.format(self.keyword), encoding='utf_8_sig')
            self.df_detail.to_excel('detail_{:s}.xlsx'.format(self.keyword))
            return
        if self.df_search is not None:
            self.df_search.to_csv('search_{:s}.csv'.format(self.keyword), encoding='utf_8_sig')
            self.df_search.to_excel('search_{:s}.xlsx'.format(self.keyword))


    # 获取网页文本
    def html_text(self, url):
        result=None
        try:
            response = self.requests_get(url)
            soup = BeautifulSoup(response, "html.parser")
            result=soup.get_text()
        except Exception as e:
            print(e)
        finally:
            return result

    def print_df(self, df):
        for index, row in df.iterrows():
            print(index)
            print(row)


    def start(self):

        df_search=self.search_news('Didi financial crisis')
        print(df_search)

        df_detail=self.news_detail()
        print(df_detail)

        self.news_save()


if __name__ == '__main__':

    ac=GoogleNews()
    ac.start()


