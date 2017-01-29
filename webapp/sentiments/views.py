from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import SubReddit
from django.core.exceptions import ObjectDoesNotExist


# Create your views here.

def index(request):
    try:
        subreddit_list = SubReddit.objects.get(subreddit_name="funny")
        context = {"list": subreddit_list} 
        return render(request, 'sentiments/index.html', context)

    except ObjectDoesNotExist:
        HttpResponse("template.render(context())")
    


def getCharts(requrest, subredditName):
    # try:
        # query = SubReddit.objects.get(subredadit_name=subredditName)
    # except DoesNotExist:
        #Find subreddit and get info using Greg info
    return HttpResponse("That subreddit doesn't exist")
    #Display info based on table-data
    #If Fancy: Create CSV and serve it up to a js handler
    #else: Serve up a png/image to the div