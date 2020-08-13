


chrome_path = (r"C:\Users\lenovo\Desktop\projects\ScrapyProject\ScrapyProject\wattpad\wattpad\chromedriver_win32\chromedriver.exe")

url = "https://www.wattpad.com/login"


import scrapy
from scrapy.crawler import CrawlerProcess

from selenium import webdriver
import time
import getpass
import datetime


########################## With the help of selenium, we are reaching the page that we wanted to scrape.
########################## This bot works with google chrome.


options = webdriver.ChromeOptions()
options.headless = False

driver = webdriver.Chrome(options = options, executable_path = chrome_path)

driver.get(url)
print(driver.page_source)


time.sleep(5)

button1 = driver.find_element_by_xpath('//*[@id="authentication-panel"]/div/button')
button1.click()


time.sleep(5)


username = driver.find_element_by_xpath('//*[@id="login-username"]')
my_email = input('Please provide your email:')
username.send_keys(my_email)

time.sleep(5)


password = driver.find_element_by_xpath('//*[@id="login-password"]')
my_pass = getpass.getpass('Please provide your password:')
password.send_keys(my_pass)

time.sleep(5)


button2 = driver.find_element_by_xpath('/html/body/div[3]/div/div[3]/div/div[2]/main/div/div/div/div/form/input')
button2.click()


time.sleep(5)
print(driver.page_source)


###### Rarely information screens pop up in the website and
###### this try-expect method in here for prevent any delay or out of aim operation.



try:
    content_notification = driver.find_element_by_xpath('/html/body/div[4]/div/div/div/div[1]/div/h2/div[1]/a')
    content_notification.click()
except:
    pass

time.sleep(2)

Browse = driver.find_element_by_xpath('/html/body/div[2]/div/nav[1]/ul/li[2]/a')
Browse.click()

time.sleep(2)

adventure = driver.find_element_by_xpath('/html/body/div[2]/div/nav[1]/ul/li[2]/div[2]/div[1]/ul/li[5]/a')
adventure.click()



import scrapy
from scrapy.crawler import CrawlerProcess
# from ..items import WattpadItem

class Link(scrapy.Item):
    link = scrapy.Field()
    name = scrapy.Field()
    author = scrapy.Field()
    readcount = scrapy.Field()
    votecount = scrapy.Field()
    partnumber = scrapy.Field()


## The name of spider Adventure however the spider scrape the secent element of browse section which means it can be changeable by language.

class Adventure(scrapy.Spider):
    name = 'wattpad'
    # allowed_domains = ['https://www.wattpad.com/']
    start_urls = [
        'https://www.wattpad.com/stories/adventure'
    ]

    def parse(self, response):
        xpath = '//a[re:test(@class, "on-navigate on-topic")]//@href'
        selection = response.xpath(xpath)
        for s in selection:
            l = Link()
            l['link'] = 'https://www.wattpad.com/' + s.get()
            yield scrapy.Request(l['link'], callback=self.parse_pages)

    def parse_pages(self, response):
        xpath = '//a[re:test(@class, "title meta on-story-preview")]//@href'
        pages = response.xpath(xpath)
        for p in pages:
            l = Link()
            l['link'] = 'https://www.wattpad.com/' + p.get()
            yield scrapy.Request(l['link'], callback=self.parse_attr)

    def parse_attr(self, response):
        item = Link()
        item["link"] = response.url
        item["name"] = "".join(response.xpath('//*/div[re:test(@class, "container")]//h1/text()').extract_first()).strip()
        item["author"] = "".join(response.xpath('//*/a[re:test(@class, "send-author-event on-navigate")]/text()')[2].extract())
        item["readcount"] = "".join(response.xpath('//*/div[re:test(@class, "meta")]//span/text()').extract_first()).strip()
        item["votecount"] = "".join(response.xpath('//*/div[re:test(@class, "meta")]//span/text()')[1].extract()).strip()
        item["partnumber"] = "".join(response.xpath('//*/div[re:test(@class, "meta")]//span/text()')[2].extract())
        return item



#dc_dict = dict()
#process = CrawlerProcess()
#process.crawl(Adventure)as
# process.start(stop_after_crawl=False)

#dc_dict[ crs_title_ext ] = ch_titles_ext