#!/usr/bin/env python
# coding: utf-8

# The global economy was unprepared for the first wave of the COVID-19 pandemic, resulting in a significant impact on various sectors. This includes an increase in cases, deaths, unemployment, and poverty, leading to a slowdown in economic activity. As part of this analysis, we will investigate the spread of COVID-19 cases and its effects on the economy.
# 
# To conduct this analysis, we will utilize a dataset downloaded from Kaggle, which includes the following information:
# 
# Country code
# Country name
# Date of the record
# Human development index of all countries
# Daily COVID-19 cases
# Daily deaths attributed to COVID-19
# Stringency index of the countries
# Population of the countries
# GDP per capita of the countries

# In[33]:


#  Importing the necessary Python libraries and the dataset:

import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import pygwalker as pyg

data = pd.read_csv("C:\\Users\\owner\\Downloads\\COVID_Data\\transformed_data.csv")
data2 = pd.read_csv("C:\\Users\\owner\\Downloads\\COVID_Data\\raw_data.csv")
print(data)
pyg.walk(data)


# Data Preparation
# The dataset we are working with consists of two files, one containing raw data and the other containing transformed data. To complete this task effectively, we need to utilize both datasets since they contain important information in different columns. Therefore, let's examine both datasets individually.

# In[34]:


print(data.head())
pyg.walk(data.head())


# In[35]:


print(data2.head())
pyg.walk(data2.head())


# Upon examining both datasets, it became apparent that a new dataset would need to be created by merging the two. However, before proceeding with the creation of a new dataset, it is essential to determine the number of samples available for each country in the dataset.

# In[37]:


data["COUNTRY"].value_counts()


# The dataset does not have an equal distribution of samples for each country. Let's examine the mode value:

# In[38]:


data["COUNTRY"].value_counts().mode()


# The mode value is 294, which we will use to divide the sum of all samples related to the human development index, GDP per capita, and population. Subsequently, we will create a new dataset by merging the relevant columns from both datasets.

# In[40]:


# Aggregating the data

code = data["CODE"].unique().tolist()
country = data["COUNTRY"].unique().tolist()
hdi = []
tc = []
td = []
sti = []
population = data["POP"].unique().tolist()
gdp = []

for i in country:
    hdi.append((data.loc[data["COUNTRY"] == i, "HDI"]).sum()/294)
    tc.append((data2.loc[data2["location"] == i, "total_cases"]).sum())
    td.append((data2.loc[data2["location"] == i, "total_deaths"]).sum())
    sti.append((data.loc[data["COUNTRY"] == i, "STI"]).sum()/294)
    population.append((data2.loc[data2["location"] == i, "population"]).sum()/294)

aggregated_data = pd.DataFrame(list(zip(code, country, hdi, tc, td, sti, population)), 
                               columns = ["Country Code", "Country", "HDI", 
                                          "Total Cases", "Total Deaths", 
                                          "Stringency Index", "Population"])
print(aggregated_data.head())
pyg.walk(aggregated_data.head())


# I have excluded the GDP per capita column from the dataset as I did not find accurate figures for it. Therefore, it would be best to manually gather data on the GDP per capita of the countries. However, since this dataset includes many countries, it would be challenging to manually collect GDP per capita data for all of them. Thus, to create a subsample, I will choose the top 10 countries with the highest number of Covid-19 cases, which will be an ideal sample for studying the economic consequences of the pandemic. Therefore, I will sort the data by total Covid-19 cases to create this subsample.

# In[41]:


# Sorting Data According to Total Cases

data = aggregated_data.sort_values(by=["Total Cases"], ascending=False)
print(data.head())
pyg.walk(data.head())


# # Top 10 Countries with Highest Covid Cases
# 

# In[42]:


# Top 10 Countries with Highest Covid Cases

data = data.head(10)
print(data)
pyg.walk(data)


# Next, I will append two additional columns to this dataset, namely the GDP per capita before Covid-19 and the GDP per capita during Covid-19.
# Note: The data about the GDP per capita is collected manually.

# In[43]:


data["GDP Before Covid"] = [65279.53, 8897.49, 2100.75, 
                            11497.65, 7027.61, 9946.03, 
                            29564.74, 6001.40, 6424.98, 42354.41]
data["GDP During Covid"] = [63543.58, 6796.84, 1900.71, 
                            10126.72, 6126.87, 8346.70, 
                            27057.16, 5090.72, 5332.77, 40284.64]
print(data)
pyg.walk(data)


# To begin with, let's analyze the spread of Covid-19 in the countries with the highest number of cases. Firstly, we will examine the countries that have recorded the highest number of Covid-19 cases.

# In[25]:


figure = px.bar(data, y='Total Cases', x='Country',
            title="Countries with Highest Covid Cases")
figure.show()
pyg.walk(figure.show())


