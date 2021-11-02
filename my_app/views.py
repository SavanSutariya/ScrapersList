import requests as req
from django.shortcuts import render
from requests import models
from requests.compat import quote_plus
from bs4 import BeautifulSoup
from .models import Search
# Create your views here
BASE_CRAIGSLIST_URL = 'https://losangeles.craigslist.org/search/?query={}'
def home(request):
    return render(request, 'base.html')

def new_search(request):
    query = request.POST.get('query')
    # Search.objects.create(search=query)
    final_url = BASE_CRAIGSLIST_URL.format(quote_plus(query))
    data = req.get(final_url).text
    soup = BeautifulSoup(data, features='html.parser')

    post_list = soup.find_all('li', {'class' : 'result-row'})

    final_posts = []
    for post in post_list:
        post_title = post.find(class_= 'result-title').text
        post_url = post.find(class_= 'result-title').get('href')
        if post.find(class_='result-price'):
            post_price = post.find(class_='result-price').text
        else:
            post_price = 'N/A'
        print(f"Title: {post_title} \n Price: {post_price}") 
        final_posts.append((post_title, post_url, post_price)) 

    stuff_for_frontend = {
        'search': query,
        'final_posts': final_posts,
        }
    return render(request,'my_app/new_search.html',stuff_for_frontend)