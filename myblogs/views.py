from django.http import HttpResponse # This is used instead of a template
import requests
#from bs4 import BeautifulSoup
from django.shortcuts import render
from django.views.generic.list import ListView 
from django.http import HttpResponseRedirect
import lxml
import sys
from selenium.webdriver.common.by import By  
from selenium import webdriver  
import feedparser
from selenium.webdriver.chrome.service import Service as C_Service


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
	
	
	feed = (feedparser.parse(
		'https://thecattycook.blogspot.com/feeds/posts/default?start-index=1&max-results=1000'))
	feed_html =""
	newfeed = list(feed.entries)
	options = webdriver.ChromeOptions()       
	options.add_argument("--headless")         
	options.add_argument("--disable-dev-shm-usage")
	options.add_argument("--disable-gpu")
	options.add_argument("--disable-features=NetworkService")
	options.add_argument("--window-size=1920x1080")
	options.add_argument("--disable-features=VizDisplayCompositor")             
	options.add_argument('--no-sandbox') # This is to prevent selenium webdriver chrome Message: unknown error: unable to discover open pages   
	options.add_argument("headless")   
	sel_ver = sys.modules[webdriver.__package__].__version__[0]
	if sel_ver == "4":        
		service = C_Service("C:\\Users\\Linda\\Dev\\blogger_health\\myblogs\\chromedriver.exe") # Specify the custom path new for Selenium 4 
		driver = webdriver.Chrome(options=options, service=service)        	 
	else: 
		driver = webdriver.Chrome(options=options, executable_path="C:\\Users\\Linda\\Dev\\blogger_health\\myblogs\\chromedriver.exe") 
	
	for i, post in enumerate(newfeed):    # Traverse through all the posts in the blog        
		 
		i = i + 1 
		url = post.link
		driver.get(url)          
		result=driver.find_element(By.XPATH, '//*[contains(@id, "post-body-")]')           
		the_length = len(result.text)     
		
		if the_length < 300:             
			if post.title == "":  # we need to put a placeholder in so it's easy to understand that there was no title
			   post.title = "NO TITLE"        
			feed_html = feed_html + "<a href=" + post.link + ">" + post.title + "</a>" + " " + str(the_length) + "<br>"  
				
	driver.quit()    
	if not feed_html:
		feed_html="none"
		
	return render(request, 'myblogs/count_words.html', {'feed_html': feed_html})     

#########################################

def count_words_all_blogs(request):
 
	url1 = "https://thecattycook.blogspot.com/feeds/posts/default?start-index=1&max-results=1000"    
	url2 = "https://djangojoy.blogspot.com/feeds/posts/default?start-index=1&max-results=1000"
	url3 = "https://www.geekaroundthehouse.com/feeds/posts/default?start-index=1&max-results=1000"
	url4 = "https://nycnocar.blogspot.com/feeds/posts/default?start-index=1&max-results=1000/"
	url5 = "https://speakingpython.blogspot.com/feeds/posts/default?start-index=1&max-results=1000/"
	url_list=[]
	url_list= url1, url2, url3, url4, url5
	feed_html_list=[]
	the_titles_list=[]
	for i in range(5):
		feed_html, the_title = my_temp_name(url_list[i])
		feed_html_list.append(the_title)
		feed_html_list.append(feed_html)

	 
	return render(request, 'myblogs/count_words_all_blogs.html', {'feed_html_list': feed_html_list})
#########################################
def my_temp_name(url):  # this function builds the list
	'''
	# This improved version of the above view will use a better cue for beautifulsoup
	# I found that all of the blog posts have the word "post-body-" followed by a number
	# That's what I will use
	# get the recipes from the RSS feed
	# loop through each recipe and count its words.
	# If word count is less than 3 hundred, store the recipe in a dictionary
	# create a list of all the dictionaries
	# I figured out that I could use selenium for post-body-<followed by post num> because selenium lets you do "contains."
	''' 

	feed = (feedparser.parse(url))
	#print("fee is", feed)
	feed_html =""
	newfeed = list(feed.entries)
	#print("newfeed is", newfeed)
	
	the_title = (feed['feed']['title'])
	
	options = webdriver.ChromeOptions()
	options.add_argument("--headless")         
	options.add_argument("--disable-dev-shm-usage")
	options.add_argument("--disable-gpu")
	options.add_argument("--disable-features=NetworkService")
	options.add_argument("--window-size=1920x1080")
	options.add_argument("--disable-features=VizDisplayCompositor")             
	options.add_argument('--no-sandbox') # This is to prevent selenium webdriver chrome Message: unknown error: unable to discover open pages   
	options.add_argument("headless")   
	sel_ver = sys.modules[webdriver.__package__].__version__[0]
	
	if sel_ver == "4":        
		service = C_Service("C:\\Users\\Linda\\Dev\\blogger_health\\myblogs\\chromedriver.exe") # Specify the custom path new for Selenium 4 
		driver = webdriver.Chrome(options=options, service=service)        	 
	else: 
		driver = webdriver.Chrome(options=options, executable_path="C:\\Users\\Linda\\Dev\\blogger_health\\myblogs\\chromedriver.exe") 
	driver = webdriver.Chrome(options=options, executable_path="C:\\Users\\Linda\\Dev\\blogger_health\\myblogs\\chromedriver.exe") 
	
	for i, post in enumerate(newfeed):    # Traverse through all the posts in the blog        
		 
		i = i + 1 
		url = post.link
		driver.get(url)          
		result=driver.find_element(By.XPATH, '//*[contains(@id, "post-body-")]')           
		the_length = len(result.text.split())        
		 
		
		
		if the_length < 100:             
			if post.title == "":  # we need to put a placeholder in so it's easy to understand that there was no title
			   post.title = "<i>NO TITLE</i>"        
			feed_html = feed_html + "<a href=" + post.link + ">" + post.title + "</a>" + ": " + str(the_length) + "<br>"  
				
	driver.quit()    
	if not feed_html:
		feed_html="<i>none</i>"
	return(feed_html, the_title)

   