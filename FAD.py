'''
This is my forum scraper, searches for paticular words in posts
Returns a list of links of topics
'''
import urllib.request
from bs4 import BeautifulSoup
import re


def match_class(target):
    '''Stolen from some comment on StackOverflow, matches a div by a classname'''
    def do_match(tag):                                                          
        classes = tag.get('class', [])                                          
        return all(c in classes for c in target)                                
    return do_match

def find_posts(words, min_page, max_page):
    '''Words is a list of strings to check against, min page and max page are the bounds respectively, right exclusive'''
    main_url = "http://www.yassl.com/forums/forum3-wolfssl-formerly-cyassl" #wolf forums
    res = []
    for i in range(min_page,max_page): #iterate through all pages
        url = main_url +  (".html" if (i==0) else ("-p" + str(i) + ".html")) #the first page has no number
        html_page = urllib.request.urlopen(url).read() #get raw html from page, destroys whitespace
        soup = BeautifulSoup(html_page) #This package is amazing

        links = []
        for link in soup.findAll('a'): #find all links on the page
            links.append(link.get('href'))

        topic_re = re.compile(".+/topic.*") #super dirty regex to find all links to topics
        finals = []

        for l in links:
            if (topic_re.match(l) != None):
                finals.append(l)

        for f in finals: #iterate through all topics
            html_page = urllib.request.urlopen(f).read()
            soup = BeautifulSoup(html_page)
            for i in soup.find_all(match_class(['entry-content'])): #iterate through all posts
                if any(word.lower() in i.text.lower() for word in words): #check 
                    res.append(f)
                    break
    return res

find_posts(['CyaSSL'],1,13)






