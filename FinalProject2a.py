#!/usr/bin/env python
# coding: utf-8

# In[33]:


import dash
import itertools
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.graph_objs as go
import plotly.express as px


# In[34]:


# Load the data using pandas
data = pd.read_csv('https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-DV0101EN-SkillsNetwork/Data%20Files/historical_automobile_sales.csv')


# In[35]:


data


# In[36]:


# Initialize the Dash app
app = dash.Dash(__name__)


# In[37]:


# Set the title of the dashboard
app.title = 'Automobile Statistics Dashboard'


# In[38]:


# Create the dropdown menu options
dropdown_options = [
    {'label':'Yearly Statistics', 'value':'Yearly Statistics'},
    {'label':'Recession Period Statistics', 'value':'Recession Period Statistics'}
]
# List of years 
year_list = [i for i in range(1980, 2024, 1)]


# In[39]:


# Create the layout of the app
app.layout = html.Div([
#TASK 2.1 Add title to the dashboard
    
    html.H1("Automobile Sales Statistics Dashboard",
        style={'textAlign':'center', 'color':'#503D36', 'font-size':24}),
    
    html.Div([#TASK 2.2: Add two dropdown menus
        html.Label("Select Statistics:"),
        dcc.Dropdown(
            id = 'dropdown-statistics',
            options =[
                {'label':'Yearly Statistics', 'value':'Yearly Statistics'},
                {'label':'Recession Period Statistics', 'value':'Recession Period Statistics'}
            ],
            value ='Select Statistics',
            placeholder ='Select a report type'
        )
    ]),
    
    html.Div(
        dcc.Dropdown(
            id = 'select-year', 
            options = [
                {'label': i, 'value': i} for i in year_list],
            placeholder = 'Select a year'
        )
    ),
 
#TASK 2.3: Add a division for output display 
    html.Div([
        html.Div(
            id = 'output-container', 
            className = 'chart-grid', 
            style = {'display':'flex'}), 
    ])
])


# In[40]:


# TASK 2.4: Creating Callbacks
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id = 'select-year', component_property = 'disabled'),
    Input(component_id = 'dropdown-statistics', component_property='value'))

def update_input_container(value):
    if value =='Yearly Statistics': 
        return False
    else: 
        return True 


# In[41]:


# Callback for plotting
# Define the callback function to update the input container based on the selected statistics
@app.callback(
    Output(component_id = 'output-container', component_property = 'children'),
    [Input(component_id = 'dropdown-statistics', component_property = 'value'), Input(component_id = 'select-year', component_property = 'value')])

def update_output_container(dropdown_statistics, select_year):
    if dropdown_statistics == 'Recession Period Statistics':
        # Filter the data for recession periods
        recession_data = data[data['Recession'] == 1]
        
#TASK 2.5: Create and display graphs for Recession Report Statistics

#Plot 1 Automobile sales fluctuate over Recession Period (year wise) using line chart
        yearly_rec = recession_data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        # Plotting for line chart
        R_Chart1 = dcc.Graph(
            figure = px.line(yearly_rec,
                    x = 'Year',
                    y = 'Automobile_Sales',
                    title = "Automobile Sales over Recession Period")
        )
        
        # Average Monthly Automobile sales of each vehicle type
        average_sales = df.groupby('Vehicle_Type')['Automobile_Sales'].mean().reset_index() 
                                   
        # Plotting for bar chart 
        R_chart2  = dcc.Graph(
            figure = px.bar(average_sales,
                    x = ['Automobile_Sales'],
                    y = ['Vehicle_Type'],
                    title = 'Average Number of Vehicles Sold by Vehicle Type')
        )
                                   
        # Pie chart for total expenditure share by vehicle type during recessions
        exp_rec= recession_data.groupby('Advertising_Expenditure')
                                   
        # Plotting for pie chart 
        R_chart3 = dcc.Graph(
            figure=px.pie(
                    values = 'exp_rec',
                    names = 'Vehicle_Type',
                    title = "Total Expenditure Share by Vehicle Type During Recessions"
                )
        )
        
        # Effect of unemployment rate on vehicle type and sales 
        unemp_rate = df.groupby(['unemployment_Rate', 'Vehicle_Type'])['Automobile_Sales'].mean().reset_index()    
                                
        # Plotting for bar chart                        
        R_chart4  = dcc.Graph(
            figure = px.bar(unemp_rate,
                x = 'unemployment_Rate',
                y = 'Automobile_Sales',
                labels = {'unemployment_rate': 'Unemployment Rate', 'Automobile_Sales': 'Average Automobile Sales'},
                title = 'Effect of Unemployment Rate on Vehicle Type and Sales')
        )
        
        return [
            html.Div(className='chart-item', children=[html.Div(children=R_Chart1),html.Div(children=R_chart2)]),
            html.Div(className='chart-item', children=[html.Div(children=R_chart3),html.Div(children=R_chart4)])
        ]

    elif (input_year and selected_statistics == 'Yearly Statistics'):
        yearly_data = data[data['Year'] == value]
        
# Create and display graphs for Yearly Statistics report

        # Plot 1 :Yearly Automobile sales using line chart for the whole period.
        yas= data.groupby('Year')['Automobile_Sales'].mean().reset_index()
        Y_chart1 = dcc.Graph(
            figure=px.line(
                x = yas, 
                y = 'Automobile_Sales',
                title = 'Yearly Automobile Sales')
        )
        
        # Plot 2 :Total Monthly Automobile sales using line chart.
        tmas= data.groupby('Month')['Automobile_Sales'].mean().reset_index(),
        Y_chart2 = dcc.Graph(
            figure = px.line(
                x = tmas,
                y = 'Automobile_Sales',
                title = 'Monthly Automobile Sales')
        )
        
        # Plot 3 bar chart for average number of vehicles sold during the given year
        avr_vdata = yearly_data.groupby('Year')['Automobile_Sales'].mean().reset_index(),
        Y_chart3 = dcc.Graph(
            figure = px.bar(
            x = avr_vdata,
            y = 'Automobile_Sales',
            title='Average Vehicles Sold by Vehicle Type in the year {}'.format(input_year)))

        # Plot 4 Total Advertisement Expenditure for each vehicle using pie chart
        exp_rec= yearly_data.groupby('Vehicle_Type')['Advertising_Expenditure'].sum().reset_index()
        Y_chart4 = dcc.Graph(
            figure = px.pie(exp_rec,
            values = 'Advertising_Expenditure',
            names = 'Vehicle_Type',
            title = "Total Expenditure Share by Vehicle Type During Recessions"
        )
    )

        return [
            html.Div(className = 'chart-item', children = [html.Div(children = Y_chart1),html.Div(children = Y_chart2)],style = {'display': 'flex'}),
            html.Div(className = 'chart-item', children = [html.Div(children = Y_chart3),html.Div(children = Y_chart4)],style = {'display': 'flex'})
            ]


# In[42]:


if __name__ == '__main__':
    app.run_server()


# In[ ]:




