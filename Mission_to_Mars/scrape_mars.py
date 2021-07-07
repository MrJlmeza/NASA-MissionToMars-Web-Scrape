#IMPORT DEPENDENCIES
from bs4 import BeautifulSoup as bs
from splinter import Browser
import pandas as pd
from webdriver_manager.chrome import ChromeDriverManager
import datetime as dt




def scrape_all():
    executable_path = {"executable_path": ChromeDriverManager().install()}
    browser = Browser("chrome", **executable_path, headless=True)

    title_text, article_text = mars_soup(browser)

    data = {
        "news_title": title_text,
        "news_paragraph": article_text,
        "featured_image_url": featured_image_url(browser),
        "facts": mars_facts(),
        "hemispheres": hemispheres(browser),
        "last_modified": dt.datetime.now()
    }

    # Stop webdriver and return data
    browser.quit()
    return data


def mars_news(browser):

    # Scrape Mars News
    # Visit the mars nasa news site
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    # Convert the browser html to a soup object and then quit the browser
    html = browser.html
    mars_soup = bs(html, 'html.parser')

    # Add try/except for error handling
    try:
        title_class = mars_soup.select_one('div.list_text')
        # Use the parent element to find the first 'a' tag and save it as 'news_title'
        title_text = title_class.find("div", class_="content_title").get_text()
        # Use the parent element to find the paragraph text
        article_text = title_class.find("div", class_="article_teaser_body").get_text()

    except AttributeError:
        return None, None

    return news_title, news_p


def featured_image(browser):
    # Visit URL
    url = 'https://spaceimages-mars.com'
    browser.visit(url)

    # Find and click the full image button
    img_tag = browser.find_by_tag('button')[1]
    img_tag.click()

    # Parse the resulting html with soup
    html = browser.html
    jpl_soup = bs(html, 'html.parser')

    # Add try/except for error handling
    try:
        # find the relative image url
        rel_url = jpl_soup.find('img', class_='fancybox-image').get('src')

    except AttributeError:
        return None

    # Use the base url to create an absolute url
    featured_image_url = f'https://spaceimages-mars.com/{rel_url}'

    return featured_image_url


def mars_facts():
    # Add try/except for error handling
    try:
        # use 'read_html' to scrape the facts table into a dataframe
        facts_df = pd.read_html('https://galaxyfacts-mars.com')[0]

    except BaseException:
        return None

    # assign columns and set index of dataframe
    facts_df.columns = ['Description', 'Mars', 'Earth']
    facts_df.set_index('Description', inplace=True)

    # Convert dataframe into HTML format, add bootstrap
    return facts_df.to_html(classes="table table-striped")


def hemispheres(browser):
    url = 'https://marshemispheres.com/'

    browser.visit(url + 'index.html')

    # Click the link, find the sample anchor, return the href
    hemisphere_urls = []
    for item in range(4):
        # Find the elements on each loop to avoid a stale element exception
        browser.find_by_css("a.product-item img")[item].click()
        hemi_data = scrape_hemisphere(browser.html)
        hemi_data['img_url'] = url + hemi_data['img_url']
        # Append hemisphere object to list
        hemisphere_image_urls.append(hemi_data)
        # Finally, we navigate backwards
        browser.back()

    return hemisphere_image_urls


def scrape_hemisphere(html_text):
    # parse html text
    hemi_soup = soup(html_text, "html.parser")

    # adding try/except for error handling
    try:
        title_elem = hemi_soup.find("h2", class_="title").get_text()
        sample_elem = hemi_soup.find("a", text="Sample").get("href")

    except AttributeError:
        # Image error will return None, for better front-end handling
        title_elem = None
        sample_elem = None

    hemispheres = {
        "title": title_elem,
        "img_url": sample_elem
    }

    return hemispheres


if __name__ == "__main__":

    # If running as script, print scraped data
    print(scrape_all())


    