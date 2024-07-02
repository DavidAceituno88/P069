#!/usr/bin/env python
# coding: utf-8

# In[20]:

import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px


# In[21]:


expense_df = pd.read_excel('C:\\Users\\David\\Downloads\\Phase 4\\excel\\Phase4 Expenses.xlsx')

purchase_df = pd.read_excel('C:\\Users\\David\\Downloads\\Phase 4\\excel\\Phase4 Purchases.xlsx')


# # Title: Exploratory Data Analysis of PO69 Phase 4 Expenses
# ## Author: David Linares
# ## Date: 06-18-2024

# ### Objectives
# #### 1. Analyze and calculate totals and percentages of the different types of expenses:
#     This analysis aims to break down the different types of expenses and calculate their totals under different categories:
#         - Per Diem 
#         - Kilometers
#         - Accommodations
#         - Purchases (this will include Sub-contracts, tools, materials, etc)
# 

# ## 1. Expenses Analysis.

# <center>For Phase 4 <b>14,670.67  CAD</b> was expended on Travel- Kilomenters, <b>51,430.00 CAD</b> on Per Diem, <b>18,386.75</b> on Acccommodations and <b>261,138.57</b> CAD on Purchases (Including sub-contracts)<center>

# In[22]:


# #------------------------------------------------- Purchase Data Frame---------------------------------------#
purchase_df = purchase_df.fillna(0)
purchase_df = purchase_df.rename(columns={'Unnamed: 0': 'Type'})
# Rename Purchase columns

# purchase_df = purchase_df.rename(columns={'Unnamed: 2': 'January 2023 total','Unnamed: 4': 'February 2023 total','Unnamed: 6': 'March 2023 total',
#                                          'Unnamed: 8': 'April 2023 total','Unnamed: 10': 'May 2023 total','Unnamed: 12': 'June 2023 total'
#                                          ,'Unnamed: 14': 'July 2023 total','Unnamed: 16': 'August 2023 total','Unnamed: 18': 'September 2023 total',
#                                          'Unnamed: 20': 'October 2023 total','Unnamed: 22': 'November 2023 total','Unnamed: 24': 'December 2023 total'
#                                          ,'Unnamed: 26': 'January 2024 total','Unnamed: 28': 'February 2024 total','Unnamed: 30': 'March 2024 total'
#                                          ,'Unnamed: 32': 'April 2024 total','Unnamed: 34': 'May 2024 total','Unnamed: 36': 'June 2024 total'})


# In[23]:


expense_df = expense_df.rename(columns={'Unnamed: 0':'Type'})

expense_df = expense_df.rename(columns={'Unnamed: 1':'July 2023','Unnamed: 2':'August 2023','Unnamed: 3':'September 2023',
                                        'Unnamed: 4':'October 2023','Unnamed: 5':'November 2023','Unnamed: 6':'December 2023',
                                        'Unnamed: 7':'January 2024','Unnamed: 8':'February 2024','Unnamed: 9':'March 2024',
                                        'Unnamed: 10':'April 2024','Unnamed: 11':'May 2024','Unnamed: 12':'June 2024'})

expense_df = expense_df.drop(index=0)
# expense_df.head()


# In[24]:


#------------------Expenses Per Diem Kilometers Data Frame------------------------------#
# Melt the DataFrame to long format
expense_long = pd.melt(expense_df, id_vars=['Type'], var_name='Month/Year', value_name = 'Amount')

# Convert the "Month" column to datetime
expense_long['Month/Year'] = pd.to_datetime(expense_long['Month/Year'])

# Convert the "Month" column to month and year format
expense_long['Month/Year'] = expense_long['Month/Year'].dt.to_period('M')

# Replace nan with 0
expense_long = expense_long.fillna(0)

# expense_long.style


# In[25]:


#---------------------------------------------Expense Data Frame---------------------------------------------#
# Pivot the DataFrame
pivot_exp = expense_long.pivot_table(index='Month/Year', columns='Type', values='Amount', aggfunc='sum')

