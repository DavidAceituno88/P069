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


df = pd.read_excel('Expenses.xlsx')

df = df.rename(columns={'Unnamed: 0': 'Type'})
purchase_df = pd.read_excel('purchasetbl.xlsx')


# # Title: Exploratory Data Analysis of PO69 Phase 3 Expenses
# ## Author: David Linares
# ## Date: 06-11-2024

# ### Objectives
# #### 1. Analyze and calculate percentages of the different types of expenses:
#     This analysis aims to break down the different types of expenses and calculate their totals under different categories:
#         -Month
#         -Total length of Phase 3
#         -Percentage of each type of expense
# 

# ### <center>Expenses table per month<center>

# <center>For Phase 3 <b>1952.25 CAD</b> was expended on Travel- Kilomenters, <b>32,790.00 CAD</b> on Per Diem, <b>21,485.42</b> on Acccommodations and <b>1202.12</b> CAD on EXP<center>

# In[28]:


#------------------------------------------------- Purchase Data Frame---------------------------------------#
# Rename Purchase columns
purchase_df = purchase_df.rename(columns={'Unnamed: 0': 'Type'})
purchase_df = purchase_df.rename(columns={'Unnamed: 2': 'January 2023 total','Unnamed: 4': 'February 2023 total','Unnamed: 6': 'March 2023 total',
                                         'Unnamed: 8': 'April 2023 total','Unnamed: 10': 'May 2023 total','Unnamed: 12': 'June 2023 total'
                                         ,'Unnamed: 14': 'July 2023 total','Unnamed: 16': 'August 2023 total','Unnamed: 18': 'September 2023 total',
                                         'Unnamed: 20': 'October 2023 total','Unnamed: 22': 'November 2023 total','Unnamed: 24': 'December 2023 total'
                                         ,'Unnamed: 26': 'January 2024 total','Unnamed: 28': 'February 2024 total','Unnamed: 30': 'March 2024 total'
                                         ,'Unnamed: 32': 'April 2024 total','Unnamed: 34': 'May 2024 total','Unnamed: 36': 'June 2024 total'})


# In[4]:


#------------------Expenses Per Diem Kilometers Data Frame------------------------------#

# Melt the DataFrame to long format
df_long = pd.melt(df, id_vars=['Type'], var_name='Month/Year', value_name='Amount')

# Exclude 'Total' rows for datetime conversion
df_long = df_long[df_long['Month/Year'] != 'Total']

# Convert the "Month" column to datetime
df_long['Month/Year'] = pd.to_datetime(df_long['Month/Year'])
# # Convert the "Month" column to month and year format
df_long['Month/Year'] = df_long['Month/Year'].dt.to_period('M')

df_long.loc[:, 'Month/Year'] = df_long['Month/Year'].dt.strftime('%B %Y')

df_long.head()


# In[5]:


#---------------------------------------------Expense Data Frame---------------------------------------------#
# Pivot the DataFrame
pivot_table = df_long.pivot_table(index='Month/Year', columns='Type', values='Amount', aggfunc='sum')

# Sort the index to ensure the months are in the correct order
pivot_table.sort_index(inplace=True)

# Adding a total row at the bottom of the DataFrame
pivot_table.loc['Total'] = pivot_table.sum()

pivot_table=pd.DataFrame(pivot_table)

# Display the pivot table
pivot_table.style

# # Pivot the DataFrame
# pivot_df = df_row.pivot_table(index='Month/Year', columns='Type', values='Total_amount', aggfunc='sum')

# # Sort the index to ensure the months are in the correct order
# pivot_df.sort_index(inplace=True)

# # Adding a total row at the bottom of the DataFrame
# #pivot_table.loc['Total'] = pivot_table.sum()

# pivot_df=pd.DataFrame(pivot_df)
# pivot_df = pivot_df.loc[:, pivot_df.columns!='Total']

# # Display the pivot table
# pivot_df.style


# In[6]:


#-------------------------------------Purchase Data Frame-------------------------------------------#
accommodation_df = purchase_df[purchase_df['Type'].str.contains('P069 - Accommodations', na=False)]
# accommodation_df.style

df = accommodation_df.filter(like='total')
df.columns = df.columns.str.replace('total','')


# In[7]:


#Convert the DF to Long Format
melted_df = df.melt(var_name='Month/Year', value_name='Total', ignore_index=False).reset_index(drop=True)
melted_df = melted_df.dropna(subset=['Total'])
melted_df = pd.DataFrame(melted_df)

# Convert the "Month" column to datetime
melted_df['Month/Year'] = pd.to_datetime(melted_df['Month/Year'])

# # Convert the "Month" column to month and year format
melted_df['Month/Year'] = melted_df['Month/Year'].dt.to_period('M')

# melted_df.style


# In[8]:


# Filter the DataFrame to select only months between April 2023 and September 2023
phase3_df = melted_df[(melted_df['Month/Year'] >= '2023-04-01') & (melted_df['Month/Year'] <= '2023-09-30')]

# Convert 'Month' column to month name and year format
phase3_df.loc[:, 'Month/Year'] = phase3_df['Month/Year'].dt.strftime('%B %Y')