# Let's examine the COVID-19 spread among the countries with the highest number of cases. Firstly, we can observe that the USA has a significantly higher number of COVID-19 cases as compared to Brazil and India, which are in the second and third positions, respectively. Next, we will explore the total number of deaths in the same countries.

# In[26]:


figure = px.bar(data, y='Total Deaths', x='Country',
            title="Countries with Highest Deaths")
pyg.walk(figure.show())


# Let's compare the total number of cases and deaths in all of these countries. As we can see, the USA has the highest number of Covid-19 cases and deaths, followed by Brazil and India in the second and third positions. It's worth noting that India, Russia, and South Africa have a comparatively lower death rate based on the total number of cases.

# In[27]:


fig = go.Figure()
fig.add_trace(go.Bar(
    x=data["Country"],
    y=data["Total Cases"],
    name='Total Cases',
    marker_color='indianred'
))
fig.add_trace(go.Bar(
    x=data["Country"],
    y=data["Total Deaths"],
    name='Total Deaths',
    marker_color='lightsalmon'
))
fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.show()
pyg.walk(fig.show())


# Let us now examine the proportion of the total number of cases and total deaths in relation to all the countries with the highest number of Covid-19 cases.

# In[28]:


# Percentage of Total Cases and Deaths
cases = data["Total Cases"].sum()
deceased = data["Total Deaths"].sum()

labels = ["Total Cases", "Total Deaths"]
values = [cases, deceased]

fig = px.pie(data, values=values, names=labels, 
             title='Percentage of Total Cases and Deaths', hole=0.5)
fig.show()
pyg.walk(fig.show())


# In[14]:


# Below is how you can calculate the death rate of Covid-19 cases:
death_rate = (data["Total Deaths"].sum() / data["Total Cases"].sum()) * 100
print("Death Rate = ", death_rate)


# The stringency index is a significant column in this dataset, as it reflects the measures taken by countries to control the spread of covid-19. It is a combined measure of response indicators, such as school and workplace closures, and travel bans.

# In[30]:


fig = px.bar(data, x='Country', y='Total Cases',
             hover_data=['Population', 'Total Deaths'], 
             color='Stringency Index', height=400, 
             title= "Stringency Index during Covid-19")
fig.show()
pyg.walk(fig.show())


# Above we can see that India is performing well in the stringency index during the outbreak of covid-19.

# Analyzing Covid-19 Impacts on Economy
# Now let’s move to analyze the impacts of covid-19 on the economy. Here the GDP per capita is the primary factor for analyzing the economic slowdowns caused due to the outbreak of covid-19. Let’s have a look at the GDP per capita before the outbreak of covid-19 among the countries with the highest number of covid-19 cases:

# In[32]:


fig = px.bar(data, x='Country', y='Total Cases',
             hover_data=['Population', 'Total Deaths'], 
             color='GDP Before Covid', height=400, 
             title="GDP Per Capita Before Covid-19")
fig.show()


# Now let’s have a look at the GDP per capita during the rise in the cases of covid-19:

# In[17]:


fig = px.bar(data, x='Country', y='Total Cases',
             hover_data=['Population', 'Total Deaths'], 
             color='GDP During Covid', height=400, 
             title="GDP Per Capita During Covid-19")
fig.show()


# Next, we will compare the GDP per capita before and during the covid-19 outbreak to evaluate the impact of the pandemic on GDP per capita.

# In[18]:


fig = go.Figure()
fig.add_trace(go.Bar(
    x=data["Country"],
    y=data["GDP Before Covid"],
    name='GDP Per Capita Before Covid-19',
    marker_color='indianred'
))
fig.add_trace(go.Bar(
    x=data["Country"],
    y=data["GDP During Covid"],
    name='GDP Per Capita During Covid-19',
    marker_color='lightsalmon'
))
fig.update_layout(barmode='group', xaxis_tickangle=-45)
fig.show()


# The countries with the highest number of covid-19 cases have experienced a decline in GDP per capita, as observed in the previous comparison. Another essential economic factor is the Human Development Index, which is a composite statistic of life expectancy, education, and per capita indicators. Let's examine how many countries have allocated their budget to human development:

# In[19]:


fig = px.bar(data, x='Country', y='Total Cases',
             hover_data=['Population', 'Total Deaths'], 
             color='HDI', height=400, 
             title="Human Development Index during Covid-19")
fig.show()


# In this analysis, I explored the impact of Covid-19 on the global economy and analyzed the spread of the virus across various countries. I observed that the United States had the highest number of Covid-19 cases and deaths, with the country's low stringency index being a contributing factor. Additionally, I analyzed the effect of Covid-19 on GDP per capita in the countries with the highest number of cases, and observed a decline in GDP per capita. Finally, I looked at the budget allocation for human development in various countries. I hope this analysis was insightful, and welcome any questions or feedback in the comments section below.