# Sort the index to ensure the months are in the correct order
pivot_exp.sort_index(inplace=True)

# Adding a total row at the bottom of the DataFrame
#pivot_exp.loc['Total'] = pivot_exp.sum()

pivot_exp=pd.DataFrame(pivot_exp)

# Display the pivot table
# pivot_exp.style


# In[26]:


#-------------------------------------Purchase Data Frame-------------------------------------------#

# Rename columns
purchase_df = purchase_df.rename(columns={'Unnamed: 148':'July 2023','Unnamed: 150':'August 2023','Unnamed: 152':'September 2023',
                                         'Unnamed: 154':'October 2023','Unnamed: 156':'November 2023','Unnamed: 158':'December 2023',
                                         'Unnamed: 160':'January 2024','Unnamed: 162':'February 2024','Unnamed: 164':'March 2024',
                                         'Unnamed: 166':'April 2024','Unnamed: 168':'May 2024','Unnamed: 170':'June 2024'})

# Get rid of unwanted columns
purchase_df = purchase_df.filter(regex='^(?!Unnamed:)')
purchase_df = purchase_df.drop(columns=['Total'])

#


# In[27]:


# Accommodations df

#Select the wanted rows
accommodation_df = purchase_df[purchase_df['Type'].str.contains('P069 - Accommodations', na=False)]
# accommodation_df.head()


# In[28]:


#Convert the DF to Long Format
# Melting the DataFrame
melted_df = pd.melt(accommodation_df, id_vars=['Type'], var_name='Month/Year', value_name='Amount')

melted_df.head()

# Convert the "Month" column to datetime
melted_df['Month/Year'] = pd.to_datetime(melted_df['Month/Year'])

# Convert the "Month" column to month and year format
melted_df['Month/Year'] = melted_df['Month/Year'].dt.to_period('M')

# melted_df.head()


# In[29]:


# Convert 'Month' column to month name and year format
#phase3_df.loc[:, 'Month/Year'] = phase3_df['Month/Year'].dt.strftime('%B %Y')

# phase3_df.style


# #### Monthly Expenses table
# This table displays the expenses per Month

# In[30]:


#Calculate Accommodations total by month
phase4_acc = melted_df.groupby('Month/Year')['Amount'].sum().reset_index()
# phase4_acc = pd.DataFrame(phase4_acc)

phase4_acc['Type']='Accommodations'

#Calculate total cost of Accommodations
# total = phase3_df['Total'].sum()
# phase4_acc.style


# In[31]:


#---------------------------------------------Accommodation Data Frame---------------------------------------------#
# Pivot the DataFrame
pivot_acc = phase4_acc.pivot_table(index='Month/Year', columns='Type', values='Amount', aggfunc='sum')

# Sort the index to ensure the months are in the correct order
pivot_acc.sort_index(inplace=True)

# Adding a total row at the bottom of the DataFrame
#pivot_acc.loc['Total'] = pivot_acc.sum()

pivot_acc = pd.DataFrame(pivot_acc)

# Display the pivot table
# pivot_acc.style


# In[75]:


expenses_dft = pd.merge(pivot_exp,pivot_acc, on='Month/Year')

expenses_dft['Total'] = expenses_dft['     Travel - Kilometers'] + expenses_dft['     Travel - Per Diem (B20/L30/S50)'] + expenses_dft['Accommodations']

#Calculate totals for each column
travel_total = expenses_dft['     Travel - Kilometers'].sum()
perdiem_total =expenses_dft['     Travel - Per Diem (B20/L30/S50)'].sum()

# expenses_dft


# ----------------

# #### Montly expenses Chart per type of expense

# In[76]:


# Plotting total expenses by type and monthly expenses in one figure
plt.figure(figsize=(14, 6))

# Plotting monthly expenses
expenses_dft.plot(kind='bar', figsize=(20, 6), alpha=0.7)

