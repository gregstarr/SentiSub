from praw import Reddit
from nltk.sentiment.vader import SentimentIntensityAnalyzer
from textblob import TextBlob
import matplotlib.pyplot as plt
plt.style.use('ggplot')
import numpy as np
from datetime import datetime
import matplotlib.dates as mdates
from matplotlib.backends.backend_agg import FigureCanvasAgg as FigureCanvas

"""
Hutto, C.J. & Gilbert, E.E. (2014). VADER: A Parsimonious Rule-based Model for Sentiment Analysis of Social Media Text. Eighth International Conference on Weblogs and Social Media (ICWSM-14). Ann Arbor, MI, June 2014.
"""

class RedditData():
    
    def __init__(self,subreddit_name,limit=30):
        
        self.reddit = Reddit(client_id='N5kDJcWEEK7BDw', 
                             client_secret='teB5Ykrjyh_ygkeGKk8mOrAyBRU', 
                             password='fuckfuck77', 
                             user_agent='SentiSub', 
                             username='gregstarr')
                             
        self.subreddit = self.reddit.subreddit(subreddit_name)
        self.getSubmissions(limit)
        
        self.dd,self.hd,self.md,self.dt,self.ht,self.mt = self.getTraffic()
        
    
    def getSubmissions(self,limit=1):
        self.submissions = []
        for submission in self.subreddit.top('month',limit=limit):
            if not submission.stickied:
                self.submissions.append(submission) 
        
    
    def grabComments(self):
        
        self.comments = []
        
        for s in self.submissions:
            print(s.title)
            s.comments.replace_more(limit=0)
            comment_queue = s.comments[:]  # Seed with top-level
            while comment_queue:
                comment = comment_queue.pop(0)
                self.comments.append(comment.body)
                comment_queue.extend(comment.replies)
            
    def analyzeComments(self):
        
        sid = SentimentIntensityAnalyzer()
    
        vader_data = np.empty((len(self.comments),4),float)
        self.tb_data = np.empty((len(self.comments),2),float)
    
        for comment in self.comments:
            i = self.comments.index(comment)
            tb = TextBlob(comment)
            self.tb_data[i,:] = tb.sentiment
            vader_data[i,:] = list(sid.polarity_scores(comment).values())
            
        self.tb_data = self.tb_data[:,0]
        self.vader_diff = vader_data[:,3]-vader_data[:,2]
        self.vader_comp = vader_data[:,1][np.isfinite(vader_data[:,1])]
        self.vader_diff = self.vader_diff[np.logical_and(self.vader_diff>=-1,self.vader_diff<=1)]
        self.tb_data = self.tb_data[np.logical_and(self.tb_data>=-1,self.tb_data<=1)]
                        
        print('{} comments analyzed'.format(len(comments)))

            
    def plotSentiment(self):
        
        fig = plt.figure()
        fig.suptitle('Sentiment')
        
        ax1 = fig.add_subplot(311)
        bins = np.arange(-1.05,1.05,.1)
        n,bins,patches = ax1.hist(self.tb_data,bins)
        ax1.set_xlim([-1,1])
        ax1.set_ylabel('TextBlob'.format(np.mean(self.tb_data)))
        
        ax2 = fig.add_subplot(312)
        ax2.hist(self.vader_diff,bins)
        ax2.set_ylabel('NLTK Difference'.format(np.mean(self.vader_diff)))
        plt.set_xlim([-1,1])
        
        ax3 = fig.add_subplot(313)
        ax3.hist(self.vader_comp,bins)
        ax3.set_ylabel('NLTK Compound'.format(np.mean(self.vader_comp)))
        ax3.set_xlim([-1,1])
        
        return FigureCanvas(fig)    
        
        
    def getTraffic(self):
        """
        day - [epoch time, uniques, pageviews, subscriptions]
        hour and month - [epoch time, uniques, pageviews]
        """
        
        traffic_data = self.subreddit.traffic()
        day_data = np.array(traffic_data['day'])
        hour_data = np.array(traffic_data['hour'])
        month_data = np.array(traffic_data['month'])
        
        day_times = np.array([datetime.fromtimestamp(timestamp) for timestamp in day_data[:,0]])
        month_times = np.array([datetime.fromtimestamp(timestamp) for timestamp in month_data[:,0]])
        hour_times = np.array([datetime.fromtimestamp(timestamp) for timestamp in hour_data[:,0]])
        
        return day_data[:,1:],hour_data[:,1:],month_data[:,1:],day_times,hour_times,month_times
        
    def plotTraffic(self):
        
        day_fig = plt.figure()
        day_fig.suptitle('Daily')
        ax1 = day_fig.add_subplot(311)
        ax1.plot(self.dt,self.dd[:,0])
        ax1.set_ylabel('Unique Visits')
        
        ax2 = day_fig.add_subplot(312,sharex=ax1)
        ax2.plot(self.dt,self.dd[:,1])
        ax2.set_ylabel('Pageviews')
        
        ax3 = day_fig.add_subplot(313,sharex=ax1)
        ax3.plot(self.dt,self.dd[:,2])
        ax3.set_ylabel('Subscribers')
        
        day_fig.autofmt_xdate()    
        
        
        hour_fig = plt.figure()
        hour_fig.suptitle('Hourly')
    
        hour_fmt = mdates.DateFormatter('%b %d %I:%M %p')
        ax1 = hour_fig.add_subplot(211)
        ax1.plot(self.ht,self.hd[:,0])
        ax1.set_ylabel('Unique Visits')
        ax1.xaxis.set_major_formatter(hour_fmt)
        
        ax2 = hour_fig.add_subplot(212,sharex=ax1)
        ax2.plot(self.ht,self.hd[:,1])
        ax2.set_ylabel('Pageviews')
    
        hour_fig.autofmt_xdate()    
        
        
        month_fig = plt.figure()
        month_fig.suptitle('Monthly')
    
        ax1 = month_fig.add_subplot(211)
        ax1.plot(self.mt,self.md[:,0])
        ax1.set_ylabel('Unique Visits')
    
        ax2 = month_fig.add_subplot(212,sharex=ax1)
        ax2.plot(self.mt,self.md[:,1])
        ax2.set_ylabel('Pageviews')
    
        month_fig.autofmt_xdate() 
        
        return FigureCanvas(day_fig),FigureCanvas(hour_fig),FigureCanvas(month_fig)
