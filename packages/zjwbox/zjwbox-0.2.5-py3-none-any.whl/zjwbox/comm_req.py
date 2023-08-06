import requests
import parsel, re, json, jsonpath
import time, random
import asyncio, aiohttp
from tqdm import tqdm
from itertools import product
import eventlet
from faker import Faker
from datetime import datetime


"""
This is a person to solve common spider in website.
You may transmit some args to it.
Least need a arg(url or urls), 
of couser, you also can change many args, headers cookie, data, mode, etc.
Matters need attention: urls should be a string or list. 
"""


fake = Faker()
fake_ua = fake.user_agent()

class Comm_req(object):

    def __init__(self, urls: str or list, headers: dict={"UserAgent": fake_ua}, cookie: dict=None, data: dict=None, 
                        encode: str="utf-8", mode: str="get", time_inter: bool=False):
        self.urls = urls
        self.headers = headers
        self.cookie = cookie
        self.data = data
        self.mode = mode
        self.encode = encode
        self.time_inter = time_inter


    async def fask(self, url, mode="get") -> str:
        async with aiohttp.ClientSession() as session:
            if self.mode == "post":
                async with session.post(url, headers=self.headers, timeout=3) as res:
                    return await res.text()
            else:
                async with session.get(url, headers=self.headers, timeout=3) as res:
                    return await res.text()


    def comm_deal(self, expr_element: list or tuple or str, is_json: bool=False) -> str:
        if isinstance(self.urls, str):
            session = requests.Session()
            if self.time_inter:
                self.time_inter = random.choice([0.5, 1, 0.9, 1.5])
                res = session.get(self.urls, headers=self.headers, timeout=5)
                text = res.content.decode(self.encode)
                if self.mode == "post":
                    res = session.post(self.urls, self.headers)
                    text = res.content.decode(self.encode)
                time.sleep(self.time_inter)
                if is_json:
                    json_text = jsonpath.jsonpath(json.loads(text), f"$..{expr_element}")
                    yield json_text
                else:
                    yield text

            else:
                res = session.get(self.urls, headers=self.headers, timeout=5)
                text = res.content.decode(self.encode)
                if self.mode == "post":
                    res = session.post(self.urls, self.headers)
                    text = res.content.decode(self.encode)
                yield text

        else:
            for url in self.urls:
                loop = asyncio.get_event_loop()
                text = loop.run_until_complete( self.fask(url, self.mode) )
                now_time = datetime.now()
                print(f"爬取{url}成功！时间：{now_time}")
                yield text


    def get_page(self, expr_element: list or tuple or str, is_json: bool=False):
        result = []
        for page in self.comm_deal(expr_element, is_json=is_json):
            result.append(page)
        if result == []:
            return None
        eventlet.monkey_patch()
        now_time = datetime.now()
        if isinstance(self.urls, str):
            print(f"目标1个，成功爬取{len(result)}, 时间：{now_time}")
        else:
            print(f"目标{len(self.urls)}个，成功爬取{len(result)}，时间：{now_time}")
  
        return result
        
           