# Adding labels and title
plt.xlabel('Month/Year')
plt.ylabel('Amount')
plt.title('Total Expenses by Type and Monthly Expenses')
plt.legend(title='Expense Type')
plt.grid(axis = 'y')
plt.show()


# In all the months the Per Diem expense was the highest one, followed by Accommodations and Kilometers.
# The distribution over the months was similar, except for the month 2023-09 and 2024-02, those months where the most expensive ones.

# In[35]:


expenses_dft = expenses_dft.loc[:,expenses_dft.columns!='Total']
# You can calculate the sum of each column to represent the pie chart
sums = expenses_dft.sum()


# ------------------------------------

# In[36]:


# Plotting
plt.figure(figsize=(9, 7))
plt.pie(sums, labels=sums.index, autopct='%1.1f%%', startangle=140)
plt.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
plt.legend(title='Expenses', loc='upper right')
plt.title('Distribution of Expenses by Type')
# plt.text(0, -1.2,"Only 8.7% of this Phase expenses where not Per Diem",fontsize=12, ha='center')
plt.show()


# In[61]:


#-------------------------------------------- Purchases -------------------------------------#

#Select only the purchases from Phase 4
purchase_dft = purchase_df[purchase_df['Type'].str.contains('Phase 4', na=False)]
# purchase_dft
# #Select the columns that contain the word total
# purchases_df = purchases_df.filter(like='total')

#Calculate Accommodations total by month
purchase_dft = pd.melt(purchase_dft, id_vars=['Type'], var_name='Month/Year', value_name = 'Amount')

purchase_dft.head()

# # Convert the "Month" column to datetime
purchase_dft['Month/Year'] = pd.to_datetime(purchase_dft['Month/Year'], errors='coerce')


# Convert the "Month" column to month and year format
purchase_dft['Month/Year'] = purchase_dft['Month/Year'].dt.to_period('M')

# Sort the DataFrame by 'Month'
purchase_dft = purchase_dft.sort_values(by='Month/Year').copy()

purchase_dfm = purchase_dft.groupby('Month/Year')['Amount'].sum().reset_index()




# ------------------------

# ## 2. Purchase Analysis. 

# $ <b>261,138.56 CAD</b> was the total expense for Purchases during this Phase

# ### 2.1.  Purchases by Type table in descending Amount order
# The table below contains the Amount per Type of Purchase in descending order, this will help us to detect the most and least expensive Purchases

# In[69]:


# Plotting
type_df = purchase_dft.groupby('Type')['Amount'].sum().reset_index()
type_df =type_df.sort_values("Amount", ascending=False)

# Clean data: strip whitespaces
type_df['Type'] = type_df['Type'].str.strip()
# Convert 'Amount' to numeric, coerce errors to NaN
type_df['Amount'] = pd.to_numeric(type_df['Amount'], errors='coerce')  
# type_df.style


# -----------------

# In[70]:


# Plotting the bar chart
plt.figure(figsize=(14, 10))
plt.barh(type_df['Type'], type_df['Amount'], color='skyblue')  # Horizontal bar chart for better label visibility
plt.xlabel('Amount ($)')
plt.ylabel('Type')
plt.title('Amounts by Type in P069 - Phase 4')
plt.gca().invert_yaxis()  # To have the largest bar at the top
plt.tight_layout()  # Adjusts the plot to ensure everything fits without overlap

# Show the plot
plt.show()


# *** On the chart above we can observe that the Sub contracts were the most expensive Purchases during Phase 4

# -------------------------------

# ### 2.2. Purchases by Month table
# The table below displays the total of Purchases per Month, this amount is the sum of all the purchases done each month, including sub contracts, tools, materials, etc

# In[71]:


#Monthly Purchase Table
# purchase_dfm.style


# ### Purchase by Month chart

# In[48]:


# Plotting total expenses by type and monthly expenses in one figure
plt.figure(figsize=(14, 6))

