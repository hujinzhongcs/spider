# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals

# useful for handling different item types with a single interface
from scrapy.http import HtmlResponse
from time import sleep
import re
# from selenium import webdriver




class NewsDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.


        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        # bro = spider.bro#获取了在爬虫类中定义的浏览器对象

        if spider.name == 'baidu':
            bro = spider.bro#获取了在爬虫类中定义的浏览器对象
            if request.url in spider.dynamicUrl_baidu:
                bro.get(request.url)
                sleep(1)
                for n in range(10):
                    bro.execute_script('window.scrollTo(0,document.body.scrollHeight)')
                    sleep(0.2)
                page_text = bro.page_source
                new_response = HtmlResponse(url=request.url,body=page_text,encoding='utf-8',request=request)
                return new_response

            else:
                return response

        if spider.name == 'sina':
            bro = spider.bro#获取了在爬虫类中定义的浏览器对象
            if request.url in spider.dynamicUrl:
                bro.get(request.url)
                bro.refresh()
                sleep(3)
                page_text = bro.page_source
                new_response = HtmlResponse(url=request.url,body=page_text,encoding='utf-8',request=request)
                return new_response
            else:
                return response

        if spider.name == 'chinanews':
            bro = spider.bro#获取了在爬虫类中定义的浏览器对象
            if request.url in spider.dynamicUrl:
                bro.get(request.url)
                bro.refresh()
                sleep(3)
                page_text = bro.page_source
                new_response = HtmlResponse(url=request.url,body=page_text,encoding='utf-8',request=request)
                return new_response
            else:
                return response

        if spider.name=='people':
        # if response.url in spider.dynamicUrl_people:
        #     bro.get(request.url)
        #     bro.find_element_by_name("cat6").click()
            return response

        if spider.name=='wangyi':
            return response

        if spider.name=='cctv':
            return response

        if spider.name=='qq':
            return response

        if spider.name=='xinhuanet':
            return response

        if spider.name=='ifeng':
            bro = spider.bro
            if (re.match(r'https://news.ifeng.com/c/.*',request.url)):
                bro.get(request.url)
                bro.refresh()
                sleep(2)
                page_text = bro.page_source
                new_response = HtmlResponse(url=request.url,body=page_text,encoding='utf-8',request=request)
                return new_response
            else:
                return response


    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass




