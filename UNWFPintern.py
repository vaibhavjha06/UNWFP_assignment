import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

data = pd.read_csv('/Users/vaibhavjha/Documents/Internships 2025/UN WFP/Active_Monthly_Gifts.csv')
print(data.columns)
print(data.head())


# In May 2022, how many unique Core, Mid-Level, and Major donors provided active monthly gifts?

# Step 1: isolate donors by type
typeCore = data[data['account_type'] == 'Core']
typeMidlevel = data[data['account_type'] == 'Mid-Level']
typeMajor = data[data['account_type'] == 'Major']

# Step 2: filter for just May 2022
typeCoremay22 = typeCore[typeCore['donation_date'].str.startswith('2022-05-')]
typeMidlevelmay22 = typeMidlevel[typeMidlevel['donation_date'].str.startswith('2022-05-')]
typeMajormay22 = typeMajor[typeMajor['donation_date'].str.startswith('2022-05-')]

# Step 3: get counts for unique donor numbers
print(typeCoremay22['donor_id'].nunique()) # 3555 unique Core donors
print(typeMidlevelmay22['donor_id'].nunique()) # 211 unique Mid-Level donors
print(typeMajormay22['donor_id'].nunique()) # 5 unique Major donors


# In the year 2021, how much monthly revenue, on average, did active monthly gifts account for?

# Step 1: filter for 2021 data
fy2021 = data[data['donation_date'].str.startswith('2021-')]

# Step 2: convert to datetime format
fy2021['donation_date'] = pd.to_datetime(fy2021['donation_date'], format='%Y-%m-%d')

# Step 3: group_by and calculate averages by month
monthly_average = (fy2021.groupby(fy2021['donation_date'].dt.month)['donation_amount'].mean())
print(monthly_average.mean())

"""
1     41.237516
2     34.112120
3     33.992902
4     33.271451
5     34.159889
6     34.280498
7     34.552359
8     34.387405
9     34.153749
10    33.922261
11    63.448006
12    39.572169
"""

# Average is 37.59

# In months, what is the average length of time donors with active monthly gifts remain active? Assume no active monthly gifts were received prior to January 2021.

# Step 0: convert dates to datetime format
diff = data.copy()
diff['donation_date'] = pd.to_datetime(diff['donation_date'], format='%Y-%m-%d')   

# Step 1: calculate number of months per person
magnitude = diff.groupby('donor_id')['donation_date'].count()

# Step 2: average all calculations
print(np.average(magnitude))

# 8.84 months is the average length of time donors with active monthly gifts remain active


# What was the overall donor retention rate between 2021 and May 2022? In other words, what percent of donors who gave in 2021 returned to give a subsequent gift the following year?

# Step 1: Find donors that gave anytime during 2021
early = data.copy()
early['donation_date'] = pd.to_datetime(early['donation_date'], format='%Y-%m-%d')
early = early[early['donation_date'].dt.year == 2021] # filtered for just 2021 data
early = early.drop_duplicates(subset='donor_id') # not necessary
print(early['donor_id'].nunique())

# Step 2: Find donors that gave anytime during 2022
late = data.copy()
late['donation_date'] = pd.to_datetime(late['donation_date'], format ='%Y-%m-%d')
late = late[late['donation_date'].dt.year == 2022] # filtered for just 2022 data
late = late.drop_duplicates(subset='donor_id') # not necessary
print(late['donor_id'].nunique())

# Step 3: See overlap in donors between years. Compare donor_id and count number of ids that are in both cases
ids_early = set(early['donor_id'])
ids_late = set(late['donor_id'])

common = ids_early.intersection(ids_late)
print(len(common)) # 3156 donors overlap between years

# Step 4: Divide those that match by number of 2021 donors | Donor retention rate = Matches between years / number of donors in 2021
print(len(common)/len(ids_early))

# 73.6% of donors from 2021 donate in 2022


# Please provide any additional analysis, visualizations, or commentary that helps tell a story about the donors and their journey.

# Question: Study how donation_source is related to donation_amount 
#   Ideas to consider: What donation_source results in the most amount of donations? Where should the organization invest resources into in order to increase donation amounts?

#   Step 1: Produce visualization of donation fluctuations by donation_source over months
        # Consider data by month/year
        # Line graph

viz = data.copy()
viz['donation_date'] = pd.to_datetime(viz['donation_date'], format ='%Y-%m-%d')
viz['year_month'] = viz['donation_date'].dt.to_period('M').astype(str) # create year-month column for x-axis of graph
monthly_totals = viz.groupby(['year_month', 'donation_source'])['donation_amount'].sum().reset_index()
sns.lineplot(data = monthly_totals, x = 'year_month', y = 'donation_amount', hue = 'donation_source', marker = 'o')
plt.title('Donations Totals over Time')
plt.xlabel('Month/Year')
plt.xticks(rotation = 90)
plt.ylabel('Donation Amount')
plt.grid(True)
plt.show()

# Donations are predominantly coming from the website. Significant number from ads. Else, negligible.

#   Step 2: Look at how donation_source is related to account_type
print(type(viz['donation_source']))
print(pd.crosstab(viz['donation_source'], viz['account_type']))

# Most donors are Core donors
# Most avenues for donations are websites


#   Step 3: Make conclusions
#   Websites prove most capable for gathering donations. This depends on the methodology used to collect the data and accessibility of donation sources across donors. Further studies should look into this matter.
