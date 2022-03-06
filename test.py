import requests
from bs4 import BeautifulSoup
from random import random, randint
url ='https://www.google.ru/search?q=money&tbm=isch&ictx=1&tbs=rimg:CSdUhsaQ8wnAIggnVIbGkPMJwCoSCSdUhsaQ8wnAER51_1OfmHnKU&hl=ru&sa=X&ved=2ahUKEwjQwvDJurH2AhUE7xoKHTYlCyIQiRx6BAgAEAQ&biw=1519&bih=722'
response = requests.get(url)
soup = BeautifulSoup(response.text, features="html.parser")
images = []
for img in soup.findAll('img'):
    images.append(img.get('src'))

print(images[randint(1, 10)])

