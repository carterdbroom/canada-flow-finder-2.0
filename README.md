# Canada Flow Finder 2.0
### A fully fledged app based on the first Canada Flow Finder

---
### Day 1
Today I planned out what I wanted this project to be and what I wanted to accomplish with it. I want to have an active userbase for this app. If want that, I need to make some changes to Flow Finder 1.0. For the first one, I used an awesome API that allows me to have over 200 requests per day, which is nice for a small command line tool that I can use for myself, but that won't cut it for hundreds, if not thousands of users. I checked out the Government of Canada's [Water Office](https://wateroffice.ec.gc.ca/) site, which is where the data comes from. I realized I could do some web scraping to get the data for each station. I started some programming and used the API from [SCRAPI](https://scrap2api.web.app/) to get a list of every station ID since I will need to modify the download URL for each station to get the data. I also have decided on what tech stack I am going to use.

---
### Day 2
I started working on the web scraper to get the csv data. I learned lots on Selenium, a super cool web scraping technology. I played around with it a bit and started making some progress towards downloading the csv file for each station. Tomorrow I should have the web scraping component fully functional. 

--- 
### Day 3
I made lots of progress, learned about how to navigate through HTML elements with XPath. I am now able to download the data for each river station. I had to work on some error handling since not every station has discharge data. One concern that I am starting to have is the amount of time it will take to download all the data. I haven't even started reading the csv data, and it still takes roughly 7 to 8 seconds for every station. There are over 2000 stations on the website, meaning it will take around 14 to 16 thousand seconds to just download all the data. This means I will only be able to update the gauges on the app every 4 or 5 hours. I can get rid of the stations that don't have discharge data, but there aren't many. I may have to rethink how to approach this problem. I think I can use the requests library to make HTTP requests and simulate cookies so I don't have to do as many clicks. Right now, the site uses cookies to know what data to give me when I go to the generic download page. Right now I'm literally clicking through to each station page to "set" the cookies for each station. I'll figure out how to fix this issue tomorrow. 

--- 
### Day 4
I made a plan to fix the download time for all of the stations. Selenium has a headless mode that supposedly speeds things up, and I can disable images as well. I can also do some multiprocessing to improve speed. I'll test each of these strategies tomorrow. 