from bs4 import BeautifulSoup
import requests
import csv
import os

chosen_dir = input('Enter the path to the folder where you would like your files saved:')

while True:
    try:
        os.chdir(chosen_dir)
        if not os.path.exists(chosen_dir+'\MovieFrameshots'):
            os.mkdir(chosen_dir+'\MovieFrameshots')
        break
    except OSError:
        print("The folder you chose doesn't exist or is incorrectly typed. Check if you typed the path correctly and try again")
    chosen_dir = input('Enter the path to the folder where you would like your files saved:')

response = requests.get('https://www.timeout.com/film/best-movies-of-all-time')
soup = BeautifulSoup(response.text, 'html.parser')

movie_titles_split_lists = [movie_title.text.split() for movie_title in soup.find_all('h3', attrs={'data-testid':'tile-title_testID'})]

movie_titles = []
movie_release_years = []

for movie_title_split_list in movie_titles_split_lists:
    title = ' '.join(movie_title_split_list[1:-1])
    movie_titles.append(title)
    movie_release_years.append(movie_title_split_list[-1].replace('(', '').replace(')', ''))
del movie_release_years[-1]
del movie_titles[-1] 

movie_links_html = soup.find_all('a', attrs={'data-testid':'tile-link_testID'})

movie_links = []
base_url = 'https://www.timeout.com'

for i in range(len(movie_links_html)):
    if i%2 == 0:
        if movie_links_html[i]['href'] == '/movies':
            movie_links.append('-')
        else:
            movie_links.append(base_url + movie_links_html[i]['href'])
del movie_links[-1]

durations_list = []
for movie_url in movie_links:
    if movie_url == '-':
        durations_list.append('-')
    else:
        try:
            movie_response = requests.get(movie_url)
            movie_soup = BeautifulSoup(movie_response.text, 'html.parser')
            duration = movie_soup.find('ul', attrs={'class':'_list_sygug_16'}).text.split(':')[-1]
            if ' mins' in duration:
                durations_list.append(duration)
            else:
                durations_list.append('-')
        except:
            durations_list.append('-')

article_list = soup.find_all('article')[:100]
image_url_list = []
for article in article_list:
    article_links = article.find_all('a', attrs={'data-testid':'tile-link_testID'})
    found_images = False
    for article_link in article_links:
        if '/movies' in article_link['href']:
            images = article.find_all('img')
            if images:
                found_images = True
                for image in images:
                    if image['src'] not in image_url_list:
                        image_url_list.append(image['src'])
    if not found_images:
        image_url_list.append('-')

file = open('100 best movies of all time.csv', 'w', newline='')
writer = csv.writer(file)
writer.writerow(['Number', 'Title', 'Release year', 'Duration', 'Blurb'])

number_column = [i+1 for i in range(len(image_url_list))]
for num, title, release_year, duration, blurb in zip(number_column, movie_titles, movie_release_years, durations_list, movie_links):
    writer.writerow([num, title, release_year, duration, blurb])
file.close()

already_saved_images = []
os.chdir(chosen_dir+'\MovieFrameshots')
for image_url in image_url_list:
    if image_url == '-':
        continue
    else:
        image = requests.get(image_url)
        image_name = str(image_url_list.index(image_url)+1) + '. ' + movie_titles[image_url_list.index(image_url)] + '.jpg'
        if image_url in already_saved_images:
            image_name = image_name + str(already_saved_images.count(image_url))
        if ':' in image_name:
            image_name = image_name.replace(':', '')
        with open(image_name, 'wb') as file:
            file.write(image.content)
            already_saved_images.append(image_url)
