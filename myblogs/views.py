from django.http import HttpResponse # This is used instead of a template
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from django.views.generic.list import ListView 
from django.http import HttpResponseRedirect


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
        soup = BeautifulSoup(r.text, 'html.parser')         
        r = requests.get(post.link)
        soup = BeautifulSoup(r.text, 'html.parser')
        result = soup.find(itemprop='description articleBody')
        
        the_length = len(result.get_text())
        if the_length < 300:             
            if post.title == "":
               post.title = "NO TITLE"        
            feed_html = feed_html + "<a href=" + post.link + ">" + post.title + "</a>" + " " + str(the_length) + "<br>"  
                
    
    if not feed_html:
        feed_html="none"
        
    return render(request, 'myblogs/count_words.html', {'feed_html': feed_html})
