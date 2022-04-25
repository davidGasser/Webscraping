import scrapy
from scrapy.loader import ItemLoader
from webtutorial.items import sightItem
import os

from scrapy.selector import Selector
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


basedir = os.path.dirname(os.path.realpath('__file__'))


class sightsSpider(scrapy.Spider):
    
    name = "sights"
    start_urls = ["https://www.tripadvisor.de/Attractions-g187309-Activities-a_allAttractions.true-Munich_Upper_Bavaria_Bavaria.html"]

    def parse(self, response):

        for sight in response.css("div .oQFSuk9j"):                                    #every sight is stored in this sort of container

            loader = ItemLoader(item=sightItem(), selector=sight)                     #initialize Loader with the predefined Item from items.py
            loader.add_css("sight_name","._1zP41Z7X::text")                            #populate item name
            loader.add_css("sight_catagory",".DrjyGw-P._26S7gyB4._3SccQt-T::text")     #populate item catagory
            
            sight_item = loader.load_item()                                            #store item

            sight_url = sight.css("a::attr(href)").get()                            #get the sight's link for more details
            
            if sight_url is not None:
                yield response.follow(sight_url, callback=self.parse_sight, meta={'sight_item': sight_item})    #visit the sight's url and use different parse method
    

    def parse_sight(self, response):
                
        sight_item = response.meta["sight_item"]
        loader = ItemLoader(item=sight_item, response=response)

        if response.css(".ui_header.h1::text") != []:  #dynamic: selenium needed here
            
            #################################
            #setup selenium
            chrome_options = Options()
            chrome_options.add_argument("--window-size=1920x1080")
            #chrome_options.add_argument("--headless")
                
            chrome_driver_path = os.path.join('C:\\Users\\David Gasser\\Documents\\Uni TUM\\Ingenieurspraxis\\scrapy\\webtutorial\\webtutorial\\chromedriver.exe')
            driver = webdriver.Chrome(chrome_options=chrome_options, executable_path=chrome_driver_path)
            ##################################

            print("________________________")
            print(response.request.url)             #useful to keep track of what's beeing scraped 
            print("________________________")
            
            #driver.implicitly_wait(5)                                                  #timer to let the website load = synchronization 
            driver.get(f'{response.request.url}')                                       #get current url
            driver.find_element_by_xpath('//*[@id="_evidon-accept-button"]').click()    #click to accept cookies
            scrapy_selector = Selector(text = driver.page_source)                       #update

            address = scrapy_selector.xpath("//div[@class='LjCWTZdN']/span/text()").re(r'[^.]* Bayern [^.]*')
            duration = scrapy_selector.css("._2y7puPsQ::text").get()

            try:    #if mehr_button does not exist it throws an error and causes strange behaviour 
                mehr_button = driver.find_element_by_xpath("//span[@class='_2d6dbR2A']")    #find mehr_button
                mehr_button.click()                                                         #click it 
                scrapy_selector = Selector(text = driver.page_source)                       #update 
                detail = scrapy_selector.css("._2VvY_ZCJ::text").get()
            except: 
                detail = scrapy_selector.xpath("//span[@class='_2aPCGjVZ']/span//text()").getall() 
                detail= ''.join(detail)    
            
            loader.add_value("sight_detail", f"{detail}")
            loader.add_value("sight_address",f"Adresse: {address}")
            loader.add_value("sight_duration", f"Vorgeschlagene Aufenthaltsdauer: {duration}")

            driver.quit()
        

        else:                                          #no dynamic: scrapy alone sufficient

            address = response.xpath("//span[@class='DrjyGw-P _1l3JzGX1']/text()").re(r'[^.]* Bayern [^.]*')
            duration = response.xpath("//div[@class='_3lExOEPJ']/div[@class='DrjyGw-P _26S7gyB4 _2nPM5Opx']/text()").get()
            detail = response.xpath("//div[@class='cPQsENeY u7nvAeyZ']/div[@class='DrjyGw-P _26S7gyB4 _2nPM5Opx']/text()").get()
            
            loader.add_value("sight_detail", f"{detail}")
            loader.add_value("sight_address", f"Adresse: {address}")
            loader.add_value("sight_duration", f"Vorgeschlagene Aufenthaltsdauer: {duration}")

        yield loader.load_item()
        

