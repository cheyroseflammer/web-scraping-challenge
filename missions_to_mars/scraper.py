# Create imports
from bs4 import BeautifulSoup
from splinter import Browser
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import requests

# Define scraper function

def scrape():
    # Splinter set up
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    # Create dictonary instance
    mars_dict = {}
    ### Part One ###
    first_url = "https://redplanetscience.com/"
    # Request result from url
    browser.visit(first_url)
    # Assign HTML doc we grabbed
    html_one = browser.html
    soup = BeautifulSoup(html_one, 'html.parser')
    # Assign vars
    title = soup.find('div', class_= 'content_title').text
    paragraph = soup.find('div', class_= 'article_teaser_body').text
    # Append to mars_dict
    mars_dict['news_title'] = title
    mars_dict['news_p'] = paragraph
    
    
    ### Part Two ###
    mars_img_url = "https://spaceimages-mars.com/"
    # Open splinter instance for img url
    browser.visit(mars_img_url)
    image_url_find = browser.links.find_by_partial_href('featured').click
    # Grab browser html
    html = browser.html
    # BS HTML parser
    parser_one = BeautifulSoup(html, 'html.parser')
    # Grab img URL using class attr
    image_url = parser_one.find('img', attrs={'class': 'headerimage'})['src']
    # Put url together
    featured_image_url = mars_img_url + image_url
    # Append to mars_dict 
    mars_dict['featured_image'] = featured_image_url
    ### Part Three ###
    
    
    pandas_url = "https://galaxyfacts-mars.com/"
    # Reading the table
    facts_table = pd.read_html(pandas_url, header=0)
    facts_df = facts_table[0]
    # Set Index
    facts_table = facts_df.set_index('Mars - Earth Comparison')
    # Turn to html string
    table_string = facts_df.to_html()
    # Append to dict
    mars_dict['facts_df'] = table_string
    
    
    ### Part Four ###
    hem_url = "https://marshemispheres.com/"
    # create browser instance 
    browser.visit(hem_url)
    # Read in browser html
    hem_html = browser.html
    # Parse
    parser = BeautifulSoup(hem_html, "html.parser")
    # Grab divs
    results = parser.find_all('div', class_='description')
    # Create a mars_dict to append results to 
    hemi_imgs = []
    # For loop
    for result in results:
        dict = {}
        title = result.find('h3').text
        # Create browser click method
        browser.links.find_by_partial_text(title).click()
        # Grab image results now
        html_img = browser.html
        parser_img = BeautifulSoup(html_img, 'html.parser')
        img_results = parser_img.find('img', class_='wide-image')['src']
        # Put urls together
        img_url = hem_url + img_results
        dict['title'] = title
        dict['url'] = img_url
        # Append result 
        hemi_imgs.append(dict)
        browser.back()
    # Append all results to dict
    mars_dict['hemi_imgs'] = hemi_imgs
     # Close browser instance
    browser.quit()
    # Show results
    print(mars_dict)
    
scrape()