from django.http import HttpResponse # This is used instead of a template
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.views.generic.list import ListView 
from django.http import HttpResponseRedirect
import lxml
import sys


###################################################
# VIEW
###################################################
def home(request):
    """ Shows a menu of views for the user to try """
    return render(request, 'myblogs/index.html')
    
def count_words(request):
    '''
    # get the recipes from the RSS feed
    # loop through each recipe and count its words.
    # If word count is less than a hundred, store the recipe in a dictionary
    # create a list of all the dictionaries
    # I tried to use this for my other blogs, but they don't all have "itemprop."
    # They do all have post-body-####### (followed by a number for each post)
    ''' 
    
    import feedparser
    feed = (feedparser.parse(
        'https://thecattycook.blogspot.com/feeds/posts/default?start-index=1&max-results=1000'))
    feed_html =""
    newfeed = list(feed.entries)
    
    
    for i, post in enumerate(newfeed):
        i = i + 1
        r = requests.get(post.link)        
        soup = BeautifulSoup(r.text, 'lxml')         
         
        result = soup.find(itemprop='description articleBody')
        
        the_length = len(result.get_text())
        if the_length < 300:             
            if post.title == "":
               post.title = "NO TITLE"        
            feed_html = feed_html + "<a href=" + post.link + ">" + post.title + "</a>" + " " + str(the_length) + "<br>"  
                
    
    if not feed_html:
        feed_html="none"
        
    return render(request, 'myblogs/count_words.html', {'feed_html': feed_html})

def count_words_improved(request):
    '''
    # This improved version of the above view will use a better cue for beautifulsoup
    # I found that all of the blog posts have the word "post-body-" followed by a number
    # That's what I will use
    # get the recipes from the RSS feed
    # loop through each recipe and count its words.
    # If word count is less than a hundred, store the recipe in a dictionary
    # create a list of all the dictionaries
    # I figured out that I could use selenium for post-body-<followed by post num> because selenium lets you do "contains."
    ''' 
    
    import feedparser
    feed = (feedparser.parse(
        'https://thecattycook.blogspot.com/feeds/posts/default?start-index=1&max-results=1000'))
    feed_html =""
    newfeed = list(feed.entries)
    
    
    for i, post in enumerate(newfeed):
        from selenium.webdriver.common.by import By  
         
         
        i = i + 1
        from selenium import webdriver  
        options = webdriver.ChromeOptions()       
        options.add_argument("--headless")
        options.add_argument("--no-sandbox")
        options.add_argument("--disable-dev-shm-usage")
        options.add_argument("--disable-gpu")
        options.add_argument("--disable-features=NetworkService")
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--disable-features=VizDisplayCompositor") 
            
        options.add_argument('--no-sandbox') # This is to prevent selenium webdriver chrome Message: unknown error: unable to discover open pages   
        options.add_argument("window-size=1920x1080")
        options.add_argument("headless")   
        driver = webdriver.Chrome(options=options, executable_path="C:\\Users\\Linda\\Dev\\blogger_health\\myblogs\\chromedriver.exe")
        
       
   
        url = post.link
        driver.get(url)    
      
        result=driver.find_element(By.XPATH, '//*[contains(@id, "post-body-")]')   
        
        the_length = len(result.text)
         
        
        if the_length < 300:             
            if post.title == "":
               post.title = "NO TITLE"        
            feed_html = feed_html + "<a href=" + post.link + ">" + post.title + "</a>" + " " + str(the_length) + "<br>"  
                
        driver.quit()
    if not feed_html:
        feed_html="none"
        
    return render(request, 'myblogs/count_words.html', {'feed_html': feed_html})     



'''
#########################################################
Scraping without JS support:
import requests
from bs4 import BeautifulSoup
response = requests.get(my_url)
soup = BeautifulSoup(response.text)
soup.find(id="intro-text")
# Result:
<p id="intro-text">No javascript support</p>

#########################################################

Scraping with JS support:
from selenium import webdriver
driver = webdriver.PhantomJS()
driver.get(my_url)
p_element = driver.find_element_by_id(id_='intro-text')
print(p_element.text)
# result:
'Yay! Supports javascript'
#########################################################
    '''