#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px


# In[2]:


foundation_df = pd.read_excel('foundationtbl.xlsx')
groundwork_df = pd.read_excel('groundwrk_tbl.xlsx')
framing_df = pd.read_excel('framing_tbl.xlsx')
cs_df = pd.read_excel('cladding_siding_windows_doors_tbl.xlsx')
roofing_df = pd.read_excel('roofing_tbl.xlsx')


# In[3]:


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


# # Title: Exploratory Data Analysis of PO69 Phase 3 Overtime 
# ## Author: David Linares
# ## Date: 06-04-2024

# ### Objectives
# #### 1. Calculate Human Hours Cost :
#     -Calculate Overtime hours and regular hours of the whole Phase 3
#     -Calculate Overtime hours and regular hours per task

# In[4]:


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
# phase3_df.style


# In[5]:


bigtbl_df = pd.concat([foundation_df,groundwork_df,framing_df,roofing_df,cs_df])
#bigtbl_df.head()            


# In[6]:


weekly_df = bigtbl_df.groupby(['week','Employee'])['hour_column'].sum()
weekly_df = pd.DataFrame(weekly_df)


weekly_df['overtime'] = weekly_df['hour_column'].apply(lambda x: x - 40 if x > 40 else 0)
weekly_df['regular_hours'] = weekly_df['hour_column'] - weekly_df['overtime']


# In[7]:


# Aggregate by 'week' to get the total regular_hours and overtime
weekly_aggregate = weekly_df.groupby('week').sum().reset_index()

# Plotting
plt.figure(figsize=(17, 7))

# Plot regular hours and overtime hours
plt.bar(weekly_aggregate['week'], weekly_aggregate['overtime'], label='Overtime',color='orange')
plt.bar(weekly_aggregate['week'], weekly_aggregate['regular_hours'], bottom=weekly_aggregate['overtime'], label='Regular Hours')

# Add labels and title
plt.xlabel('Week')
plt.ylabel('Hours')
plt.title('Regular Hours and Overtime Hours per Week', fontsize = 20)
plt.xticks(weekly_aggregate['week'],rotation=90)
plt.legend()
# plt.tight_layout()
# Show plot
plt.show()


# In[8]:


total_regular_hours = weekly_df['regular_hours'].sum()
total_overtime = weekly_df['overtime'].sum()

# Plotting
fig, ax = plt.subplots(figsize=(7, 5))
ax.pie([total_regular_hours, total_overtime], labels=['Regular Hours', 'Overtime'], autopct='%1.1f%%')
ax.set_title('Total Distribution of Regular Hours and Overtime Hours')
plt.tight_layout()
# Show plot
plt.show()


# In[9]:


foundation_weekdf = pd.DataFrame(foundation_df)
foundation_weekdf = foundation_weekdf.groupby(['week','Employee'])['hour_column'].sum().reset_index()
foundation_weekdf['Task'] = 'Foundation'
foundation_weekdf['Regular_hours'] = foundation_weekdf['hour_column'].apply(lambda x : x if x < 40 else 40)
foundation_weekdf['Overtime'] = foundation_weekdf['hour_column'] - foundation_weekdf['Regular_hours']
# foundation_weekdf.head()


# In[10]:


groundwork_weekdf = pd.DataFrame(groundwork_df)
groundwork_weekdf = groundwork_weekdf.groupby(['week','Employee'])['hour_column'].sum().reset_index()
groundwork_weekdf['Task'] = 'Groundwork'
groundwork_weekdf['Regular_hours'] = groundwork_weekdf['hour_column'].apply(lambda x : x if x < 40 else 40)
groundwork_weekdf['Overtime'] = groundwork_weekdf['hour_column'] - groundwork_weekdf['Regular_hours']
# groundwork_weekdf.head()


# In[11]:


framing_weekdf = pd.DataFrame(framing_df)
framing_weekdf = framing_weekdf.groupby(['week','Employee'])['hour_column'].sum().reset_index()
framing_weekdf['Task'] = 'Framing'
framing_weekdf['Regular_hours'] = framing_weekdf['hour_column'].apply(lambda x : x if x < 40 else 40)
# framing_weekdf['Overtime'] = framing_weekdf['hour_column'] - framing_weekdf['Regular_hours']


