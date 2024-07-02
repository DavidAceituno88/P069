#!/usr/bin/env python
# coding: utf-8

# # Title: Exploratory Data Analysis of PO69 Phase 3 
# ## Author: David Linares
# ## Date: 05-31-2024

# ### Objectives
# #### 1. Compare the duration and human hours cost of each task 
# 
# #### 2. Analyze any overlap between tasks
#     - Detect any overlap between tasks to identify "peak weeks" 

# In[16]:


import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px


# In[17]:


foundation_df = pd.read_excel('foundationtbl.xlsx')
groundwork_df = pd.read_excel('groundwrk_tbl.xlsx')
framing_df = pd.read_excel('framing_tbl.xlsx')
cs_df = pd.read_excel('cladding_siding_windows_doors_tbl.xlsx')
roofing_df = pd.read_excel('roofing_tbl.xlsx')


# In[18]:


def convert_to_hour(time_str):
    if isinstance(time_str, str):
        try:
            time_format = "%H:%M"
            time_obj = datetime.strptime(time_str, time_format)
            return time_obj.hour
        except ValueError:
            return None  # or any other value you prefer for invalid inputs
    else:
        return None 
foundation_df['hour_column'] = foundation_df['Hours'].apply(convert_to_hour)
groundwork_df['hour_column'] = groundwork_df['Hours'].apply(convert_to_hour)
framing_df['hour_column'] = framing_df['Hours'].apply(convert_to_hour)
cs_df['hour_column'] = cs_df['Hours'].apply(convert_to_hour)
roofing_df['hour_column'] = roofing_df['Hours'].apply(convert_to_hour)


# In[19]:


#drop empty hours
# foundation_df = foundation_df[foundation_df['hour_column']!=0]
# groundwork_df = groundwork_df[groundwork_df['hour_column']!=0]
# framing_df = framing_df[framing_df['hour_column']!=0]
# cs_df = cs_df[cs_df['hour_column']!=0]
# roofing_df = roofing_df[roofing_df['hour_column']!=0]


# ### 1. Compare the duration and human hours cost

#    #### <center>Phase 3 table <center>

# In[20]:


dataframes= [
    (foundation_df,'Foundation'),
    (groundwork_df,'Groundwork'),
    (framing_df,'Framing'),
    (cs_df,'Cladding/Siding'),
    (roofing_df,'Roofing')
]

phase3 = []

for df,phase in dataframes:
    total_hours = df['hour_column'].sum()
    df['date_clean'] = pd.to_datetime(df['Date'], errors='coerce')
    df['week'] = df['date_clean'].dt.strftime('%Y-%U')
    
    start_date = df['date_clean'].min()
    end_date = df['date_clean'].max()
   
    
    weeks = len(set(df['week']))
    phase3.append({'Phase':phase , 'Hours' : total_hours,'Weeks':weeks,'Start Date': start_date, 'End Date': end_date})

phase3_df = pd.DataFrame(phase3)
phase3_df = phase3_df.sort_values(by='Start Date')
phase3_df.style


# ### <center>Tasks weeks duration proportion to human hours cost<center>

# In[21]:


#Plot
# Set the seaborn style
sns.set(style="whitegrid")

# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(9, 7))

# Plot the bar chart on ax1
sns.barplot(x='Phase', y='Hours', data=phase3_df, ax=ax1, color='b', alpha=0.6)

# Set labels for the first y-axis
ax1.set_ylabel('Total Hours', color='b')
ax1.set_xlabel('Phase')
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=45)

# Create a second y-axis to plot the weeks
ax2 = ax1.twinx()
ax2.plot(phase3_df['Phase'], phase3_df['Weeks'], color='r', marker='o', linewidth=2)

# Set labels for the second y-axis
ax2.set_ylabel('Weeks', color='r')

# Show the plot
plt.title('Total Hours and Weeks by Phase')
plt.show()


# 1. We can observe that the human hour cost is proportional to the number of weeks that it took to complete the task, except for roofing where the week proportion to human hours was higher <br>
# 2. Framing was the most expensive task in Human Hours followed by Cladding/Siding<br><br>

# In[22]:


# Aggregating the data by weeks (calculating the sum of hours per week)
groundwork_agg = groundwork_df.groupby('week')['hour_column'].sum().reset_index()
foundation_agg = foundation_df.groupby('week')['hour_column'].sum().reset_index()
framing_agg = framing_df.groupby('week')['hour_column'].sum().reset_index()
cs_agg = cs_df.groupby('week')['hour_column'].sum().reset_index()
roofing_agg = roofing_df.groupby('week')['hour_column'].sum().reset_index()


groundwork_tdf = pd.DataFrame(groundwork_agg)
foundation_tdf = pd.DataFrame(foundation_agg)
framing_tdf = pd.DataFrame(framing_agg)
cs_tdf = pd.DataFrame(cs_agg)
roofing_tdf = pd.DataFrame(roofing_agg)


