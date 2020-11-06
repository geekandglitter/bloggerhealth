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
        #  driver = webdriver.Chrome("c:\\data\\chromedriver\\chromedriver.exe", options=options)
        #driver = webdriver.Chrome(executable_path='chromedriver.exe')
        #driver = webdriver.Chrome("C:\Windows")
        driver = webdriver.Chrome("C:\\Users\\Linda\\Dev\\blogger_health\\myblogs\\chromedriver.exe")
        
        #driver = webdriver.Chrome("c:\\data\\chromedriver\\chromedriver.exe")
        #browser = webdriver.PhantomJS(executable_path = "/usr/local/Cellar/phantomjs/2.1.1/bin/phantomjs")
        # UserWarning: Selenium support for PhantomJS has been deprecated, please use headless versions of Chrome or Firefox instead.
        print("driver is", driver)
        print("drive type is", type(driver))
        print("post.link is", post.link)
        print("type of post.link is", type(post.link))
        # Perhaps you meant http://post.link?
        url ="https://thecattycook.blogspot.com/2020/11/sugar-snap-peas-and-pasta.html"
        driver.get(url)    
        result=driver.find_element(By.XPATH, '//*[@id="post-body-590782127147809932"]')
        #result = r.find(id_='post-body-590782127147809932')
        # elem=driver.find_element(By.XPATH, '//*[@id="search-6"]/form/label/input') # We
        # //*[@id="post-body-590782127147809932"]
        #print(result.text)     
      
        
        the_length = len(result.text)
        print("the type of result is", type(result))
        print("the_length is", the_length)
        print("size is", the_length)
        
        if the_length < 300:             
            if post.title == "":
               post.title = "NO TITLE"        
            feed_html = feed_html + "<a href=" + post.link + ">" + post.title + "</a>" + " " + str(the_length) + "<br>"  
                
    
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