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
            
            canvas0, canvas1, canvas2 = reddit.plotTraffic()
            #canvas3 = reddit.plotSentiment()
            graphic0 = BytesIO()
            graphic1 = BytesIO()
            graphic2 = BytesIO()
            graphic3 = BytesIO()
            canvas0.print_png(graphic0)
            canvas1.print_png(graphic1)
            canvas2.print_png(graphic2)
            #canvas3.print_png(graphic3)
            graphic0 = b64encode(graphic0.getvalue())
            graphic1 = b64encode(graphic1.getvalue())
            graphic2 = b64encode(graphic2.getvalue())
            graphic3 = None# b64encode(graphic3.getvalue())
            context = {'graphic0':graphic0, 'graphic1':graphic1, 'graphic2':graphic2, 'graphic3':graphic3, 'form':form} 
            return render(request, 'sentiments/index.html', context)
        else:
            
            print(form)
            return HttpResponse("error?{0}".format(form.is_valid()))
            
    else:
        form = subredditForm()
        context = {'graphic':"",'form':form}

        return render(request,'sentiments/index.html',context)


