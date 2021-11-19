import requests as req
from collections import Counter
from bs4 import BeautifulSoup as BS4
import nltk
from nltk.corpus import stopwords
from concurrent.futures import ThreadPoolExecutor, as_completed

nltk.download('stopwords')

# global var
MAX_THREADS = 50
HEADER = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.85 Safari/537.36'}

# cleaner function to remove non-internal urls   
def cleaner(data):
    """Cleans data from external url"""
    for items in data:
        if items[0:len(our_url)] == our_url:
            temp_data.append(items)
    global clean_data
    clean_data = set(temp_data)

# function to crawls the website and search for internal urls
def crawler(url):
    """Scrape given url and search for internal urls

    Args:
        url (string): provide a complete url in the form "https://www.example.com"

    Returns:
        List: all the urls of the website
    """
    global our_url
    our_url = url

    global temp_data
    temp_data = []
    
    global clean_data
    clean_data = []
    
    raw_data = []
    temp = []  
    limit = 1
    count = 0

    source_code = req.get(url, "html.parser", headers=HEADER).content

    soup = BS4(source_code, 'lxml')

    links = soup.findAll("a", href=True)
    
    # append the internal urls to a list, iteratively
    def raw_append(link):
        raw_data.append(str(link.get("href")))

    with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
        futures = [executor.submit(raw_append, link)for link in links] 
        
    for i in raw_data:
        try:
            if i[0] == "/":
                raw_data.append(url+i)
        except Exception as e:
            print(f"[!!!] Exception occurred (a): {e}")
    
    # call the cleaner function to purge the external urls        
    cleaner(raw_data)
    
    # define a scraper function to run within the multithread executor
    def scraper(link):
        source_code = req.get(link, "html.parser").content
        soup = BS4(source_code, 'lxml')
        bites = soup.findAll("a", href=True)

    while count < limit:    
        try:
            with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
                futures = [executor.submit(scraper, link)for link in clean_data]
                for result in as_completed(futures):
                    temp.append(result.get("href"))
        except Exception as e:
            print(f"[!!!] Exception occurred (b): {e}")      

        cleaner(temp)
        
        # increase the counter, to stay within the limit and avoid very long running loops
        count += 1
         
    return clean_data

# lets' count the number of times a word appears in a given text within each url
def kw_ranking (url):
    """Function to scan the text of each url and count the number of times a word appears

    Args:
        url (string): provide a complete url in the form "https://www.example.com"

    Returns:
        dict: link and kword count
    """    
    # define our list of stopwords
    custom = ["!","'","£","$","%","&","(",")","?","^","*","+","/","-", "©"]  # add further words to be excluded
    stopwords_overall = stopwords.words('italian')  + stopwords.words('english') + custom
    
    # scrape the url
    best = []
           
    page  = req.get(url, "html.parser", headers=HEADER).content

    soup = BS4(page, "lxml")

    text = soup.findAll("p")

    text_clean =[]
    
    # clean the text from unwanted characters
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

# let's start our scraping routine:
# ask user for a url
url = input("[+] Enter a url: ")

# launch the crawler
links = crawler(url)

# launch the multi-threaded keyword ranking function
with ThreadPoolExecutor(max_workers=MAX_THREADS) as executor:
    futures = {executor.submit(kw_ranking, link): link for link in links}
    for result in as_completed(futures):
        link = futures.get(result)
        try:
            data=result.result()
        except Exception as e:
            print(f"[!!!] Exception occurred (b): {e}") 
        else:
            print (f"Link: {link}:\nData:{data}")
            