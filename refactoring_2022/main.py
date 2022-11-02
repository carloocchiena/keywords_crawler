from functions import crawler_iterator, rank_iterator, url_crawler, url_cleaner

def orchestrator(site_url: str) -> list:
    """Orchestrator function for the main ranking process

    Args:
        url (str): the url that need to be scraped

    Returns:
        list: the list of ranked keywords
    """
    crawl_it = url_crawler(site_url)
    clean_it = url_cleaner(site_url, crawl_it)
    iterate_it = crawler_iterator(clean_it, 1)
    clean_data = url_cleaner(site_url, iterate_it)
    result = rank_iterator(clean_data)
    
    return result


def export_txt(data: list) -> None:
    with open('result.txt', 'a', encoding='utf-8') as f:
        f.write(data)


if __name__ == '__main__':
    url = 'https://www.azionadigitale.com'
    # print(orchestrator(url))
    # orchestrator(url)
    text_data = str(orchestrator(url))
    export_txt(text_data)
    