# phase3_df.style


# #### Monthly Accommodations table

# In[9]:


#Calculate Accommodations total by month
phase3_mdf = phase3_df.groupby('Month/Year')['Total'].sum()
phase3_mdf = pd.DataFrame(phase3_mdf)

#Calculate total cost of Accommodations
total = phase3_df['Total'].sum()
phase3_mdf.style


# #### Monthly Expenses table

# In[10]:


#Merge the accommodations table with the expenses table

#Add a column to the melted_df and fill it with the string Accommodations
melted_df['Type']='Accommodations'

#Delete null values from melted_df
melted_df= melted_df.fillna(0)

#Delete null values from df_long
df_long = df_long.fillna(0)

#Concatenate df_long and melted_df
df_row = pd.concat([df_long,melted_df])

#Replace null values with 0
df_row.fillna(0, inplace=True)

#Create new column Total = sum Column Amount and Total
df_row['Total_amount']=df_row['Amount']+df_row['Total']

#Delete the two added columns
df_row.drop(columns=['Amount', 'Total'], inplace=True)

#Select columns that correspond to the dates of Phase 3
df_row = df_row[(df_row['Month/Year'] >= '2023-04-01') & (df_row['Month/Year'] <= '2023-09-30')]


# Pivot the DataFrame
pivot_df = df_row.pivot_table(index='Month/Year', columns='Type', values='Total_amount', aggfunc='sum')

# Sort the index to ensure the months are in the correct order
pivot_df.sort_index(inplace=True)

# Adding a total row at the bottom of the DataFrame
#pivot_table.loc['Total'] = pivot_table.sum()


pivot_df=pd.DataFrame(pivot_df)

#Select all the columns but the Total column
pivot_df = pivot_df.loc[:, pivot_df.columns!='Total']



# Display the pivot table
pivot_df.style


# In[11]:


# Plotting total expenses by type and monthly expenses in one figure
plt.figure(figsize=(14, 6))

# Plotting monthly expenses
pivot_df.plot(kind='bar', figsize=(20, 6), alpha=0.7)

# Adding labels and title
plt.xlabel('Month/Year')
plt.ylabel('Amount')
plt.title('Total Expenses by Type and Monthly Expenses')
plt.legend(title='Expense Type')
plt.grid(axis = 'y')
plt.show()


# In[12]:


#-------------------------------------------- Purchases -------------------------------------#

#Select only the purchases from Phase 3
purchases_df = purchase_df[purchase_df['Type'].str.contains('Phase 3', na=False)]

#Select the columns that contain the word total
purchases_df = purchases_df.filter(like='total')

#Delete the word total from the selected columns
purchases_df.columns = purchases_df.columns.str.replace('total','')

#Convert table to Long Format
porch_df = purchases_df.melt(var_name='Month/Year', value_name='Total', ignore_index=False).reset_index(drop=True)

#Drop the total column so it doesnt show on the graphs
porch_df = porch_df.dropna(subset=['Total'])
porch_df = pd.DataFrame(porch_df)

# Convert the "Month" column to datetime
porch_df['Month/Year'] = pd.to_datetime(porch_df['Month/Year'], errors='coerce')

# Drop rows where 'Month' couldn't be converted to datetime (NaT values)
porch_df = porch_df.dropna(subset=['Month/Year'])

# Convert the "Month" column to month and year format
porch_df['Month/Year'] = porch_df['Month/Year'].dt.to_period('M')

# Sort the DataFrame by 'Month'
porch_df = porch_df.sort_values(by='Month/Year').copy()

# Calculate the total Purchases by Month
porch_df = porch_df.groupby('Month/Year').sum().reset_index()

# porch_df


# In[13]:


# Calculate all the totals so that it can be displayed in a table
total2 = porch_df['Total'].sum()
total = phase3_df['Total'].sum()
total3 = pivot_table.iat[-1,-1]


# In[14]:


# Create a new DataFrame with the total sums
total_tbl = pd.DataFrame({
    'Purchase': 48510.58,
    'Accommodations': [total],
    'Per Diem + Kilometers': [total3]
})

# total_tbl


# In[ ]:





# In[15]:


#Drop the total column from the Expenses Data Frame 
test = pivot_table.loc[:,pivot_table.columns!='Total']

# You can calculate the sum of each column to represent the pie chart
sums = test.sum()

# Add the Accommodation column to the data frame
sums['Accommodation' ] = phase3_df['Total'].sum()


# In[16]:


