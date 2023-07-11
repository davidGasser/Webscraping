# Webscraping

The paper for this project can be found [here](../blob/main/Ingenieurpraxis-final.pdf). However, it is in German.


The importance of data has increased rapidly in recent years, because it help us to personalize applications, improve processes, gain new insights as well as
obtain and make predictions, e.g. in the area of Machine Learning. The number of data is always a decisive factor, since with each valid data point we are able 
to get an improved insight into reality.

## Goal of the project
The scope of this project was to scrape information about tourist destinations in and around Munich, Germany. After considering multiple websites I focused mainly on 
Tripadvisor as their website layout is ideal for scraping and the information provided by the site is quite complete. For the implemetation, I used Scrapy and Selenium 
to scrape, adjust and filter the data. The output is simply a JSON file.

This is the site's layout:

![tripadvisor](https://github.com/davidGasser/Webscraping/assets/104353141/243906ec-7ee7-4e76-b832-341fdbbdeedf)



## Modes of operation

There are two modes of operation depending on the website. If the website is static, which means that it does not change depending on user input, the program
only uses scrapy as it is significantly faster without Selenium. 
The structure of the system can be seen here:

![scrapy_architecture_02](https://github.com/davidGasser/Webscraping/assets/104353141/8741470f-df54-427f-82b8-6101205795dc)

However, scrapy can not deal with dynamic websites, websites that change or are dependent on user input. Therefore Selenium is used to carry out clicks and entries.
The information gets sent to scrapy's engine which then uses the obtained data to do the usual operations. This comes with a increase of running time, but it allows 
you to scrape dynamic websites, which are by far the majority on the internet. 

![scrapy_selenium_architecture](https://github.com/davidGasser/Webscraping/assets/104353141/7711d327-c22a-4fe7-8fbf-37d1612f066c)
