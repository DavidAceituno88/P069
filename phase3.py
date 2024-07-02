import streamlit as st
import altair as alt
import numpy as np
import pandas as pd
import matplotlib.pylab as plt
import seaborn as sns
from datetime import datetime
import plotly.express as px
import P069_Phase3_Expense as exp
import P069_Phase3_Overtime as ot 
import P069_Phase3_oa as oa

st.set_page_config(layout="wide")


def app():
        #--------------------- Expenses Data  ----------------------#
        pivot_df = exp.pivot_df
        sums = exp.sums
        porch_df = exp.porch_df
        # type_df = exp.type_df
        # purchase_dfm = exp.purchase_dfm
        total_tbl = exp.total_tbl

        # #--------------------- Overtime Data ------------------------#
        weekly_aggregate = oa.weekly_aggregate # Weekly aggreagate of regular hours and overtime
        total_regular_hours = oa.total_regular_hours 
        total_overtime = oa.total_overtime
        overtime_emp_df = oa.overtime_emp_df
        overtime_task_df = oa.overtime_task_df
        phase3_df = ot.phase3_df
        foundation_tdf = ot.foundation_tdf
        groundwork_tdf = ot.groundwork_tdf
        framing_tdf = ot.framing_tdf
        roofing_tdf = ot.roofing_tdf
        cs_tdf = ot.cs_tdf
        phase3_time_df = ot.phase3_time_df
       
        ot_emp_df = overtime_emp_df.groupby('Employee').agg({
                                'Regular_hours':'sum',
                                'Overtime':'sum'
                                }).reset_index() 

        ot_emp_df['Total_Hours']= ot_emp_df['Regular_hours']+ot_emp_df['Overtime']
        
        # Purchases df
        data = {
        'Category': ['T & J Delaney Contracting', 'Siding Materials', 'Touch up Paint','Scotia Metal Products'],
        'Value': [25937.68, 22226.53, 92.00,254.37]
        }

        # Creating the DataFrame
        pr_df = pd.DataFrame(data)

        
        #------------------------------------- Streamlit -----------------------------------------------#


        # Set the title of the application
        # Set the theme for matplotlib
        plt.style.use('dark_background')  

        # Sidebar menu for selecting sections
        selected_section = st.sidebar.radio("Select Report", [":dollar: Expenses and Purchase", ":clock2: Hours and Overtime"])

        if selected_section == ":dollar: Expenses and Purchase":
                st.subheader("P069 Phase 3 Expenses and Purchases")

                # Define your KPI metrics
                metrics_data = {
                        'Total Cost': total_tbl.iloc[0].sum(),
                        'Travel - Kilometers': pivot_df.iloc[:, 0].sum(),
                        'Per Diem': pivot_df.iloc[:, 1].sum(),
                        'Accommodations': total_tbl['Accommodations'].sum(),
                        'Purchases': pr_df['Value'].sum()
                }

                # Display metrics data in two rows
                # First row of metrics
                col1, col2, col3 = st.columns(3)
                with col1:
                        st.metric(label='Total Cost', value=f"${metrics_data['Total Cost']:.2f}")
                with col2:
                        st.metric(label='Travel - Kilometers', value=f"${metrics_data['Travel - Kilometers']}")
                with col3:
                        st.metric(label='Per Diem', value=f"${metrics_data['Per Diem']}")

                # Second row of metrics
                col4, col5, col6 = st.columns(3)
                with col4:
                        st.metric(label='Accommodations', value=f"${metrics_data['Accommodations']:.2f}")
                with col5:
                        st.metric(label='Purchases', value=f"${metrics_data['Purchases']}")
                with col6:
                        st.write("")  # Empty column for layout consistency
                                        
                # Main Content Area

                # Monthly Expenses Section
                with st.expander("Monthly Expenses Section"):
                        # Display data frame with purchases details
                        st.dataframe(pivot_df)

                        # Create the bar plot for Monthly Expenses
                        fig, ax = plt.subplots(figsize=(10, 5))
                        colors = plt.cm.Dark2(range(len(pivot_df.columns)))
                        pivot_df.plot(kind='bar', color=colors, ax=ax, alpha=0.7)

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

        #         # Purchases Section
                with st.expander("Purchases Section"):
                        st.subheader("Purchases & Sub-contracts")

                        # Display data frame with purchases details
                        st.dataframe(pr_df)

                        amount_range = st.slider('Select Amount Range', min_value=0.0, max_value=max(pr_df['Value']), value=(0.0, max(pr_df['Value'])))

                        # Filter data based on amount range
                        filtered_data = pr_df[(pr_df['Value'] >= amount_range[0]) & (pr_df['Value'] <= amount_range[1])]

                        # Create the bar plot for Purchases
                        colors = plt.cm.coolwarm(pr_df['Value'] / float(max(pr_df['Value'])))
                        fig, ax = plt.subplots(figsize=(14, 10))
                        ax.barh(filtered_data['Category'], filtered_data['Value'], color=colors)

                        # Customize plot
                        ax.set_xlabel('Amount ($)')
                        ax.set_ylabel('Type')
                        ax.set_title('Amounts by Type in P069 - Phase 4')
                        ax.invert_yaxis()
                        plt.tight_layout()

                        # Display the plot
                        st.pyplot(fig)

                # Monthly Purchases Section
                # with st.expander("Monthly Purchases Section"):
                #         st.subheader("Monthly Purchases")

                #         # Display data frame with monthly purchases details
                #         st.dataframe(porch_df)

                #         # Create the bar plot for Monthly Purchases
                #         plt.figure(figsize=(14, 6))
                #         porch_df.plot(kind='bar', x='Month/Year', y='Total', ax=plt.gca(), alpha=0.7)
                #         plt.xlabel('Month/Year')
                #         plt.ylabel('Amount')
                #         plt.xticks(rotation=90, fontsize=20)
                #         plt.yticks(fontsize=20)
                #         plt.title('Total Expenses by Type and Monthly Expenses', fontsize=24)
                #         plt.legend(title='Expense Type')
                #         plt.grid(axis='y')

                #         # Display the plot
                #         st.pyplot(plt)

                # Total Expenses Section
                with st.expander("Total Expenses Section"):
                        st.subheader("Total expenses and Purchases table")

                        # Display data frame with total expenses and purchases
                        st.dataframe(total_tbl[["Purchase", "Accommodations", "Per Diem + Kilometers"]])

                        # Create the bar plot for Total Expenses
                        fig, ax = plt.subplots()

                        labels = ['Purchases Total', 'Accommodation Total', 'Per Diem Total']
                        values = [pr_df['Value'].sum(), total_tbl['Accommodations'].iloc[0], total_tbl['Per Diem + Kilometers'].iloc[0]]

                        # Select contrasting colors from different colormaps
                        colors = ['#1f77b4', '#ff7f0e', '#2ca02c']  # Blue, Orange, Green
                        ax.bar(labels, values, color=colors)

                        # Customize plot
                        ax.set_ylabel('Sum of Totals')
                        ax.set_title('Comparison of Totals from Purchases, Per Diem, and Accommodations')

                        # Display the plot
                        st.pyplot(fig)

        elif selected_section == ":clock2: Hours and Overtime":
                st.title("P069 Phase 3 Hours and Overtime")

                # Define your KPI metrics
                metrics_data = {
                        'Project Length': weekly_aggregate['week'].count(),
                        'Human Hours': ot_emp_df['Total_Hours'].sum(),
                        'Regular Hours': ot_emp_df['Regular_hours'].sum(),
                        'Overtime Hours': ot_emp_df['Overtime'].sum(),
                }

                # Display metrics data in two rows
                # First row of metrics
                col1, col2, col3, col4 = st.columns(4)
                with col1:
                        st.metric(label='Phase Length', value=f"{metrics_data['Project Length']} weeks")
                with col2:
                        st.metric(label='Human Hours', value=f"{metrics_data['Human Hours']}")
                with col3:
                        st.metric(label='Regular Hours', value=f"{metrics_data['Regular Hours']}")
                with col4:
                        st.metric(label='Overtime Hours', value=f"{metrics_data['Overtime Hours']}")

                with st.expander("Overtime and Regular Hours"):
                        # st.subheader("Total expenses and Purchases table")
                        tab1, tab2, tab3 = st.tabs(["Weekly", "Per Employee", "Per Task"])
                        with tab1:
                                st.header("Weekly OT and Regular Hours")
                                st.dataframe(weekly_aggregate)
                                plt.figure(figsize=(17, 7))

                                # Plot regular hours and overtime hours
                                plt.bar(weekly_aggregate['week'], weekly_aggregate['overtime'], label='Overtime', color='#FFB74D')
                                plt.bar(weekly_aggregate['week'], weekly_aggregate['regular_hours'], bottom=weekly_aggregate['overtime'], label='Regular Hours', color='#00FA9A')

                                # Add labels and title
                                plt.xlabel('Week')
                                plt.ylabel('Hours')
                                plt.title('Regular Hours and Overtime Hours per Week', fontsize=20)
                                plt.xticks(weekly_aggregate['week'], rotation=90, fontsize=16)
                                plt.yticks(fontsize=16)
                                 # Add grid for better readability
                                plt.grid(color='gray', linestyle='-', linewidth=0.6)
                                plt.legend()
                                # plt.tight_layout()
                                # Show plot
                                st.pyplot(plt)

                                # Plotting pie
                                # Using bright colors that contrast well with a dark theme
                                colors = ['#2e8b57', '#CD5C5C'] 
                                fig, ax = plt.subplots(figsize=(7, 5))
                                ax.pie([total_regular_hours, total_overtime], labels=['Regular Hours', 'Overtime'], autopct='%1.1f%%', colors=colors)
                                ax.set_title('Total Distribution of Regular Hours and Overtime Hours')
                                plt.tight_layout()
                                # Show plot
                                st.pyplot(plt)
                        with tab2:
                                # Display the styled DataFrame
                                # ot_emp_df = overtime_emp_df.groupby('Employee').agg({
                                # 'Task':'first',
                                # 'Regular_hours':'sum',
                                # 'Overtime':'sum'
                                # }).reset_index() 

                                # ot_emp_df['Total_Hours']= ot_emp_df['Regular_hours']+ot_emp_df['Overtime']
                                # ot_emp_df.style
                                st.dataframe(ot_emp_df)
                                # Plotting
                                # Plotting
                                plt.figure(figsize=(10, 6))
                                width1 = 0.5
                                # Plot regular hours and overtime hours

                                plt.bar(ot_emp_df['Employee'], ot_emp_df['Regular_hours'], label='Regular Hours')
                                plt.bar(ot_emp_df['Employee'], ot_emp_df['Overtime'], label='Overtime Hours')

                                # Add labels and title
                                plt.xlabel('Employee')
                                plt.ylabel('Hours')
                                plt.title('Regular Hours and Overtime Hours per Employee')
                                plt.xticks(overtime_emp_df['Employee'],rotation=90)
                                 # Add grid for better readability
                                plt.grid(color='gray', linestyle='-', linewidth=0.6)
                                plt.legend()
                                # plt.tight_layout()
                                # Show plot
                                st.pyplot(plt)
                        with tab3:
                                st.dataframe(overtime_task_df)
                                # Plotting
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
                                 # Add grid for better readability
                                plt.grid(color='gray', linestyle='-', linewidth=0.6)
                                # plt.tight_layout()
                                # Show plot
                                st.pyplot(plt)
                with st.expander("Project Length"):
                        st.subheader("Project Length Table and Chart")
                        
                        st.dataframe(phase3_df)
                        #Plot
                        # Set the seaborn style
                        # sns.set_theme(style="whitegrid")

                       # Create a figure and a set of subplots
                        fig, ax1 = plt.subplots(figsize=(20, 10))

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
                        st.pyplot(plt)
                with st.expander("Overlaps and Human Hour Cost"):       
                        st.subheader("Overlapping Tasks chart:")
                        st.write("Here we plot all the tasks in chronological order, so that we can spot any overlap. The red dots on top of the bars represent the total human hours for that week.")

                       # Task options for plotting
                        task_options = ['Foundation', 'Groundwork', 'Framing', 'Roofing', 'Cladding/Siding']

                        # Dropdown for task selection
                        selected_tasks = st.multiselect('Select tasks to plot:', task_options, default=task_options)

                        # Plotting
                        plt.figure(figsize=(20, 10))

                        # Check and plot each selected task
                        if 'Foundation' in selected_tasks:
                                plt.hist(foundation_tdf['week'], weights=foundation_tdf['hour_column'], 
                                bins=50, alpha=0.5, label='Foundation')

                        if 'Groundwork' in selected_tasks:
                                plt.hist(groundwork_tdf['week'], weights=groundwork_tdf['hour_column'], 
                                bins=50, alpha=0.5, label='Groundwork')

                        if 'Framing' in selected_tasks:
                                plt.hist(framing_tdf['week'], weights=framing_tdf['hour_column'], 
                                bins=50, alpha=0.5, label='Framing')

                        if 'Roofing' in selected_tasks:
                                plt.hist(roofing_tdf['week'], weights=roofing_tdf['hour_column'], 
                                bins=50, alpha=0.5, label='Roofing')

                        if 'Cladding/Siding' in selected_tasks:
                                plt.hist(cs_tdf['week'], weights=cs_tdf['hour_column'], 
                                bins=50, alpha=0.5, label='Cladding/Siding')

                        plt.scatter(phase3_time_df['week'], phase3_time_df['hour_column'], color='red', label='Total Human Hours')
                        
                        plt.xticks(rotation=90)
                        plt.legend(loc='upper right') 
                        plt.ylabel('Human hours',fontsize=20)
                        plt.xlabel('Weeks', fontsize=20)
                        plt.xticks(fontsize=20)
                        plt.yticks(fontsize=20)
                        plt.title('Overlapping Phase 3 Tasks', fontsize=24) 
                        # Add grid for better readability
                        plt.grid(color='gray', linestyle='-', linewidth=0.6)
                        # Display plot in Streamlit
                        st.pyplot(plt)
