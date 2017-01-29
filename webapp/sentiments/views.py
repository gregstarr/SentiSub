from django.shortcuts import render
from django.http import HttpResponse
from .models import SubReddit
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

def index(request):
    try:
        query = SubReddit.objects.get(subreddit_name="asdf")
    except ObjectDoesNotExist:
        return HttpResponse("That subreddit doesn't exist")
    print(query)
    return HttpResponse("Hola.")

def getCharts(requrest, subredditName):
    try:
        query = SubReddit.objects.get(subreddit_name=subredditName)
    except DoesNotExist:
        #Find subreddit and get info using Greg info
        return HttpResponse("That subreddit doesn't exist")
    #Display info based on table-data
    print(query)
    #If Fancy: Create CSV and serve it up to a js handler
    #else: Serve up a png/image to the div