# In[12]:


roofing_weekdf = pd.DataFrame(roofing_df)
roofing_weekdf = roofing_weekdf.groupby(['week','Employee'])['hour_column'].sum().reset_index()
roofing_weekdf['Task'] = 'Roofing'
roofing_weekdf['Regular_hours'] = roofing_weekdf['hour_column'].apply(lambda x : x if x < 40 else 40)
roofing_weekdf['Overtime'] = roofing_weekdf['hour_column'] - roofing_weekdf['Regular_hours']


# In[13]:


cs_weekdf = pd.DataFrame(cs_df)
cs_weekdf = cs_weekdf.groupby(['week','Employee'])['hour_column'].sum().reset_index()
cs_weekdf['Task'] = 'Cladding/Siding'
cs_weekdf['Regular_hours'] = cs_weekdf['hour_column'].apply(lambda x : x if x < 40 else 40)
cs_weekdf['Overtime'] = cs_weekdf['hour_column'] - cs_weekdf['Regular_hours']
# cs_weekdf.head()


# In[14]:


overtime_df = pd.concat([foundation_weekdf,groundwork_weekdf,framing_weekdf,roofing_weekdf,cs_weekdf])


# In[15]:


overtime_weekly_df = overtime_df.groupby(['Task','week'])


# In[16]:


overtime_emp_df = overtime_df.groupby(['Task','Employee'])[['Regular_hours','Overtime']].sum().reset_index()
#overtime_emp_df.style


# --------------------------------

# ### <center>Hors worked by Week per Employee<center>

# In[17]:


# Define the order of tasks
task_order = ['Foundation', 'Groundwork', 'Framing', 'Roofing', 'Cladding/Siding']

# Convert 'Task' column to a categorical type with the specified order
overtime_emp_df['Task'] = pd.Categorical(overtime_emp_df['Task'], categories=task_order, ordered=True)

# Sort the DataFrame by the 'Task' column
overtime_emp_df = overtime_emp_df.sort_values(by='Task')

# Display the styled DataFrame
overtime_emp_df.style


# In[18]:


# Plotting
plt.figure(figsize=(10, 6))
width1 = 0.5
# Plot regular hours and overtime hours

plt.bar(overtime_emp_df['Employee'], overtime_emp_df['Regular_hours'], label='Regular Hours')
plt.bar(overtime_emp_df['Employee'], overtime_emp_df['Overtime'], label='Overtime Hours')

# Add labels and title
plt.xlabel('Employee')
plt.ylabel('Hours')
plt.title('Regular Hours and Overtime Hours per Employee')
plt.xticks(overtime_emp_df['Employee'],rotation=90)
plt.legend()

# Show plot
plt.show()


# ------------------------------------------------------------------------------------

# ### <center>Hours worked per Task <center>

# In[19]:


overtime_task_df = overtime_df.groupby(['Task'])[['Regular_hours','Overtime']].sum().reset_index()
overtime_task_df.style


# In[20]:


# Plotting
plt.figure(figsize=(10, 6))
width1 = 0.5
# Plot regular hours and overtime hours

plt.bar(overtime_task_df['Task'], overtime_task_df['Regular_hours'], label='Regular Hours')
plt.bar(overtime_task_df['Task'], overtime_task_df['Overtime'], label='Overtime Hours')

# Add labels and title
plt.xlabel('Task')
plt.ylabel('Hours')
plt.title('Regular Hours and Overtime Hours per Task')
plt.xticks(overtime_task_df['Task'],rotation=90)
plt.legend()

# Show plot
plt.show()


# In[27]:


overtime_emptsk_df = overtime_emp_df
overtime_emp = overtime_df.groupby(['Employee'])[['Regular_hours','Overtime']].sum().reset_index()


# In[28]:


with pd.ExcelWriter('P096 Phase 3 Overtime.xlsx') as writer:  
       overtime_task_df.to_excel(writer, sheet_name='Overtime by Task')
       overtime_emp.to_excel(writer, sheet_name='Overtime by Employee')
       overtime_emptsk_df.to_excel(writer, sheet_name = 'Overtime by task and Employee')
       


# In[ ]:




