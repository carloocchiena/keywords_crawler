"""Managing and updating
   stop words list
"""

def stop_words_update() -> list:
    """Read from txt file and create a list of stopwords"""
    stop_words = ["!","'","£","$","%","&","(",")","?","^","*","+","/","-", '–', "©"]  #add further custom words to be excluded

    with open('stop_words.txt', 'rt', encoding='utf-8') as f:
        words = f.readlines()
        stop_words.extend(words)
        
    stop_words = [word.rstrip() for word in stop_words]
        
    return stop_words


if __name__ == '__main__':
    stop_words_update()
    