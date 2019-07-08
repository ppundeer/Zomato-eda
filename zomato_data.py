import pandas as pd
import numpy  as np
import os
import matplotlib.pyplot as plt
import seaborn as sns

zdata = pd.read_csv('C:\Users\hp\Desktop\zomato data\zomato.csv',encoding='ISO-8859-1')
country = pd.read_excel('C:\Users\hp\Desktop\zomato data\Country-Code.xlsx')
data = pd.merge(zdata, country, on='Country Code')

#No. of restaurants by country
data_country = data.groupby(['Country'], as_index=False).count()[['Country', 'Restaurant ID']]
data_country.columns = ['Country', 'No of Restaurant']
print data_country
plt.bar(data_country['Country'], data_country['No of Restaurant'])
plt.rcParams['figure.figsize']=(30,20)
plt.xlabel('Country', fontsize=20)
plt.ylabel('No of Restaurant', fontsize=20)
plt.xticks(rotation = 75)

## --------------------- Analysis of Indian restaurants --------------------- ##

Ind_rest = data[data.Country == 'India']

# Average rating against number of Indian restaurants
f, ax = plt.subplots(1,1, figsize = (15, 4))
ax = sns.countplot(Ind_rest[Ind_rest['Aggregate rating'] != 0]['Aggregate rating'])
ax.set_title('Rating vs Number of Indian Restaurants')

''' Remark: Most restaurants seems to have an average rating '''

#Most favoured cuisine
total_cuisines = Ind_rest.Cuisines.value_counts()
cuisines = {}
cnt = 0
for i in total_cuisines.index:
    for j in i.split(', '):
        if j not in cuisines.keys():
            cuisines[j] = total_cuisines[cnt]
        else:
            cuisines[j] += total_cuisines[cnt]
    cnt += 1
sorted_cuisines = pd.Series(cuisines).sort_values(ascending=False)

f, ax = plt.subplots(1,1, figsize = (15, 4))
ax = sns.barplot(sorted_cuisines[:15].index, sorted_cuisines[:15].values, palette="inferno")
ax.set_title('Most Popular Cuisines')

''' Remark: North Indian food is the most popular served cuisine'''

# Online delivery
f, g = plt.subplots(1,1, figsize = (10, 10))
g = sns.countplot(Ind_rest['Has Online delivery'])
''' Remark: Most restaurants don't deliver via online order.
            This appears to be untapped business opportunity.'''

# Cost distribution of Indian restraurants
f, ax = plt.subplots(figsize=[16,4])
ax = sns.distplot(Ind_rest['Average Cost for two'])
ax.set_title('Cost Distribution for Indian restaurants')

plt.show()

## Finding the best restaurants with criteria:
#   cheapest
#   highly rated
#   reliable (large number of votes)

# Step 1 : find restaurants with average cost for two less than Rs.1000.
new = Ind_rest[['Restaurant ID','Restaurant Name','Locality','Average Cost for two']].groupby(['Average Cost for two'], sort = True)
new = new.filter(lambda x: x['Average Cost for two'].mean() <= 1000)
new = new.sort_values(by=['Average Cost for two'])
#print new

# Step 2 : find restaurants with rating > 4.5/5
new_rate = Ind_rest[['Restaurant ID','Aggregate rating']].groupby(['Aggregate rating'], sort = True)
new_rate = new_rate.filter(lambda x: x['Aggregate rating'].mean() >= 4.5)
new_rate = new_rate.sort_values(by=['Aggregate rating'])
#print new_rate

# Step 3 : now we merge both dataframes to get intersection of
#          low cost and high rated restaurants
s1 = pd.merge(new_rate, new, how='inner', on=['Restaurant ID'])
#print("List of cheap restaurants with high rating \n")
#print s1

# Step 4 : filtering for mean number of votes > 150
new_votes = Ind_rest[['Restaurant ID','Votes']].groupby(['Votes'], sort = True)
new_votes = new_votes.filter(lambda x: x['Votes'].mean() > 150)
new_votes = new_votes.sort_values(by=['Votes'])
#print new_votes

s = pd.merge(s1, new_votes, how='inner', on=['Restaurant ID'])
s = s.sort_values(by=['Aggregate rating'])
print("List of reliable high rated restaurants with low cost")
print s

