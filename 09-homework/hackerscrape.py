
# coding: utf-8

# In[1]:


import requests
from bs4 import BeautifulSoup
import pandas as pd


# In[9]:


response = requests.get('https://news.ycombinator.com/')
doc = BeautifulSoup(response.text, 'html.parser')


# In[115]:


posts = doc.find(class_="itemlist").findAll('tr')
list_of_stories = []

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
    if len(post_dict) > 0:
        list_of_stories.append(post_dict)
        
        


# In[116]:


print(list_of_stories)


# In[117]:


df = pd.DataFrame(list_of_stories)
df.head()


# In[130]:


import datetime
right_now = datetime.datetime.now()
right_now.strftime("%Y-%m-%d-%-I%p")


# In[125]:


filename = "briefing" + right_now.strftime("%Y-%m-%d-%-I%p") + ".csv"
df.to_csv(filename, index = False)


# In[133]:


email_subject = "Here is your " + right_now.strftime('%-I %p') +" briefing"
print(email_subject)


# In[136]:



requests.post(
    "https://api.mailgun.net/v3/*******/messages",
    auth=("api", "*****"),
    files=[("attachment", open(filename))],
    data={"from": "M Albasi <mda2160@columbia.edu>",
          "to": ["M Albasi <mda2160@columbia.edu>"],
          "subject": email_subject,
          "text": email_subject}) 

