
# coding: utf-8

# In[2]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[3]:


# Visit hackernews and store it in variable doc
response = requests.get('https://news.ycombinator.com/')
doc = BeautifulSoup(response.text, 'html.parser')


# In[4]:


# Find the table with each post
posts = doc.find(class_="itemlist").findAll('tr')
list_of_stories = []
# Scrape specific info
for post in posts:
    post_dict={}
    try:
        post_dict['headline'] = post.find(class_='storylink').text
    except:
        pass
    try:
        post_dict['link'] = post.find(class_='storylink')['href']
    except:
        pass
    try:
        post_dict['user'] = post.find(class_='hnuser').text
    except:
        pass
    try:
        post_dict['points'] = post.find(class_='subtext').span.text
    except:
        pass
    #Drop empty cells before appending to full list_of_stories
    if len(post_dict) > 0:
        list_of_stories.append(post_dict)
            


# In[5]:


# This dataframe is complete, but messy. Odd lines need to be joined with the next
# line and dupes need to be removed.
df = pd.DataFrame(list_of_stories)
# df.head()


# In[6]:


# make a new DF with just the headlines and links and forward fill the NaN values
df_headlines = df[['headline', 'link']].ffill()
# Make a new DF with just the points and users and backfill the NaN values
df_users = df[['points', 'user']].bfill()
# Drop the dupes from both our new data frams
df_users = df_users.drop_duplicates()
df_headlines = df_headlines.drop_duplicates()
# Join the cleaned DF
df_complete = df_headlines.join(df_users)


# In[7]:


import datetime
right_now = datetime.datetime.now()
# right_now.strftime("%Y-%m-%d-%-I%p")


# In[9]:


filename = "briefing" + right_now.strftime("%Y-%m-%d-%-I%p") + ".csv"
df_complete.to_csv(filename, index = False)


# In[10]:


email_subject = "Here is your " + right_now.strftime('%-I %p') +" briefing"


# In[11]:



requests.post(
    "https://api.mailgun.net/v3/*********/messages",
    auth=("api", "********"),
    files=[("attachment", open(filename))],
    data={"from": "M Albasi <*****>",
          "to": ["M Albasi <*****>"],
          "subject": email_subject,
          "text": email_subject}) 

