# Dependencies
import time
from splinter import Browser
from bs4 import BeautifulSoup
import pandas as pd

def init_browser():
    executable_path = {'executable_path': './chromedriver.exe'}
    return Browser("chrome", **executable_path, headless=False)

#Function to get Hemisphere image
def get_image_url(item):
    new_browser = init_browser()
    remove = " Enhanced"
    thelen = len(remove)
    new_item = item
    if item[-thelen:] == remove:
        new_item = item[:-thelen]
    hemis_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    attempt = 2
    while attempt>=1:
        try:
            new_browser.visit(hemis_url)
            new_browser.click_link_by_partial_text(item)
            img_root = "https://astrogeology.usgs.gov"
            img_response = new_browser.html
            himg_soup = BeautifulSoup(img_response, 'html.parser')
            image_link = himg_soup.find('img', class_="wide-image")
            image = image_link['src']
            image_url = f"{img_root}{image}"
    
        except:
            attempt -= 1
            print(f"An error occured. There {attempt} attempt left")
            time.sleep(2)

        else:
            attempt = 0
    new_browser.quit()
    return {'title':new_item, "img_url": image_url}


def scrape():

    browser = init_browser()
    mars_info = {}

    # ## NASA Mars News
    # Scrape the NASA Mars News Site and collect the latest News Title and Paragraph Text.
    nasa_url = 'https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest'
    attempt = 2
    while attempt>=1:
        try:
            browser.visit(nasa_url)
            news_response = browser.html
            nasa_soup = BeautifulSoup(news_response, 'html.parser')
            # Identify and return title of content
            news_title = nasa_soup.find('div', class_="content_title").text
        
            # Identify and return the paragraph
            news_p = nasa_soup.find('div', class_="article_teaser_body").text 
        
            mars_info["news_title"] = news_title
            mars_info["news_p"] = news_p
        
        except:
            attempt -= 1
            print(f"An error occured. There {attempt} attempt left")
            time.sleep(2)
            
        else:
            attempt = 0


    # ## JPL Mars Space Images - Featured Image
    url_root = "https://www.jpl.nasa.gov"
    im_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    attempt = 2
    while attempt>=1:
        try:
            browser.visit(im_url)
            browser.click_link_by_partial_text("FULL IMAGE")
            img_response = browser.html
            feat_soup = BeautifulSoup(img_response, 'html.parser')
            image_link = feat_soup.find('img', class_="fancybox-image")
            image = image_link['src']
            featured_image_url = f"{url_root}{image}"
            mars_info["featured_image_url"] = featured_image_url
        
        except:
            attempt -= 1
            print(f"An error occured. There {attempt} attempt left")
            time.sleep(2)
            
        else:
            attempt = 0


    # ## Mars Weather
    twit_url = "https://twitter.com/marswxreport?lang=en"
    attempt = 2
    while attempt>=1:
        try:
            browser.visit(twit_url)
            twit_response = browser.html
            weath_soup = BeautifulSoup(twit_response, 'html.parser')
            tweet = weath_soup.find('div', class_="js-stream-tweet")
            weather = tweet.find('p', class_="tweet-text")
            unwanted = weather.find('a')
            unwanted.extract()
            mars_weather = weather.text.strip()
            mars_info["mars_weather"] = mars_weather
        
        except:
            attempt -= 1
            print(f"An error occured. There {attempt} attempt left")
            time.sleep(2)
            
        else:
            attempt = 0


    # ## Mars Facts
    fact_url = "https://space-facts.com/mars/"
    table = pd.read_html(fact_url,thousands=',')[0].rename(columns={0:'Parameter',1:'Value'})
    mars_fact = table.to_html(index=False)
    mars_info["mars_fact"] = mars_fact


    # ## Mars Hemispheres

    #Get the list of the Hemispheres
    hemis_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    attempt = 2
    while attempt>=1:
        try:
            browser.visit(hemis_url)
            hemis_response = browser.html
            hemis_soup = BeautifulSoup(hemis_response, 'html.parser')
            items = hemis_soup.find_all("div", class_="description")
            hemisphere_title = []
            for item in items:
                title_text = item.find('h3').text
                hemisphere_title.append(title_text)
        except:
            attempt -= 1
            print(f"An error occured. There {attempt} attempt left")
            time.sleep(2)
            
        else:
            attempt = 0

    #Get the Hemispheres images urls
    hemisphere_image_urls = list(map(get_image_url, hemisphere_title))
    mars_info["hemisphere_image_urls"] = hemisphere_image_urls

    browser.quit()
    return mars_info
