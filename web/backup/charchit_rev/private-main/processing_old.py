from bs4 import BeautifulSoup as BS4
from collections import Counter
import requests as req
from stop_words import get_stop_words
import pprint
import lxml

def cleaner(data):
    for items in data:
        if items[0:len(our_url)] == our_url:
            temp_data.append(items)
    global clean_data
    clean_data = set(temp_data)


def crawler(url):
    
    global our_url
    our_url = url
              
    raw_data = []

    global temp_data
    temp_data = []
    
    global clean_data
    clean_data = []

    limit = 1
    
    count = 0
    
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
    
    source_code = req.get(url, "html.parser", headers=header).content

    soup = BS4(source_code, 'lxml')
    

    links = soup.findAll("a", href=True)
    

    
    for link in links:
        raw_data.append(str(link.get("href")))

    cleaner(raw_data)
    bites = ""
    
    while count < limit:


        for links in clean_data:
            temp = []
            source_code = req.get(links, "html.parser").content
            soup = BS4(source_code, 'lxml')
            bites = soup.findAll("a", href=True)
      
        for bite in bites:
            temp.append(str(bite.get("href")))  
        
        cleaner(temp)
            
        count += 1 
    
    return clean_data


def kw_ranking (urls):

    custom = ["!","'","£","$","%","&","(",")","?","^","*","+","/","-"]  #add further words to be excluded
    stop_words = get_stop_words("italian") + get_stop_words ("english") + custom
    
    best = []
    
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
    
    

    for url in urls:
        
        page  = req.get(url, "html.parser", headers = header ).content

        soup = BS4(page, "lxml")

        text = soup.findAll("p")

        text_clean =[]

        for slots in text:
            text_clean.append(slots.get_text().lower())
    
        text_all = "".join(text_clean).replace(",", "").replace(".","").replace("!","").replace("?","").split()
        
        for word in reversed(text_all):
            if word in stop_words:
                text_all.remove(word)
        
        rank = Counter(text_all)

        best.append(rank.most_common(5))
    
    named_kw = dict(zip(urls, best))
    
       
    return named_kw
if __name__ == '__main__':

    a = crawler("https://www.azionadigitale.com/")

    kw_ranking(a)
    