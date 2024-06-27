import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px
import P069_Phase4_Expense as exp
import P069_Phase4_Overtime as ot 

#--------------------- Expenses Data  ----------------------#
expenses_dft = exp.expenses_dft
sums = exp.sums
type_df = exp.type_df
purchase_dfm = exp.purchase_dfm
total_tbl = exp.total_tbl

#--------------------- Overtime Data ------------------------#
weekly_aggregate = ot.weekly_aggregate # Weekly aggreagate of regular hours and overtime
total_regular_hours = ot.total_regular_hours 
total_overtime = ot.total_overtime
weekly_emp = ot.weekly_emp # Weekly Overtime and regular hours per Employee
task_aggregate = ot.task_aggregate # Overtime and regular hours per Task
hour_week_df = ot.hour_week_df # Total Hours per week
total_hours = ot.total_hours # Total Hours per Task

#------------------------------------- Streamlit -----------------------------------------------#

st.set_page_config(layout="wide")

# Set the title of the application
# Set the theme for matplotlib
plt.style.use('dark_background')    

# Sidebar menu for selecting sections
selected_section = st.sidebar.radio("Select Report", [":dollar: Expenses and Purchase", ":clock2: Hours and Overtime"])

if selected_section == ":dollar: Expenses and Purchase":
        st.subheader("P069 Phase 4 Expenses and Purchases")

        # Define your KPI metrics
        metrics_data = {
        'Total Cost': '345,625.99',
        'Travel - Kilometers': '14,670.67',
        'Per Diem': '51,430.00',
        'Accommodations': '18,386.75',
        'Purchases (Including sub-contracts)': '261,138.57'
        }

       # Display metrics data in two rows
        # First row of metrics
        col1, col2, col3 = st.columns(3)
        with col1:
                st.metric(label='Total Cost', value=f"${metrics_data['Total Cost']}")
        with col2:
                st.metric(label='Travel - Kilometers', value=f"${metrics_data['Travel - Kilometers']}")
        with col3:
                st.metric(label='Per Diem', value=f"${metrics_data['Per Diem']}")

        # Second row of metrics
        col4, col5, col6 = st.columns(3)
        with col4:
                st.metric(label='Accommodations', value=f"${metrics_data['Accommodations']}")
        with col5:
                st.metric(label='Purchases (Including sub-contracts)', value=f"${metrics_data['Purchases (Including sub-contracts)']}")
        with col6:
                st.write("")  # Empty column for layout consistency
                
        # Main Content Area

        # Monthly Expenses Section
        with st.expander("Monthly Expenses Section"):

                # Display data frame with purchases details
                expenses_dft

                # Create the bar plot for Monthly Expenses
                fig, ax = plt.subplots(figsize=(10, 5))
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

        with st.expander("Purchases Section"):
                st.subheader("Purchases & Sub-contracts")

                # Display data frame with purchases details
                st.dataframe(type_df[["Type", "Amount"]])

                amount_range = st.slider('Select Amount Range', min_value=0.0, max_value=max(type_df['Amount']), value=(0.0, max(type_df['Amount'])))

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
        with st.expander("Monthly Purchases Section"):
                st.subheader("Monthly Purchases")

                # Display data frame with monthly purchases details
                st.dataframe(purchase_dfm[["Month/Year", "Amount"]])

                # Create the bar plot for Monthly Purchases
                plt.figure(figsize=(14, 6))
                purchase_dfm.plot(kind='bar', x='Month/Year', y='Amount', ax=plt.gca(), alpha=0.7)
                plt.xlabel('Month/Year')
                plt.ylabel('Amount')
                plt.xticks(rotation=90, fontsize=20)
                plt.yticks(fontsize=20)
                plt.title('Total Expenses by Type and Monthly Expenses', fontsize = 24)
                plt.legend(title='Expense Type')
                plt.grid(axis='y')

                # Display the plot
                st.pyplot(plt)

        # Total Expenses Section
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
        # st.write("""
        # ## This is a markdown section
        # You can add more detailed explanations here.
        # - Bullet point 1
        # - Bullet point 2
        # """)
