#!/usr/bin/env python
# coding: utf-8

# In[16]:


import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px
import re #regex


# In[17]:


#Create phase 4 DF 
phase4_df = pd.read_excel('C:\\Users\\David\\Downloads\\Phase 4\\excel\\Phase4.xlsx')


# In[18]:


# phase4_df.head()


# In[19]:


# Converting the 'Hours' column from HH:MM:SS to hours in decimal form

# Ensuring 'Hours' column is in string format
phase4_df['Hours'] = phase4_df['Hours'].astype(str)
# First, converting to timedelta to access the hour component
phase4_df['Hours'] = pd.to_timedelta(phase4_df['Hours'])

# Extracting hours as a float
phase4_df['Hours'] = phase4_df['Hours'].dt.total_seconds() / 3600
# print(phase4_df.dtypes)


# In[20]:


# Converting 'Date' column to datetime
phase4_df['Date'] = pd.to_datetime(phase4_df['Date'], format='%m/%d/%Y')

# Creating 'Year' and 'Week' columns
phase4_df['Year'] = phase4_df['Date'].dt.year
phase4_df['Week'] = phase4_df['Date'].dt.isocalendar().week

# phase4_df['date_clean'] = pd.to_datetime(phase4_df['Date'], errors='coerce')
phase4_df['Weeks'] = phase4_df['Date'].dt.strftime('%Y-%U')


# # Title: Exploratory Data Analysis of PO69 Phase 4 Project length and Overtime
# ## Author: David Linares
# ## Date: 06-14-2024

# ### Objectives
# #### 1. Compare the duration and human hours cost of each task 
# 
# #### 2. Analyze any overlap between tasks
#     - Detect any overlap between tasks to identify "peak weeks" and human hour cost on those weeks
# #### 3. Overtime analysis :
#     -Calculate Overtime hours and regular hours of the whole Phase 4
#     -Calculate Overtime hours and regular hours per task

# ============================================================================================================

# #### 1. Compare the duration and human hours cost of each task 
#     Phase 4 took 36 weeks to complete or 2061.25 human hours

# In[21]:


#Array of all tasks that were not specified in odoo
badtsk = ['/', 'Final touch ups','trim, caulk, prime,',
       'Trim, caulk, touch ups,']


# In[22]:


phase4_df['Task'] = phase4_df['Task'].replace(badtsk, 'Prime and Touch ups')


# In[23]:


#Save the name of each unique task in an array
tasks = phase4_df['Task'].unique()


# In[24]:


# Using list comprehension to filter out bad tasks
tasks = [task for task in tasks if task in tasks]

# Convert list to array
tasks_array = np.array(tasks)

# Create a mask for non-NaN values
mask = np.array([task != 'nan' for task in tasks_array])

# Apply the mask to get only non-NaN values
tasks = tasks_array[mask]

# tasks


# In[25]:


# Get the rows from the phase4_df where Task column contains values that exists in the tasks array
phase4_df = phase4_df[phase4_df['Task'].isin(tasks)]


# In[26]:


phase4_total_weeks = phase4_df['Weeks'].nunique()

phase4_total_hours = phase4_df['Hours'].sum()

# print(f"Phase 4 took {phase4_total_weeks} weeks to complete or {phase4_total_hours} human hours")


# In[27]:


# Create separate dataframes for each task
task_dfs = {task: phase4_df[phase4_df['Task'] == task] for task in tasks}

#  # Printing the first few rows of each dataframe
# for task, task_df in task_dfs.items():
#     print(f"Task: {task}")
#     print(task_df.head())
#     print("\n")


# ### Tasks table 

# In[28]:


#Calculate Hours per Task
total_hours = phase4_df.groupby('Task')['Hours'].sum().reset_index()
total_hours.columns = ['Task','Hours']

#Calculate Weeks per Task
total_weeks = phase4_df.groupby('Task')['Weeks'].nunique().reset_index()
total_weeks.columns = ['Task','Weeks']

#Get min date per Task
start_date = phase4_df.groupby('Task')['Date'].min().reset_index()
start_date.columns = ['Task','Start Date']

#Get min date per Task
end_date = phase4_df.groupby('Task')['Date'].max().reset_index()
end_date.columns = ['Task','End Date']

#Merge the two calculations
hour_week_df = pd.merge(total_hours,total_weeks, on='Task')
hour_week_df = pd.merge(hour_week_df,start_date, on='Task')
hour_week_df = pd.merge(hour_week_df,end_date, on='Task')
hour_week_df = hour_week_df.sort_values(by='Start Date')
hour_week_df.style


# In[29]:


#Plot
# Set the seaborn style
sns.set(style="whitegrid")

# Create a figure and a set of subplots
fig, ax1 = plt.subplots(figsize=(15, 7))