# Plotting monthly expenses
purchase_dfm.plot(kind='bar', figsize=(20, 6), alpha=0.7)

# Adding labels and title
plt.xlabel('Month/Year')
plt.ylabel('Amount')

# Set the x-axis tick labels
plt.xticks(range(len(purchase_dfm)), purchase_dfm['Month/Year'], rotation=90)

plt.title('Total Expenses by Type and Monthly Expenses')
plt.legend(title='Expense Type')
plt.grid(axis = 'y')
plt.show()


# ** In the chart above we can observe a descending trend in the expenses, with a bi monthly peak that is smaller than the previous peak

# -----------------------------

# In[39]:


# Calculate all the totals so that it can be displayed in a table
total_acc = pivot_acc['Accommodations'].sum()
total_pur = purchase_dft['Amount'].sum()
total_expense = expense_long['Amount'].sum()


# In[40]:


# Create a new DataFrame with the total sums
total_tbl = pd.DataFrame({
    'Purchase': [total_pur],
    'Accommodations': [total_acc],
    'Per Diem + Kilometers': [total_expense]
})

# total_tbl


# ### 3. Distribution of Expenses by Purchases, Acommodations and Per Diem/Kilometers
#     On this final section we can compare all the types of Purchases totals

# ### Total expenses table

# In[42]:


#Total expenses table

# total_tbl


# In[43]:


# Creating the plot
fig, ax = plt.subplots()

# Plotting the values
labels = ['Purchases Total', 'Accommodation Total', 'Per Diem Total']
values = [total_pur, total_acc, total_expense]

ax.bar(labels, values, color=['blue', 'green', 'red'])

# Adding labels and title
ax.set_ylabel('Sum of Totals')
ax.set_title('Comparison of Totals from Purchases , Per Diem and Accommodations')

# Show the plot
plt.show()


# ### Conclusions:
#     In Phase 4, travel, per diem, and accommodation expenses followed the consistent trends seen in previous phases. However, sub-contract costs emerged as the most significant expense, marking a distinct shift. This rise in sub-contracting expenses suggests a growing dependence on external services and warrants closer examination for cost optimization.

# In[44]:


# pivot_df.style, porch_df


# In[78]:


#with pd.ExcelWriter("P060 Phase4 Expenses_and_Purchases.xlsx", engine = "openpyxl") as writer:
#    expenses_dft.to_excel(writer,sheet_name='Expenses table')
#    type_df.to_excel(writer,sheet_name='Purchases per Type')
#    purchase_dfm.to_excel(writer,sheet_name='Purchases per Month')

#------------------------------------- Streamlit -----------------------------------------------#
# Set the title of the application
# Set the theme for matplotlib
plt.style.use('dark_background')    

st.title("P069 Dashboard")
st.subheader("A Basic Streamlit Application Template")

# Sidebar
st.sidebar.title("Sidebar")

# Widgets for Monthly Expenses Section
with st.sidebar.expander("Monthly Expenses Settings"):
    show_monthly_expenses = st.checkbox("Show Monthly Expenses Chart", value=True)

# Widgets for Purchases Section
with st.sidebar.expander("Purchases Settings"):
    show_purchases = st.checkbox("Show Purchases Chart", value=True)
    amount_range = st.slider('Select Amount Range', min_value=0.0, max_value=max(type_df['Amount']), value=(0.0, max(type_df['Amount'])))

# Widgets for Monthly Purchases Section
with st.sidebar.expander("Monthly Purchases Settings"):
    show_monthly_purchases = st.checkbox("Show Monthly Purchases Chart", value=True)

# Widgets for Total Expenses Section
with st.sidebar.expander("Total Expenses Settings"):
    show_total_expenses = st.checkbox("Show Total Expenses Chart", value=True)

# Main Content Area