# ### 2. Analyze any overlap between tasks
# 
# #### Human Hours per Week by Tasks and Overlapping
# 
# The graph below illustrates the allocation of human hours per week across various tasks, along with an indication of whether tasks overlap with each other.
# 

# In[23]:


plt.figure(figsize=(15,7))
plt.hist(foundation_tdf['week'], weights=foundation_tdf['hour_column'], 
         bins = 50,
         alpha=0.5, 
         label='Foundation')
plt.hist(groundwork_tdf['week'], weights=groundwork_tdf['hour_column'], 
         bins = 50,
         alpha=0.5, 
         label='Groundwork')
plt.hist(framing_tdf['week'], weights=framing_tdf['hour_column'], 
         bins = 50,
         alpha=0.5, 
         label='Framing')
plt.hist(roofing_tdf['week'], weights=roofing_tdf['hour_column'], 
         bins = 50,
         alpha=0.5, 
         label='Roofing') 

plt.hist(cs_tdf['week'], weights=cs_tdf['hour_column'], 
         bins = 50,
         alpha=0.5, 
         label='Cladding/Siding')

plt.xticks(rotation=90)

plt.legend(loc='upper right') 
plt.ylabel('Human hours')
plt.xlabel('Weeks')
plt.title('Overlapping Phase 3 Tasks',fontsize=16) 
plt.show()


# #### Observation:
# 
# In reviewing the graph, it's evident that numerous overlaps occur, <b>particularly notable among framing, roofing, and cladding/siding tasks</b>. These three activities seem to intertwine significantly within the schedule, suggesting a high degree of interdependence or shared resource utilization.
# 
# Next, we will delve deeper into each overlap individually to better understand their implications and potential areas for optimization.

# -------------------------------------------------------------------------------------------------------------------------

# In[24]:


#Plot task histogram

# Aggregating the data by weeks (calculating the sum of hours per week)
groundwork_agg = groundwork_df.groupby('week')['hour_column'].sum().reset_index()
foundation_agg = foundation_df.groupby('week')['hour_column'].sum().reset_index()
framing_agg = framing_df.groupby('week')['hour_column'].sum().reset_index()
cs_agg = cs_df.groupby('week')['hour_column'].sum().reset_index()
roofing_agg = roofing_df.groupby('week')['hour_column'].sum().reset_index()


groundwork_tdf = pd.DataFrame(groundwork_agg)
foundation_tdf = pd.DataFrame(foundation_agg)
framing_tdf = pd.DataFrame(framing_agg)
cs_tdf = pd.DataFrame(cs_agg)
roofing_tdf = pd.DataFrame(roofing_agg)

# Plotting the data
plt.figure(figsize=(15,5))

plt.hist(foundation_tdf['week'], weights=foundation_tdf['hour_column'], 
         bins=30,
         alpha=0.5, 
         label='Foundation') 

plt.hist(groundwork_tdf['week'],  weights=groundwork_tdf['hour_column'],
         bins=15,
         alpha=0.5, # the transaparency parameter 
         label='Groundwork') 

plt.xticks(rotation=90)
plt.legend(loc='upper right') 
plt.title('Overlapping time Groundwork and Foundation', fontsize=20) 

plt.tight_layout()

plt.show()


# <center>There was only <b>1 overlap on week 47 of 2022<center>

# ---------------------------------------------------------------------------------------------------------------------------

# In[25]:


# Plotting the data
plt.figure(figsize=(12,7))

plt.hist(foundation_tdf['week'],  weights=foundation_tdf['hour_column'],
         bins=50,
         alpha=0.5, # the transaparency parameter 
         label='Foundation') 

plt.hist(groundwork_tdf['week'],  weights=groundwork_tdf['hour_column'],
         bins=50,
         alpha=0.5, # the transaparency parameter 
         label='Groundwork') 

plt.hist(framing_tdf['week'], weights=framing_tdf['hour_column'], 
         bins = 50,
         alpha=0.5, 
         label='Framing') 

plt.xticks(rotation=90)
plt.legend(loc='upper right') 
plt.title('Overlapping time Foundation, Groundowrk and Framing',fontsize=16) 
plt.tight_layout()

plt.show()


# <center>There was a <b>2 week overlap</b> between foundation and framing on weeks <b>50-2022 and 04-2023</b>, then there was another week of groundwork on week 45-2022 but there was no overlap during that week<cener>

# -------------------------------------------------------------------------------------------------------------------------------

# In[ ]:





# In[26]:


# Plotting the data
plt.figure(figsize=(12,7))
plt.hist(framing_tdf['week'],  weights=framing_tdf['hour_column'],
         bins=50,
         alpha=0.5, # the transaparency parameter 
         label='Framing') 

plt.hist(roofing_tdf['week'], weights=roofing_tdf['hour_column'], 
         bins = 50,
         alpha=0.5, 
         label='Roofing') 

plt.xticks(rotation=90)
plt.legend(loc='upper right') 
plt.title('Overlapping time Framing and Roofing',fontsize=16) 
plt.show()


