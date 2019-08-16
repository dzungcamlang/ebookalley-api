import requests
from bs4 import BeautifulSoup
import json
import re
import itertools


def get_books_arr(book_name):
    def get_dpage_link(link):
        part = re.findall(r'(-e[0-9]\d+)', link)[0]
        new_link = ''
        for x,i in enumerate(link):
            if x == link.find(part)+1:
                i = 'd'
            new_link += i
        return new_link
        
    BASE_URL = 'https://pdfdrive.com'
    url = f'https://www.pdfdrive.com/search?q={book_name}'

    res = requests.get(url)

    soup = BeautifulSoup(res.text, 'html.parser')

    #book primary data list
    books_arr_1 = soup.find_all('div',{'class':'file-left'})

    #book info list
    books_arr_2 = soup.find_all('div',{'class':'file-info'})

    #book_link_object
    book_links = []

    #looping over both lists : 
    #book arr 1
    #book arr 2
    for v1, v2 in zip(books_arr_1, books_arr_2):
        #getting first set of data
        link = v1.find('a')['href']
        if link[0] is '/':
            link = BASE_URL + link
        book_url = get_dpage_link(link)
        book_thumb = v1.find('img')['src']
        book_name = v1.find('img')['alt']

        #getting second set of data

        book_year = v2.findAll('span',{'class':'fi-year'})[0].text 

        #extracting book pages number
        book_pages = v2.findAll('span',{'class':'fi-pagecount'})[0].text
        book_pages = re.findall(r'\d+', book_pages)[0]
        
        #extracting book downloads number
        book_downloads = v2.findAll('span',{'class':'fi-hit'})[0].text
        book_downloads = re.findall(r'\d+', book_downloads)
        book_downloads = ''.join(book_downloads)

        book_links.append({
            'name':book_name,
            'link':book_url,
            'img':book_thumb,
            'year':book_year,
            'pages':book_pages,
            'downloads':book_downloads
            })
        
    return book_links

#method to get final url
def get_book_url(base_url):
    #custom replace function
    def quot_replace(string):
        new_string = ''
        for x,i in enumerate(string):
            if i is "'":
                new_string += '"'
            else:
                new_string += i
        return new_string
    #inner method to get file url
    def get_file_url(book_url):
        res = requests.get(book_url)
        soup = BeautifulSoup(res.text, 'html.parser')
        url = soup.find('a')['href']
        BASE_URL = 'https://pdfdrive.com'
        if '/download' in url:
            url = BASE_URL + url
        obj = {'url':url}
        return obj
        
    res = requests.get(base_url)
    if '{id:' in res.text:
        index = res.text.index('/ebook/broken')
        start = res.text[index+15:index+100]
        end = start.index(').d')
        string = start[:end]
        string = string.replace('id','"id"').replace('session','"session"').replace('r','"r"')
        string = quot_replace(string)
        data = json.loads(string)
        book_url = f"https://www.pdfdrive.com/ebook/broken?id={data['id']}&session={data['session']}&r={data['r']}"
        return get_file_url(book_url)
    