# Monthly Expenses Section
if show_monthly_expenses:
    with st.expander("Monthly Expenses Section"):
        st.subheader("Monthly Expenses Chart")

        # Create the bar plot for Monthly Expenses
        fig, ax = plt.subplots(figsize=(10, 6))
        colors = plt.cm.Dark2(range(len(expenses_dft.columns)))
        expenses_dft.plot(kind='bar', color=colors, ax=ax, alpha=0.7)

        # Customize plot
        ax.set_xlabel('Month')
        ax.set_ylabel('Amount')
        ax.set_title('Total Expenses by Type and Monthly Expenses')
        ax.legend(title='Expense Type')
        ax.grid(axis='y')

        # Display the plot
        st.pyplot(fig)

        # Title for the Streamlit app
        st.title('Distribution of Expenses by Type')

        # Creating the pie chart using Matplotlib
        fig, ax = plt.subplots(figsize=(9, 7))
        ax.pie(sums, labels=sums.index, autopct='%1.1f%%', startangle=140, colors=colors)
        ax.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
        ax.legend(title='Expenses', loc='upper right')
        plt.title('Distribution of Expenses by Type')

        # Display the chart in Streamlit
        st.pyplot(fig)

# Purchases Section
if show_purchases:
    with st.expander("Purchases Section"):
        st.subheader("Purchases & Sub-contracts")

        # Display data frame with purchases details
        st.dataframe(type_df[["Type", "Amount"]])

        # Filter data based on amount range
        filtered_data = type_df[(type_df['Amount'] >= amount_range[0]) & (type_df['Amount'] <= amount_range[1])]

        # Create the bar plot for Purchases
        colors = plt.cm.coolwarm(type_df['Amount'] / float(max(type_df['Amount'])))
        fig, ax = plt.subplots(figsize=(14, 10))
        ax.barh(filtered_data['Type'], filtered_data['Amount'], color=colors)

        # Customize plot
        ax.set_xlabel('Amount ($)')
        ax.set_ylabel('Type')
        ax.set_title('Amounts by Type in P069 - Phase 4')
        ax.invert_yaxis()
        plt.tight_layout()

        # Display the plot
        st.pyplot(fig)

# Monthly Purchases Section
if show_monthly_purchases:
    with st.expander("Monthly Purchases Section"):
        st.subheader("Monthly Purchases")

        # Display data frame with monthly purchases details
        st.dataframe(purchase_dfm[["Month/Year", "Amount"]])

        # Create the bar plot for Monthly Purchases
        plt.figure(figsize=(14, 6))
        purchase_dfm.plot(kind='bar', x='Month/Year', y='Amount', ax=plt.gca(), alpha=0.7)
        plt.xlabel('Month/Year')
        plt.ylabel('Amount')
        plt.xticks(rotation=90)
        plt.title('Total Expenses by Type and Monthly Expenses')
        plt.legend(title='Expense Type')
        plt.grid(axis='y')

        # Display the plot
        st.pyplot(plt)

# Total Expenses Section
if show_total_expenses:
    with st.expander("Total Expenses Section"):
        st.subheader("Total expenses and Purchases table")

        # Display data frame with total expenses and purchases
        st.dataframe(total_tbl[["Purchase", "Accommodations", "Per Diem + Kilometers"]])

        # Create the bar plot for Total Expenses
        fig, ax = plt.subplots()

        labels = ['Purchases Total', 'Accommodation Total', 'Per Diem Total']
        values = [total_tbl['Purchase'].iloc[0], total_tbl['Accommodations'].iloc[0], total_tbl['Per Diem + Kilometers'].iloc[0]]

        # Select contrasting colors from different colormaps
        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Blue, Orange, Green
        ax.bar(labels, values, color=colors)

        # Customize plot
        ax.set_ylabel('Sum of Totals')
        ax.set_title('Comparison of Totals from Purchases, Per Diem, and Accommodations')

        # Display the plot
        st.pyplot(fig)

# Additional Text
st.write("""
## This is a markdown section
You can add more detailed explanations here.
- Bullet point 1
- Bullet point 2
""")