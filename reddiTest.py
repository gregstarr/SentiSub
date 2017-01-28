import praw

reddit = praw.Reddit(client_id='N5kDJcWEEK7BDw', client_secret='teB5Ykrjyh_ygkeGKk8mOrAyBRU', password='fuckfuck77', user_agent='whatever you want this to say?', username='gregstarr')

for submission in reddit.subreddit('programmingcirclejerk').hot(limit=25):
	print(submission.title)
	for comment in submission.comments:
		print(comment)
