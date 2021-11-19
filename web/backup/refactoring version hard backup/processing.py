#versione aggressiva tutta multithreading

from bs4 import BeautifulSoup as BS4
from collections import Counter
import requests as req
import nltk
from nltk.corpus import stopwords

nltk.download('stopwords')

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
    
    temp = []  

    limit = 1
    
    count = 0

    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}
   
    source_code = req.get(url, "html.parser", headers=header).content

    soup = BS4(source_code, 'lxml')

    links = soup.findAll("a", href=True)
    
    for link in links:
        raw_data.append(str(link.get("href")))
        
    for i in raw_data:
        try:
            if i[0] == "/":
                raw_data.append(url+i)
        except Exception as e:
            pass
          
    cleaner(raw_data)
    
    while count < limit:    
        try:
            with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
                futures = [executor.submit(scraper, link)for link in clean_data]
                for result in as_completed(futures):
                    temp.append(result.get("href"))
        except Exception as e:
                pass       

        cleaner(temp)

        count += 1
         
    return clean_data


def kw_ranking (url):
           
    custom = ["!","'","£","$","%","&","(",")","?","^","*","+","/","-", "©"]  #add further words to be excluded
    stopwords_overall = stopwords.words('italian')  + stopwords.words('english') + custom
    
    best = []
    
    # for url in urls: #devo modificare questa parte perchè il ciclo for lo fa già il multithreading
        
    page  = req.get(url, "html.parser").content

    soup = BS4(page, "lxml")

    text = soup.findAll("p")

    text_clean =[]

    for slots in text:
        text_clean.append(slots.get_text().lower())

    text_all = "".join(text_clean).replace(",", "").replace(".","").replace("!","").replace("?","").split()

    for word in reversed(text_all):
        if word in stopwords_overall:
            text_all.remove(word)

    rank = Counter(text_all)

    best.append(rank.most_common(5))
    
    named_kw = dict(zip(url, best))
    
       
    return named_kw