#!/usr/bin/env python
# coding: utf-8

# In[1]:


import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import plotly.graph_objects as go
import plotly.express as px


# In[2]:


#st.title('Blogpost Formula 1 (2010-2021)')


# In[3]:


seasons = ['2010', '2011', '2012','2013', '2014', '2015','2016', '2017', '2018','2019','2020','2021']
races_df = pd.DataFrame()

for season in seasons:
   r = requests.get("http://ergast.com/api/f1/{}/results/.json?limit=450".format(season))
   data=r.json()
   #Normalize F1 race data
   races = pd.json_normalize(data['MRData']['RaceTable']['Races'])
   races_df = races_df.append(races)


# In[18]:


#Iterate race by race and append the results to the list
results = []
for index, race in races_df.iterrows():
    race_data = pd.json_normalize(race['Results'])
    for index, row in race_data.iterrows():
        results.append((race['round'], 
                        race['raceName'],
                        race['season'],
                        race['Circuit.Location.country'], 
                        row['laps'], 
                        row['grid'],
                        row['position'],
                        row['Time.millis'],
                        row['status'],
                        row['Constructor.name'],
                       (row['Driver.givenName']+' '+ row['Driver.familyName']),
                        row['Driver.dateOfBirth'],
                        row['Driver.nationality']
                       )
                      )


# In[19]:


#Create results_df Dataframe
column_names = ['Race_Id',
                'Race_Name',
                'Season',
                'Country',
                'Laps',
                'Grid',
                'Position',
                'Time_(ms)',
                'Status',
                'Team',
                'Driver_Name',
                'Driver_Date_Of_Birth',
                'Driver_Nationality',
               ]
results_df = pd.DataFrame(results, columns = column_names)


# In[20]:


#Convert datatpyes
convert_dict = {
    'Race_Id' : int,
    'Race_Name' : str,
    'Season' : str,
    'Country' : str,
    'Laps' : int,
    'Grid' : str,
    'Position' : int,
    'Time_(ms)': str,
    'Status' : str,
    'Team' : str,
    'Driver_Name' : str,
    'Driver_Date_Of_Birth' : str,
    'Driver_Nationality' : str,            
}
results_df = results_df.astype(convert_dict)


# In[21]:


results_df.head()


# In[22]:





# In[23]:


results_df.shape


# In[24]:


results_df.dtypes


# In[25]:


results_df.info()


# In[26]:


results_df.isnull().sum()


# In[27]:


results_df.nunique(axis=0)


# In[28]:


results_df.describe()


# In[29]:



won_total = results_df[results_df['Position'] == 1]['Team'].value_counts()
dfwontotal = pd.DataFrame([won_total])
dfwontotal



# In[30]:


df_slider = results_df[results_df['Position'] == 1]



# Create the basic figure
fig = go.Figure()



# Loop through the states
for season in seasons:
    # Subset the DataFrame
    df = df_slider[df_slider.Season == season]
    # Add a trace for each season
    fig.add_trace(go.Histogram(x=df["Team"], name=season))



for i in [1, 2, 3 , 4, 5, 6, 7, 8, 9, 10 ,11]:
    fig.data[i].visible = False



# Create the slider elements
sliders = [{'steps':[
{'method': 'update', 'label': '2010', 'args': [{'visible': [True, False, False, False, False, False, False, False, False, False, False, False]}]},
{'method': 'update', 'label': '2011', 'args': [{'visible': [False, True, False, False, False, False, False, False, False, False, False, False]}]},
{'method': 'update', 'label': '2012', 'args': [{'visible': [False, False, True, False, False, False, False, False, False, False, False, False]}]},
{'method': 'update', 'label': '2013', 'args': [{'visible': [False, False, False, True, False, False, False, False, False, False, False, False]}]},
{'method': 'update', 'label': '2014', 'args': [{'visible': [False, False, False, False, True, False, False, False, False, False, False, False]}]},
{'method': 'update', 'label': '2015', 'args': [{'visible': [False, False, False, False, False, True, False, False, False, False, False, False]}]},
{'method': 'update', 'label': '2016', 'args': [{'visible': [False, False, False, False, False, False, True, False, False, False, False, False]}]},
{'method': 'update', 'label': '2017', 'args': [{'visible': [False, False, False, False, False, False, False, True, False, False, False, False]}]},
{'method': 'update', 'label': '2018', 'args': [{'visible': [False, False, False, False, False, False, False, False, True, False, False, False]}]},
{'method': 'update', 'label': '2019', 'args': [{'visible': [False, False, False, False, False, False, False, False, False, True, False, False]}]},
{'method': 'update', 'label': '2020', 'args': [{'visible': [False, False, False, False, False, False, False, False, False, False, True, False]}]},
{'method': 'update', 'label': '2021', 'args': [{'visible': [False, False, False, False, False, False, False, False, False, False, False, True]}]}]}]





