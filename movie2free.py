#!/bin/python
# -*- coding: utf-8 -*-
# author: bii811


from bs4 import BeautifulSoup
import urllib.request
import urllib.parse
import re
from datetime import datetime


#get menu list
#data = urllib.request.urlopen(url).read().decode('utf-8')
#menu = {}
#for item in BeautifulSoup(data, 'html.parser').find_all('li', class_='menu-item'):
#    item_a = item.a.extract()
#    menu[item_a.string] = item_a.get('href')
#    lkeys = list(menu.keys())
#    lvalues = list(menu.values())

url = 'https://www.movie2free.com'

def re_search(pattern, text):
    m = re.search(pattern, text)
    if m:
        return str(m.group(1))
    else:
        return 'N/A'


def getWatchMovieLink(url):
    r = urllib.request.urlopen(url)
    data = r.read().decode('utf-8')

    m = re.search('create\("(.*?)"', data)
    if m:
        data = urllib.request.urlopen(m.group(1)).read().decode('utf-8')
        m = re.search('"url":"(.*?)"', data)
        if m:
            return str(m.group(1))


def downloadReport(block_count, block_size, total_size):
    if block_count == 0:
        print('block_count == 0.')

    if (block_count * block_size) == total_size:
        print('Download finished.')
    
    percent = float(block_count * block_size * 100 / total_size)
    print("Downloading... {}/{}/{} {:.2f}% complete.".format(block_count, block_size, total_size, percent), end='\r')


def Download(url, filename):
    urllib.request.urlretrieve(url, filename, reporthook=downloadReport)


while(1):
    print('=== Menu ===')
    category_list = {'Top IMDb': 'https://www.movie2free.com/top-imdb/',
                         'Asia': 'https://www.movie2free.com/category/%e0%b8%ab%e0%b8%99%e0%b8%b1%e0%b8%87%e0%b9%80%e0%b8%ad%e0%b9%80%e0%b8%8a%e0%b8%b5%e0%b8%a2/',
                         'Series': 'https://www.movie2free.com/category/%e0%b8%ab%e0%b8%99%e0%b8%b1%e0%b8%87%e0%b8%a0%e0%b8%b2%e0%b8%84%e0%b8%95%e0%b9%88%e0%b8%ad/',
                         'Cartoon': 'https://www.movie2free.com/category/%e0%b8%ab%e0%b8%99%e0%b8%b1%e0%b8%87%e0%b8%81%e0%b8%b2%e0%b8%a3%e0%b9%8c%e0%b8%95%e0%b8%b9%e0%b8%99/',
                         'New': 'https://www.movie2free.com/category/%e0%b8%ab%e0%b8%99%e0%b8%b1%e0%b8%87%e0%b8%ad%e0%b8%ad%e0%b8%81%e0%b9%83%e0%b8%ab%e0%b8%a1%e0%b9%88/',
                         'Home': 'https://www.movie2free.com',
                         'Inter': 'https://www.movie2free.com/category/%e0%b8%ab%e0%b8%99%e0%b8%b1%e0%b8%87%e0%b8%9d%e0%b8%a3%e0%b8%b1%e0%b9%88%e0%b8%87/',
                         'Cartoon Series': 'https://www.movie2free.com/category/%e0%b8%81%e0%b8%b2%e0%b8%a3%e0%b9%8c%e0%b8%95%e0%b8%b9%e0%b8%99%e0%b8%a0%e0%b8%b2%e0%b8%84%e0%b8%95%e0%b9%88%e0%b8%ad/',
                         'Hit': 'https://www.movie2free.com/%e0%b8%84%e0%b8%99%e0%b8%8a%e0%b8%ad%e0%b8%9a%e0%b8%a1%e0%b8%b2%e0%b8%81%e0%b8%97%e0%b8%b5%e0%b9%88%e0%b8%aa%e0%b8%b8%e0%b8%94/'}    

    cl_keys = sorted([str(i) for i in category_list])
    count = 0
    for c in cl_keys:
        print(str(count) + '. '+ c)
        count += 1

    choice = input("Choice: ")
    if choice.isdigit():
        category_name = str(cl_keys[int(choice)])
        url = category_list[category_name]

        #get list movie
        #url = r'https://www.movie2free.com/'
        #url = urllib.parse.quote(url, safe='/:')
        
        r = urllib.request.urlopen(url).read().decode('utf-8')
        soup = BeautifulSoup(r, 'html.parser')
        
        movie_list = [movie.a.extract().get('href') for movie in soup.find_all('div', class_='moviefilm')]
        movie_dict = {re_search('movie2free.com/(.*?)-%', m):m for m in movie_list}

        count = 0
        choices = []
        print('\n===', category_name, 'Movie List ===')
        for k in movie_dict:
            print(str(count) + '. ' + k)
            choices.append(k)
            count += 1

        choice_selected = input("Choice: ")
        movie_title = str(choices[int(choice_selected)])
        if choice.isdigit():
            movie_link = getWatchMovieLink(str(movie_dict[movie_title]))

        confirm_download = input("Do you want to download it? (y/n): ")
        if confirm_download == 'y':
            print('\n', movie_title, "is downloading...")
            file_name = str(datetime.strptime(str(datetime.now()), '%Y-%m-%d %H:%M:%S.%f').strftime('%Y-%m-%d-%H%M%S')) + '-' + movie_title + '.mp4'
            Download(movie_link, file_name)
            print(file_name, "is downloaded.")
        else:
            print(movie_link)

        print()
        c = input('Press any key to continue...')
