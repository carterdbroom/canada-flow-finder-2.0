# Canada Flow Finder 2.0
A fully fledged app based on the first Canada Flow Finder
---
### Day 1
Today I planned out what I wanted this project to be and what I wanted to accomplish with it. I want to have an active userbase for this app. If want that, I need to make some changes to Flow Finder 1.0. For the first one, I used an awesome API that allows me to have over 200 requests per day, which is nice for a small command line tool that I can use for myself, but that won't cut it for hundreds, if not thousands of users. I checked out the Government of Canada's [Water Office](https://wateroffice.ec.gc.ca/) site, which is where the data comes from. I realized I could do some web scraping to get the data for each station. I started some programming and used the API from [SCRAPI](https://scrap2api.web.app/) to get a list of every station ID since I will need to modify the download URL for each station to get the data. I also have decided on what tech stack I am going to use.

---
### Day 2
I started working on the web scraper to get the csv data. I learned lots on Selenium, a super cool web scraping technology. I played around with it a bit and started making some progress towards downloading the csv file for each station. Tomorrow I should have the web scraping component fully functional. 