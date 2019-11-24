#!/usr/bin/env python
# coding: utf-8


from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd
import requests
import time

def scrape_info():

    # Using Splinter to initialize Chrome browser
    executable_path={'executable_path':'C:\\Users\\slake\\Downloads\\chromedriver_win32\\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)



    # NASA Mars articles site
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    browser.is_element_present_by_css("ul.item_list li.slide", wait_time=1)




    # Parse results HTML with BeautifulSoup. Scraping web page into soup.
    html = browser.html
    news_soup = BeautifulSoup(html, "html.parser")

    # Find title and paragraph elements

    slide_elem = news_soup.select_one("ul.item_list li.slide")
    slide_elem.find("div", class_="content_title")


    article_title = slide_elem.find("div",class_="content_title").get_text()

    article_title


    article_content = slide_elem.find("div",class_="article_teaser_body").get_text()

    article_content

    # ++++++++++++++++++++++++++++++++++++++++
    # Jet Propulsion Lab Mars space images site

    url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    browser.find_by_id("full_image").first.click()


    # Click full image button(code above) then click the more info button on the second page to get to the image link for the lg file.


    browser.click_link_by_partial_text('more info')



    html=browser.html
    full_size_img_soup=BeautifulSoup(html, "html.parser")
    images=full_size_img_soup.find_all('img', {"class":"main_image"})
    featured_image =images[0]['src']
    base_url='https://www.jpl.nasa.gov'
    # print(base_url + featured_image)
    featured_img_url = base_url + featured_image



    # ++++++++++++++++++++++++++++++++++++++++++++++
    # Mars Weather from Twitter
    executable_path={'executable_path':'C:\\Users\\slake\\Downloads\\chromedriver_win32\\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)



    twitter_url="https://twitter.com/marswxreport?lang=en"
    browser.visit(twitter_url)
    time.sleep(1)
    html = browser.html
    weather_soup = BeautifulSoup(html,"html.parser")



    mars_tweet = weather_soup.find('p', class_ ='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').get_text()
    mars_tweet



    # +++++++++++++++++++++++++++++++++++++++++++++++
    # Dataframe of Mars Facts
    mars_facts_url= 'https://space-facts.com/mars/'
    mars_df = pd.read_html(mars_facts_url)[0]
    print(mars_df)
    mars_df.columns=["Description","Value"]
    mars_df



    facts_html = mars_df.to_html(index=False)
    facts_html



    # ++++++++++++++++++++++++++++++++++++++++++
    # Mars Hemispheres images

    executable_path={'executable_path':'C:\\Users\\slake\\Downloads\\chromedriver_win32\\chromedriver.exe'}
    browser = Browser('chrome', **executable_path, headless=False)
    url="https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)



    hemph_img_urls = []
    hemph_dictionary = {"title": [] , "img_url": []}
    hemph_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    # Resource Github juliasweet
    home = browser.html
    hemph_soup = BeautifulSoup(home, "html.parser")
    results = hemph_soup.find_all("h3")
    for result in results:
        title = result.text[:-9]
    #     print(title)
        browser.click_link_by_partial_text(title)
        time.sleep(1)
        img_url = browser.find_link_by_partial_href("download")["href"]
    #     print(img_url)
        hemph_dictionary = {"title": title, "img_url": img_url}
        hemph_img_urls.append(hemph_dictionary)
        time.sleep(1)
        browser.visit(hemph_url)
        print(hemph_dictionary)

    # Store data in a dictionary
    mars_data = {
        "article_title": article_title,
        "article_content": article_content,
        "featured_img": featured_img_url,
        "mars_weather": mars_tweet,
        # facts_html place holder (how does that fit in the dictionary),
        "facts": facts_html,
        "hemph_dictionary": hemph_dictionary

    }
    # Close browser after scraping
    browser.quit()

    # Return results
    return mars_data