# <center>There was a <b>3 week overlap</b> between Framing and Roofing on weeks <b>12-2023, 18-2023 and 19-2023<center>

# -------------------------------------------------------------------------------------------------------------------------------

# In[27]:


# Plotting the data
plt.figure(figsize=(12,7))

plt.hist(roofing_tdf['week'], weights=roofing_tdf['hour_column'], 
         bins = 40,
         alpha=0.5, 
         label='Roofing') 

plt.hist(cs_tdf['week'], weights=cs_tdf['hour_column'], 
         bins = 40,
         alpha=0.5, 
         label='Cladding/Siding')

plt.xticks(rotation=90)
plt.legend(loc='upper right') 
plt.title('Overlapping time Roofing and Cladding/Siding',fontsize=16) 
plt.show()


# <center>There was a <b>8 week overlap</b> between Roofing and Cladding/Siding on weeks <b>14-2023, 15-2023, 16-2023, 17-2023, 
# 18-2023, 19-2023, 22-2023, 15-2023</b><cener><br>
# 

# ----------------------------------------------

# ### Graph: Weeks with Highest Overlap
# 
# In the next graph provides a close-up view of the weeks where <b>framing, roofing, and cladding/siding</b> tasks exhibit the most overlap. This zoomed-in perspective allows for a detailed examination of the interplay between these activities during critical periods of project execution.

# In[28]:


plt.figure(figsize=(15,7))
plt.hist(groundwork_tdf['week'], weights=groundwork_tdf['hour_column'], 
         bins = 50,
         alpha=0.5, 
         label='Groundwork')
plt.hist(foundation_tdf['week'], weights=foundation_tdf['hour_column'], 
         bins = 50,
         alpha=0.5, 
         label='Foundation')
plt.hist(framing_tdf['week'], weights=framing_tdf['hour_column'], 
         bins = 50,
         alpha=0.5, 
         label='Framing')
plt.hist(roofing_tdf['week'], weights=roofing_tdf['hour_column'], 
         bins = 50,
         alpha=0.5, 
         label='Roofing') 

plt.hist(cs_tdf['week'], weights=cs_tdf['hour_column'], 
         bins = 50,
         alpha=0.5, 
         label='Cladding/Siding')
 
plt.xticks(rotation=90)

plt.xlim(18, 30)

plt.legend(loc='upper right') 
plt.title('Overlapping time Cladding/Siding and Roofing') 
plt.show()


# ------------------------------------------------------------------------------------------------------------------------

# In[29]:


#phase3_time_df=[]
time_df = [groundwork_tdf, 
foundation_tdf, 
framing_tdf, 
cs_tdf, 
roofing_tdf]

phase3_time_df = pd.concat(time_df)
phase3_time_df= phase3_time_df.groupby('week')["hour_column"].sum().reset_index()
#phase3_time_df.style


# ### Graph: Overlapping of Tasks with Human Hours per Week
# 
# In this graph, overlapping sections represent the concurrency of tasks, while the red dots indicate the total human hours required each week. The hours are calculated as the sum of human hours per task when they overlap, providing a comprehensive understanding of resource allocation during periods of concurrent activity.

# In[30]:


plt.figure(figsize=(20,7))
plt.hist(groundwork_tdf['week'], weights=groundwork_tdf['hour_column'], 
         bins = 50,
         alpha=0.5, 
         label='Groundwork')
plt.hist(foundation_tdf['week'], weights=foundation_tdf['hour_column'], 
         bins = 50,
         alpha=0.5, 
         label='Foundation')
plt.hist(framing_tdf['week'], weights=framing_tdf['hour_column'], 
         bins = 50,
         alpha=0.5, 
         label='Framing')
plt.hist(roofing_tdf['week'], weights=roofing_tdf['hour_column'], 
         bins = 50,
         alpha=0.5, 
         label='Roofing') 

plt.hist(cs_tdf['week'], weights=cs_tdf['hour_column'], 
         bins = 50,
         alpha=0.5, 
         label='Cladding/Siding')

plt.scatter(phase3_time_df['week'], phase3_time_df['hour_column'], color='red', label='Total Human Hours')

 
plt.xticks(rotation=90)

plt.legend(loc='upper right') 
plt.title('Overlapping time Cladding/Siding and Roofing', fontsize = 20) 
plt.tight_layout()
plt.show()


# #### Observation:
# 
# The graph illustrates a clear relationship between task overlap and the total human hours required, <b>particularly noticeable from weeks 18 to 25.</b> This suggests that as tasks overlap more, there's a corresponding increase in human resource demand. This correlation underscores the need for careful resource management to mitigate risks such as burnout and maintain productivity during intense project phases.

# -----------------------------------------------------------

# ### Construction Work Schedule:
# 
# Below is the Gantt chart detailing the duration of each task in the construction project. Additionally, it provides a unique perspective on task overlap and identifies where these overlaps occur.

# In[32]:







