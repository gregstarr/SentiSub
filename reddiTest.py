from praw import Reddit
from nltk.sentiment.vader import SentimentIntensityAnalyzer

subreddit_name = 'science'

reddit = Reddit(client_id='N5kDJcWEEK7BDw', 
                client_secret='teB5Ykrjyh_ygkeGKk8mOrAyBRU', 
                password='fuckfuck77', 
                user_agent='whatever you want this to say?', 
                username='gregstarr')

subreddit = reddit.subreddit(subreddit_name).hot()
top_submission = reddit.submission(subreddit.next())

comments = []

top_submission.comments.replace_more(limit=0)
for top_level_comment in top_submission.comments:
    comments.append(top_level_comment.body)
    
sid = SentimentIntensityAnalyzer()

for comment in comments:
    print(comment)
    print(sid.polarity_scores(comment))
    print()