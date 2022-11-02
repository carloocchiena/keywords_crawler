"""
Functions repository
Here you have the functions needed to scrape and clean the data
from the given url.
"""

from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed

from bs4 import BeautifulSoup as bs4
import requests

from stop_words import stop_words_update



def url_crawler(url: str) -> list:
    """Crawl a website and find all the internal urls

    Args:
        url (str): the url that need to be scraped

    Returns:
        list: a list of all the internal url find in the target website
    """
    raw_data = []
    
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}

    try:
        source_code = requests.get(url, 'html.parser', headers=header).content
        soup = bs4(source_code, 'html.parser')
        links = soup.find_all('a', href=True)
    except ConnectionError:
        print(f'[!!!] Connection error for: {url}')
        
    for link in links:
        raw_data.append(str(link.get('href')))
    
    return raw_data
    

def url_cleaner(url: str, data: list) -> list:
    """Clean the urls

    Args:
        url (str): the website that need to be scraped
        data (list): the list of raw urls

    Returns:
        list: list cleaned
    """
    clean_data = []
    
    for link in data:
        if link[0] == '/':
            clean_data.append(url + link)
        
        if link[0:len(url)] == url:
            clean_data.append(link)
            
    clean_data = set(clean_data)
    
    return list(clean_data)
        
    
def crawler_iterator(data: list, limit: int=1) -> list:
    """Iterate through link and search for link in links

    Args:
        data (list): url list data
        limit (int, optional): max. no of iterations. Defaults to 1 for standard use cases. 
        Extend in case you need to create a site tree or a complete mapping of urls. 

    Returns:
        list: raw urls list
    """
    count = 0
    raw_data = []
    
    while count < limit:
        with ThreadPoolExecutor(max_workers=5) as executor:
            futures = [executor.submit(url_crawler, link) for link in data]

            for future in as_completed(futures):
                try:
                    raw_data.extend(future.result())
                except AttributeError as e:
                    print(f'[!!!] Error is: {e}')
                    
        count += 1
    
    return raw_data


def text_extractor(url: str) -> list:
    """Text Extractor from a URL

    Args:
        url (str): the url that you want to extract text from

    Returns:
        list: the raw list included in the webpage, cleaned and uniformed
    """
    header = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 13_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/106.0.0.0 Safari/537.36'}
    
    text_clean = []

    try:
        webpage = requests.get(url, 'html.parser', headers=header).content
        soup = bs4(webpage, 'html.parser', from_encoding='utf-8')
        text = soup.findAll('p')
    except ConnectionError:
        print(f'[!!!] Connection error for: {url}')
        
    for slots in text:
        text_clean.append(slots.get_text().lower())

    text_all = "".join(text_clean).replace(",", "").replace(".","").replace("!","").replace("?","").split()
    
    # return text_all
    # mi serve che questa funzione sia risolutiva (ritorni il risultato finale desiderato)
    # così da poterla richiamare in multithread
    
    clean_word_list = stop_word_remover(text_all, stop_words_update())
    
    kw_ranked = kw_ranker(clean_word_list, 5)
    
    return kw_ranked
    
    
def stop_word_remover(text: list, stop_words:list) -> list:
    """remove stop words from a text doc

    Args:
        text (list): _the text you want to purge
        stop_words (list): _the list of stop words

    Returns:
        list: a list of words cleaned from stop words
    """

    text_clean = text

    for word in text_clean[:]:
        if word in stop_words:
            text_clean.remove(word)
        
    return text_clean


def kw_ranker(text:list, n_items:int) -> dict:
    """_summary_

    Args:
        text (list): a text, inputed as a list
        n_items (int): the number of rank you want to extract, "top n ranks"

    Returns:
        dict: a dictionary where the keys are the words and the items are their frequencies
    """
    top_kw = []
    rank = Counter(text)
    top_kw.extend(rank.most_common(n_items))
    kw_rank = dict(top_kw)
    
    return kw_rank
    

def rank_iterator(data: list) -> list:
    """_summary_

    Args:
        data (list): a list of url that need to be ranked

    Returns:
        list: a list of all the urls and most frequent words
    """
    end_result = []
    
    with ThreadPoolExecutor(max_workers=5) as executor:
        futures = {executor.submit(text_extractor, link): link for link in data}
        for result in as_completed(futures):
            link = futures.get(result)
            try:
                rank_result = result.result()
            except AttributeError as e:
                print(f'[!!!] Error is: {e}')
            else:
                print (f'Link: {link}:\nData:{rank_result}')
                goal = f'Link: {link}:\nData:{rank_result}'
                end_result.append(goal)
    
    return end_result
 

if __name__ == '__main__':
    my_list = ['https://www.google.com', 'https://www.azionadigitale.com']
    my_url =  'https://www.azionadigitale.com'