# Plot the bar chart on ax1
sns.barplot(x='Task', y='Hours',data=total_hours, ax=ax1, color='b', alpha=0.6)

# Set labels for the first y-axis
ax1.set_ylabel('Total Hours', color='b')
ax1.set_xlabel('Tasks')
ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90)

# Create a second y-axis to plot the weeks
ax2 = ax1.twinx()
ax2.plot(total_weeks['Task'], total_weeks['Weeks'], color='r', marker='o', linewidth=2)

# Set labels for the second y-axis
ax2.set_ylabel('Weeks', color='r')
plt.tight_layout()

# Show the plot
plt.title('Total Hours and Weeks by Phase')
plt.show()


# ---------------------------

# ### 2. Analyze any overlap between tasks
#     

# In[30]:


# Grouping by both 'Week' and 'Task' and aggregating hours
grouped_df = phase4_df.groupby(['Weeks', 'Task'])['Hours'].sum().reset_index()

# Plotting
plt.figure(figsize=(15, 7))
sns.barplot(x='Weeks', y='Hours', hue='Task', data=grouped_df, palette='Set3')

# Adjusting bar width using matplotlib after seaborn plot
for patch in plt.gca().patches:
    current_width = patch.get_width()
    diff = current_width * 1  
    patch.set_width(current_width + diff)

#Calculate the sum of hours per week not task!!    
phase4_time_df= phase4_df.groupby('Weeks')["Hours"].sum().reset_index()    
plt.scatter(phase4_time_df['Weeks'], phase4_time_df['Hours'], color='red', label='Total Human Hours')


plt.title('Sum of Hours per Week for Each Task')
plt.xticks(rotation=90)
plt.xlabel('Weeks')
plt.ylabel('Sum of Hours')
plt.legend(title='Task', loc='upper right', fontsize="13")
plt.grid(color = 'gray', linestyle = '-', linewidth = 0.6)
plt.tight_layout()
plt.show()


# <center> Here we can notice only a few overlaps, the most significative one being the one between <b>Interior Framing, Insulation</b> and the first weeks of <b>Drywall</b>, that overlap also reflects a significant higher human hours on week 2023-49</center>

# --------------------------------------------------------------------------------------------

# In[31]:


#Select data from tasks in di 
di = ['Interior Framing', 'Insulation','Drywall']
di_df = grouped_df.loc[grouped_df["Task"].isin(di)]


# ### Zoom on the most overlaped weeks / tasks

# In[32]:


# Plotting overlap 
plt.figure(figsize=(15, 7))
sns.barplot(x='Weeks', y='Hours', hue='Task', data=di_df, palette='Set3')

# Adjusting bar width using matplotlib after seaborn plot
for patch in plt.gca().patches:
    current_width = patch.get_width()
    diff = current_width * 0.2  
    patch.set_width(current_width + diff)

plt.title('Overlap between Interior Framing and Insulation')
plt.xticks(rotation=90)
plt.xlabel('Weeks')
plt.ylabel('Sum of Hours')
plt.legend(title='Task', loc='upper right', fontsize="13")
plt.grid(color = 'gray', linestyle = '-', linewidth = 0.6)
plt.tight_layout()
plt.show()


# -----------------------------------------------------------------------------------------

# ### 3. Overtime Analysis

# In[33]:


# phase4_df = phase4_df.replace('_x000D_',' ')
# phase4_df.head(50)


# In[34]:


# Overtime and regular hours calculations
# Sum the hours by week and employee, but keep all the other columns from the original DF
weekly_df = phase4_df.groupby(['Employee', 'Weeks']).agg({
    'Date': 'first',
    'Task': 'first',
    'Description': 'first',
    'Hours': 'sum',
    'Year': 'first',
    'Week': 'first'
}).reset_index()

# Sum the hours per week, employee and task
# weekly_df = phase4_df.groupby(['Weeks','Employee'])['Hours'].sum().reset_index()
# weekly_df = pd.DataFrame(weekly_df)

# Calculate overtime and regular hours
weekly_df['overtime'] = weekly_df['Hours'].apply(lambda x: x - 40 if x > 40 else 0)
weekly_df['regular_hours'] = weekly_df['Hours'] - weekly_df['overtime']

# Total regular_hours Phase4
regular_hours= weekly_df['regular_hours'].sum()
# Total regular_hours Phase4
overtime_hours= weekly_df['overtime'].sum()


# Normalize Names
weekly_df['Employee'] = weekly_df['Employee'].str.replace('_x000D_',' ')

def add_space_to_camel_case(text):
    # Use regex to find uppercase letters and add a space before them
    spaced_text = re.sub(r'(?<!^)(?<!\s)(?=[A-Z])', ' ', text)
    return spaced_text