# Update the figure to add sliders and show
fig.update_layout({'sliders': sliders}, xaxis_title_text='Teams', yaxis_title_text='Wins', title='Grand Prix Wins Per Team (2010-2021)')
# Show the plot
fig.show()


# In[31]:


fig = go.Figure()

for team in ['Ferrari','McLaren','Red Bull', 'Mercedes','Williams','Lotus F1', 'AlphaTauri', 'Racing Point', 'Alpine F1 Team']:
    df = results_df[results_df['Team'] == team]
    df_1 = df[df['Position'] == 1] 
    fig.add_trace(go.Scattergeo(
        locations = df_1['Country'],
        locationmode = 'country names',
        name = team, 
        opacity = 0.7
    )
)
dropdown_buttons = [
    {'label' :'All Teams', 'method': 'update',
     'args': [{'visible': [True,True,True,True,True,True,True,True,True]},
             {'title':'Grand Prix Win Locations Per Team (2010-2021)'}]},
    {'label' :'Ferrari', 'method': 'update',
     'args': [{'visible': [True,False,False,False,False,False,False,False,False]},
             {'title':'Ferrari Grand Prix Win Locations (2010-2021)'}]},
    {'label' : 'McLaren', 'method': 'update',
     'args': [{'visible': [False,True,False,False,False,False,False,False,False]},
             {'title':'McLaren Grand Prix Win Locations (2010-2021)'}]},
    {'label' : 'Red Bull', 'method': 'update',
     'args': [{'visible': [False,False,True,False,False,False,False,False,False]},
             {'title':'Red Bull Grand Prix Win Locations (2010-2021)'}]},
    {'label' : 'Mercedes', 'method': 'update',
     'args': [{'visible': [False,False,False,True,False,False,False,False,False]},
             {'title':'Mercedes Grand Prix Win Locations (2010-2021)'}]},
    {'label' : 'Williams', 'method': 'update',
     'args': [{'visible': [False,False,False,False,True,False,False,False,False]},
             {'title':'Williams Grand Prix Win Locations (2010-2021)'}]},
    {'label' : 'Lotus F1', 'method': 'update',
     'args': [{'visible': [False,False,False,False,False,True,False,False,False]},
             {'title':'Lotus F1 Grand Prix Win Locations (2010-2021)'}]},
    {'label' : 'AlphaTauri', 'method': 'update',
     'args': [{'visible': [False,False,False,False,False,False,True,False,False]},
             {'title':'AlphaTauri Grand Prix Win Locations (2010-2021)'}]},
    {'label' : 'Racing Point', 'method': 'update',
     'args': [{'visible': [False,False,False,False,False,False,False,True,False]},
             {'title':'Racing Point Grand Prix Win Locations (2010-2021)'}]},
    {'label' : 'Alpine F1 Team', 'method': 'update',
     'args': [{'visible': [False,False,False,False,False,False,False,False,True]},
             {'tile':'Alpine F1 Team Grand Prix Win Locations (2010-2021)'}]}
    ]


fig.update_layout({
    'updatemenus':[{
        'type': 'dropdown',
        'x' : 1.2,
        'y' : 0.4,
        'showactive': True,
        'active' : 0,
        'buttons': dropdown_buttons
    }],
    'title': 
    {'text': 'Grand Prix Win Locations Per Team (2010-2021)',
      'x': 0.45, 
      'y': 0.9}
     
    
})


# In[ ]:





# In[ ]:




