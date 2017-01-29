from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import SubReddit
from django.core.exceptions import ObjectDoesNotExist
from .forms import subredditForm
from .reddiTest import RedditData
from io import BytesIO
from base64 import b64encode

# Create your views here.

def index(request):
    try:
        subreddit_list = SubReddit.objects.get(subreddit_name="funny")
        form= subredditForm()
        context = {"graphic": "", "form":form} 
        return render(request, 'sentiments/index.html', context)

    except ObjectDoesNotExist:
        HttpResponse("template.render(context())")
    


def inputSubReddit(request):
    if request.method == 'POST':
        form = subredditForm(request.POST)

        if form.is_valid():
            subredditName = form.cleaned_data['subredditName']
            
            reddit = RedditData(subredditName)
            
            canvas = reddit.plotTraffic()[0]
            graphic = BytesIO()
            canvas.print_png(graphic)
            print(canvas)
            print(graphic)              
            return render(request, 'sentiments/index.html', {'graphic':b64encode(graphic.getvalue()), 'form':form})
            #respons= HttpResponse(content_type='image/png')
            #canvas.print_png(respons)            
            #return respons
        else:
            
            print(form)
            return HttpResponse("error?{0}".format(form.is_valid()))
            
    else:
        form = subredditForm()
        context = {'graphic':"",'form':form}

        return render(request,'sentiments/index.html',context)