weekly_df['Employee']= weekly_df['Employee'].apply(add_space_to_camel_case)

# Mapping of short names to full names
name_map = {
    'Azael': 'Azael Santos',
    'Brea': 'Brea Mc Lellan',
    'David': 'David Aceituno',
    'Malekey': 'Malekey Boddie',
    'Mike': 'Mike Cluett',
    'Neil': 'Neil Wolthers',
    'Tim': 'Tim Bargen'
}

weekly_df['Employee'] = weekly_df['Employee'].replace(name_map)


# Set the weeks column as index
weekly_df.set_index('Date', inplace=True)
# print(weekly_df.columns)

# print(regular_hours, overtime_hours)


#  <center>Phase 4 took <b>1985.75 Regular hours</b> and <b>75.5 Overtime hours</b> <center>

# #### Overtime hours and Regular hours per Week

# In[35]:


# Aggregate by 'week' to get the total regular_hours and overtime
weekly_aggregate = weekly_df.groupby('Weeks')[['regular_hours','overtime']].sum().reset_index()

weekly_aggregate.style


# In[36]:


# ------------------------------------Plotting Overtime and regular hours per week-------------------------------------
plt.figure(figsize=(17, 7))

# Plot regular hours and overtime hours
plt.bar(weekly_aggregate['Weeks'], weekly_aggregate['overtime'], label='Overtime',color='orange')
plt.bar(weekly_aggregate['Weeks'], weekly_aggregate['regular_hours'], bottom=weekly_aggregate['overtime'], label='Regular Hours')

# Add labels and title
plt.xlabel('Week')
plt.ylabel('Hours')
plt.title('Regular Hours and Overtime Hours per Week', fontsize = 20)
plt.xticks(weekly_aggregate['Weeks'],rotation=90)
plt.legend()
# plt.tight_layout()
# Show plot

plt.show()


# In[37]:


# Overtime and regular hours calculations

# # Sum the hours per week, employee and task
# weekly_df = phase4_df.groupby(['Weeks','Employee'])['Hours'].sum().reset_index()
# weekly_df = pd.DataFrame(weekly_df)

# # Calculate overtime and regular hours
# weekly_df['overtime'] = weekly_df['Hours'].apply(lambda x: x - 40 if x > 40 else 0)
# weekly_df['regular_hours'] = weekly_df['Hours'] - weekly_df['overtime']

total_regular_hours = weekly_df['regular_hours'].sum()
total_overtime = weekly_df['overtime'].sum()

# Plotting
fig, ax = plt.subplots(figsize=(7, 5))
ax.pie([total_regular_hours, total_overtime], labels=['Regular Hours', 'Overtime'], autopct='%1.1f%%')
ax.set_title('Total Distribution of Regular Hours and Overtime Hours')
plt.tight_layout()
# Show plot
plt.show()


# ---------------------

# ### Weekly Overtime hours and Regular hours per Employee

# In[38]:


# weekly_aggregate.style
# Aggregate by 'week' to get the total regular_hours and overtime
weekly_emp = weekly_df.groupby('Employee')[['regular_hours','overtime']].sum().reset_index()

weekly_emp.style


# In[39]:


# Plotting
plt.figure(figsize=(17, 7))

# Plot regular hours and overtime hours
plt.bar(weekly_emp['Employee'], weekly_emp['overtime'], label='Overtime',color='orange')
plt.bar(weekly_emp['Employee'], weekly_emp['regular_hours'], bottom=weekly_emp['overtime'], label='Regular Hours')

# Add labels and title
plt.xlabel('Week')
plt.ylabel('Hours')
plt.title('Regular Hours and Overtime Hours per Week', fontsize = 20)
plt.xticks(weekly_emp['Employee'],rotation=90)
plt.legend()
# plt.tight_layout()
# Show plot
plt.show()


# ------------------------------------------------

# ### Overtime and Regular Hours per Task

# In[40]:


# Overtime by Task
# Aggregate by 'task' to get the total regular_hours and overtime
task_aggregate = weekly_df.groupby('Task')[['regular_hours','overtime']].sum().reset_index()

#Print task_aggregate table
task_aggregate.style


# In[41]:


# Plotting
plt.figure(figsize=(17, 7))

# Plot regular hours and overtime hours
plt.bar(task_aggregate['Task'], task_aggregate['overtime'], label='Overtime',color='orange')
plt.bar(task_aggregate['Task'], task_aggregate['regular_hours'], bottom=task_aggregate['overtime'], label='Regular Hours')

# Add labels and title
plt.xlabel('Task')
plt.ylabel('Hours')
plt.title('Regular Hours and Overtime Hours per Task', fontsize = 20)
plt.xticks(task_aggregate['Task'],rotation=90)
plt.legend()
# plt.tight_layout()
# Show plot
plt.show()