# Plotting
plt.figure(figsize=(9, 7))
plt.pie(sums, labels=sums.index, autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.legend(title='Expenses', loc='upper right')
plt.title('Distribution of Expenses by Type')
# plt.text(0, -1.2,"Only 8.7% of this Phase expenses where not Per Diem",fontsize=12, ha='center')
plt.show()


# In[ ]:





# ### Purchase Expenses table and Graphs
#     $32,949.13 CAD was the total expense for Purchases during this Phase

# In[17]:


#Monthly Purchase Table
porch_df


# In[18]:


plt.figure(figsize=(15, 5))
plt.bar(range(len(porch_df)), porch_df['Total'], color='skyblue')
plt.title('Monthly Purchase Expense Totals')
plt.xlabel('Month/Year')
plt.ylabel('Total')

# Set the x-axis tick labels
plt.xticks(range(len(porch_df)), porch_df['Month/Year'], rotation=90)

plt.grid(axis='y')
plt.tight_layout()

# Display the plot
plt.show()


# ### Distribution of Expenses by Purchases, Acommodations and Per Diem/Kilometers

# ### Total expenses table

# In[19]:


#Total expenses table

total_tbl


# In[20]:


# Assuming total2 and total are already calculated
total2 = porch_df['Total'].sum()
total = phase3_df['Total'].sum()
total3 = pivot_table['Total'].sum() 

# Creating the plot
fig, ax = plt.subplots()

# Plotting the values
labels = ['Purchases Total', 'Accommodation Total', 'Per Diem Total']
values = [total2, total, total3]

ax.bar(labels, values, color=['blue', 'green', 'red'])

# Adding labels and title
ax.set_ylabel('Sum of Totals')
ax.set_title('Comparison of Totals from Purchases , Per Diem and Accommodations')

# Show the plot
plt.show()


# In[21]:


# # Convert 'Month/Year' column in pivot_table to period
# #pivot_table['Month/Year'] = pivot_table['Month/Year'].dt.to_period('M')
# melted_df['Type']='Accommodations'

# melted_df= melted_df.fillna(0)
# df_long = df_long.fillna(0)
# df_row = pd.concat([df_long,melted_df])
# df_row.fillna(0, inplace=True)
# df_row['Total_amount']=df_row['Amount']+df_row['Total']

# df_row.drop(columns=['Amount', 'Total'], inplace=True)

# df_row = df_row[(df_row['Month/Year'] >= '2023-04-01') & (df_row['Month/Year'] <= '2023-09-30')]

# #df_row.style
# # Pivot the DataFrame
# pivot_df = df_row.pivot_table(index='Month/Year', columns='Type', values='Total_amount', aggfunc='sum')

# # Sort the index to ensure the months are in the correct order
# pivot_df.sort_index(inplace=True)

# # Adding a total row at the bottom of the DataFrame
# #pivot_table.loc['Total'] = pivot_table.sum()

# pivot_df=pd.DataFrame(pivot_df)
# pivot_df = pivot_df.loc[:, pivot_df.columns!='Total']



# # Display the pivot table
# pivot_df.style


# In[22]:


# # Plotting total expenses by type and monthly expenses in one figure
# plt.figure(figsize=(14, 6))

# # Plotting monthly expenses
# pivot_table.plot(kind='bar', figsize=(14, 6), alpha=0.7)

# # Adding labels and title
# plt.xlabel('Month/Year')
# plt.ylabel('Amount')
# plt.title('Total Expenses by Type and Monthly Expenses')
# plt.legend(title='Expense Type')
# plt.grid(axis = 'y')
# plt.show()

# # Plotting total expenses by type and monthly expenses in one figure
# plt.figure(figsize=(14, 6))

# # Plotting monthly expenses
# pivot_df.plot(kind='bar', figsize=(20, 6), alpha=0.7)

# # Adding labels and title
# plt.xlabel('Month/Year')
# plt.ylabel('Amount')
# plt.title('Total Expenses by Type and Monthly Expenses')
# plt.legend(title='Expense Type')
# plt.grid(axis = 'y')
# plt.show()


# ### Conclusions:
#     Out of all the expenses Per Diem not including traveling was the highest expense during this phase (Not counting sub contracts)

# In[23]:


# # Pivot the DataFrame
# pivot_df = df_row.pivot_table(index='Month/Year', columns='Type', values='Total_amount', aggfunc='sum')

# # Sort the index to ensure the months are in the correct order
# pivot_df.sort_index(inplace=True)

# # Adding a total row at the bottom of the DataFrame
# #pivot_table.loc['Total'] = pivot_table.sum()

# pivot_df=pd.DataFrame(pivot_df)
# pivot_df = pivot_df.loc[:, pivot_df.columns!='Total']
# # Display the pivot table
# pivot_df.style


# In[24]:


# # Plotting total expenses by type and monthly expenses in one figure
# plt.figure(figsize=(14, 6))

# # Plotting monthly expenses
# pivot_df.plot(kind='bar', figsize=(20, 6), alpha=0.7)

# # Adding labels and title
# plt.xlabel('Month/Year')
# plt.ylabel('Amount')
# plt.title('Total Expenses by Type and Monthly Expenses')
# plt.legend(title='Expense Type')
# plt.grid(axis = 'y')
# plt.show()


# In[25]:


# pivot_df.style, porch_df


# In[26]:


# with pd.ExcelWriter("P060 Phase3 Expenses.xlsx", engine = "openpyxl") as writer:
#     pivot_df.to_excel(writer,sheet_name='Per Diem_KM_Accommodations')
#     porch_df.to_excel(writer,sheet_name='Purchases')


# In[ ]:





# In[ ]:





# In[ ]:




