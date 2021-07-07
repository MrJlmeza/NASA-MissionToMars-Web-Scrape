#IMPORT DEPENDENCIES
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager


def scrape():
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)

    #####-MARS NEWS-#####
    url = "https://redplanetscience.com/"
    browser.visit(url)

    html = browser.html
    mars_soup = bs(html, "html.parser")
    
    title_class = mars_soup.select_one('div.list_text')

    #FIND DIV FOR TITLE OF ARTICLE
    title_class.find('div', class_='content_title')

    #SAVE TITLE TEXT WITH VARIABLE
    title_text = title_class.find('div', class_='content_title').get_text()

    #SAVE ARTICLE PREVIEW TEXT WITH VARIABLE
    article_text = title_class.find('div', class_='article_teaser_body').get_text()
    
    #####-JPL-#####
    # VISIT URL
    jpl_url = "https://spaceimages-mars.com"
    browser.visit(jpl_url)
    
    # FIND IMG TAG
    img_tag = browser.find_by_tag("button")[1]
    img_tag.click()

    html = browser.html
    jpl_soup = bs(html, 'html.parser') 

    rel_url = jpl_soup.find('img', class_='fancybox-image').get('src')

    featured_image_url = f'https://spaceimages-mars.com/{rel_url}'

    #####-MARS FACTS-#####
    facts_df = pd.read_html('https://galaxyfacts-mars.com')[0]

    facts_df.columns=['Description', 'Mars', 'Earth']
    facts_df.set_index('Description', inplace=True)
    
    mars_facts = facts_df.to_html()

    #####-HEMISPHERES-#####
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
    
    mars_dictionary = {
        "news_title": title_text,
        "news_paragraph": article_text,
        "featured_image_url": featured_image_url(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
    }

    browser.quit()

    return mars_dictionary


