#IMPORT DEPENDENCIES
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "ChromeDriverManager().install()"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = init_browser()
    mars_dict ={}
    # Mars News

    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html
    mars_soup = bs(html, "html.parser")

    news_title = mars_soup.find_all('div', class_='content_title')[0].text
    news_p = mars_soup.find_all('div', class_='article_teaser_body')[0].text

    # JPL IMAGE
    jpl_url = "https://spaceimages-mars.com"
    browser.visit(jpl_url)

    img_tag = browser.find_by_tag("button")[1]
    img_tag.click()

    html = browser.html
    jpl_soup = bs(html, 'html.parser') 

    rel_url = jpl_soup.find('img', class_='fancybox-image').get('src')

    featured_image_url = f'https://spaceimages-mars.com/{rel_url}'

    # Mars Facts

    facts_df = pd.read_html('https://galaxyfacts-mars.com')[0]
    facts_df.columns=['Description', 'Mars', 'Earth']
    facts_df.set_index('Description', inplace=True)

    facts = facts_df.to_html()

    # Hemispheres

    url = 'https://marshemispheres.com/'
    browser.visit(url)

    # CREATE LIST FOR HEMISPHERES
    hemisphere_urls = []

    # LIST ALL HEMISPHERES
    hemispheres = browser.find_by_css('a.product-item img')

    # Next, loop through those links, click the link, find the sample anchor, return the href
    for item in range(len(hemispheres)):
        hemisphere = {}
        
        #IDENTIFY ELEMENTS
        browser.find_by_css('a.product-item img')[item].click()
        
        #HEMISPHERE TITLE
        hemisphere["title"] = browser.find_by_css("h2.title").text
        
        # IDENTIFY IMG ANCHOR/USE HREF
        img_anchor = browser.links.find_by_text('Sample').first
        hemisphere['img_url'] = img_anchor['href']
        
        
        # APPEND TO LIST
        hemisphere_urls.append(hemisphere)
        
    
        browser.back()

    browser.quit()


    mars_dict = {
            "news_title": news_title,
            "news_p": news_p,
            "featured_image_url": featured_image_url,
            "facts": facts,
            "hemisphere_urls": hemisphere_urls,
    }


    return mars_dict

