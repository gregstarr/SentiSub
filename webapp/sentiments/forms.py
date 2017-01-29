from django import forms

class subredditForm(forms.Form):
        subredditName = forms.CharField(label="Input the name of a subreddit (exclude  /r/)", max_length=20)