if selected_section == ":clock2: Hours and Overtime":
        st.title("P069 Phase 4 Hours and Overtime")

          # Define your KPI metrics
        metrics_data = {
        'Project Length': '36 weeks',
        'Human Hours': total_regular_hours + total_overtime,
        'Regular Hours': total_regular_hours,
        'Overtime Hours': total_overtime,
        }

       # Display metrics data in two rows
        # First row of metrics
        col1, col2, col3, col4 = st.columns(4)
        with col1:
                st.metric(label='Phase Length', value=f"{metrics_data['Project Length']}")
        with col2:
                st.metric(label='Human Hours', value=f"{metrics_data['Human Hours']}")
        with col3:
                st.metric(label='Regular Hours', value=f"{metrics_data['Regular Hours']}")
        with col4:
                st.metric(label='Overtime Hours', value=f"{metrics_data['Overtime Hours']}")

        #st.subheader("A Basic Streamlit Application Template")
        with st.expander("Overtime and Regular Hours"):
                st.subheader("Total expenses and Purchases table")
                tab1, tab2, tab3 = st.tabs(["Weekly", "Per Employee", "Per Task"])
        with tab1:
                        st.header("Weekly OT and Regular Hours")
                        plt.figure(figsize=(17, 7))

                        # Plot regular hours and overtime hours
                        plt.bar(weekly_aggregate['Weeks'], weekly_aggregate['overtime'], label='Overtime',color='#FFB74D')
                        plt.bar(weekly_aggregate['Weeks'], weekly_aggregate['regular_hours'], bottom=weekly_aggregate['overtime'], label='Regular Hours',color='#00FA9A')

                        # Add labels and title
                        plt.xlabel('Week')
                        plt.ylabel('Hours')
                        plt.title('Regular Hours and Overtime Hours per Week', fontsize = 20)
                        plt.xticks(weekly_aggregate['Weeks'],rotation=90, fontsize = 16)
                        plt.yticks(fontsize = 16)
                        plt.legend()
                        # plt.tight_layout()
                        # Show plot

                        st.pyplot(plt)
        
                        # Plotting pie
                        # Using bright colors that contrast well with a dark theme
                        colors = ['#2e8b57', '#CD5C5C'] 
                        fig, ax = plt.subplots(figsize=(7, 5))
                        ax.pie([total_regular_hours, total_overtime], labels=['Regular Hours', 'Overtime'], autopct='%1.1f%%',colors=colors)
                        ax.set_title('Total Distribution of Regular Hours and Overtime Hours')
                        plt.tight_layout()
                        # Show plot
                        st.pyplot(plt)
        with tab2:
                        weekly_emp
                        # Plotting
                        plt.figure(figsize=(17, 7))

                        # Plot regular hours and overtime hours
                        plt.bar(weekly_emp['Employee'], weekly_emp['overtime'], label='Overtime',color='orange')
                        plt.bar(weekly_emp['Employee'], weekly_emp['regular_hours'], bottom=weekly_emp['overtime'], label='Regular Hours')

                        # Add labels and title
                        plt.xlabel('Employee')
                        plt.ylabel('Hours')
                        plt.title('Regular Hours and Overtime Hours per Week', fontsize = 24)
                        plt.xticks(weekly_emp['Employee'],rotation=90,fontsize = 20)
                        plt.yticks(fontsize = 20)
                        plt.legend()
                        # plt.tight_layout()
                        # Show plot
                        st.pyplot(plt)
        with tab3:
                        task_aggregate
                        # Plotting
                        plt.figure(figsize=(17, 7))

                        # Plot regular hours and overtime hours
                        plt.bar(task_aggregate['Task'], task_aggregate['overtime'], label='Overtime',color='orange')
                        plt.bar(task_aggregate['Task'], task_aggregate['regular_hours'], bottom=task_aggregate['overtime'], label='Regular Hours')

                        # Add labels and title
                        plt.xlabel('Task')
                        plt.ylabel('Hours')
                        plt.title('Regular Hours and Overtime Hours per Task', fontsize = 23)
                        plt.xticks(task_aggregate['Task'],rotation=90, fontsize = 20)
                        plt.yticks(fontsize=20)
                        plt.legend()
                        # plt.tight_layout()
                        # Show plot
                        st.pyplot(plt)
        with st.expander("Project Length"):
                st.subheader("Project Length Table and Chart")
                
                hour_week_df
                #Plot
                # Set the seaborn style
                # sns.set_theme(style="whitegrid")

                # Create a figure and a set of subplots
                fig, ax1 = plt.subplots(figsize=(15, 10))

                # Plot the bar chart on ax1
                sns.barplot(x='Task', y='Hours',data=total_hours, ax=ax1, color="#2e8b57", alpha=0.6)

                # Set labels for the first y-axis
                ax1.set_ylabel('Total Hours', color='b',fontsize=16)
                ax1.set_xlabel('Tasks',fontsize=16)
                ax1.set_xticklabels(ax1.get_xticklabels(), rotation=90, fontsize = 20)
                ax1.set_yticklabels(ax1.get_yticklabels(),fontsize = 20)

                # Create a second y-axis to plot the weeks
                ax2 = ax1.twinx()
                ax2.plot(ot.total_weeks['Task'], ot.total_weeks['Weeks'], color='r', marker='o', linewidth=2)

                # Set labels for the second y-axis
                ax2.set_ylabel('Weeks', color='r',fontsize=16)
                ax2.set_yticklabels(ax2.get_yticklabels(),fontsize = 20)
                plt.tight_layout()

                # Show the plot
                plt.title('Total Hours and Weeks by Phase', fontsize = 24)
                st.pyplot(plt)
        with st.expander("Overlaps and Human Hour Cost"):
                st.subheader("Overlaping Tasks chart:")
                st.write("Here we plot all the tasks in chronological order, so that we can spot any overlap \n the red dots on top of the bars represent the total human hours for that week")
                # Assuming `ot.grouped_df` is your original DataFrame and contains 'Weeks', 'Hours', 'Task' columns

                # Define the available tasks
                available_tasks = ot.grouped_df['Task'].unique()

                # Multiselect widget for task selection
                selected_tasks = st.multiselect('Select Tasks to Display: ', available_tasks, default=available_tasks)

                # Filter the DataFrame based on selected tasks
                filtered_df = ot.grouped_df[ot.grouped_df['Task'].isin(selected_tasks)]

                # Plotting
                plt.figure(figsize=(20, 12))

                # Create seaborn barplot with filtered data
                bar_plot = sns.barplot(x='Weeks', y='Hours', hue='Task', data=filtered_df, palette='Set3')

                # Adjust the bar width
                for patch in bar_plot.patches:
                        current_width = patch.get_width()
                        # You can adjust this factor to change the width increment
                        width_factor = 0.8
                        new_width = current_width + width_factor * current_width
                        center = patch.get_x() + current_width / 2.0
                        patch.set_x(center - new_width / 2.0)
                        patch.set_width(new_width)

                # Calculate the sum of hours per week, not task!
                phase4_time_df = ot.phase4_df.groupby('Weeks')["Hours"].sum().reset_index()

                phase4_time_df = phase4_time_df [phase4_time_df['Weeks'].isin(filtered_df['Weeks'])]
                # Plot total hours per week as red dots
                plt.scatter(phase4_time_df['Weeks'], phase4_time_df['Hours'], color='red', s=100, label='Total Human Hours')

                # Titles and labels
                plt.title('Sum of Hours per Week for Each Task', fontsize=24)
                plt.xticks(rotation=90)
                plt.xlabel('Weeks', fontsize=20)
                plt.ylabel('Hours', fontsize=20)
                plt.xticks(fontsize=20)
                plt.yticks(fontsize=20)
                plt.legend(title='Task', loc='upper left', fontsize="20")

                # Add grid for better readability
                plt.grid(color='gray', linestyle='-', linewidth=0.6)

                # Layout adjustment
                plt.tight_layout()

                # Display the plot in Streamlit
                st.pyplot(plt)
