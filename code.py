# For this capstone project we will be analyzing some 911 call data from Kaggle. The data contains the following fields:

# lat : String variable, Latitude
# lng: String variable, Longitude
# desc: String variable, Description of the Emergency Call
# zip: String variable, Zipcode
# title: String variable, Title
# timeStamp: String variable, YYYY-MM-DD HH:MM:SS
# twp: String variable, Township
# addr: String variable, Address
# e: String variable, Dummy variable (always 1)
 
## Data and Setup
#** Import numpy ,pandas, matplot and seaborn**
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

##** Read in the csv file as a dataframe called df **
df = pd.read_csv('911.csv')

##** Check the info() of the df **
df.info()

##** Check the head of df **
df.head()

## Basic Questions- Answering 
#** What are the top 5 zipcodes for 911 calls? **
df.zip.value_counts().nlargest(5)

#** What are the top 5 townships (twp) for 911 calls? **
df.twp.value_counts().nlargest(5)

#** Take a look at the 'title' column, how many unique title codes are there? **
df.title.nunique()

## Creating new features
#* In the titles column there are "Reasons/Departments" specified before the title code. These are EMS, Fire, and Traffic. 
# Use .apply() with a custom lambda expression to create a new column called "Reason" that contains this string value.**
#*For example, if the title column value is EMS: BACK PAINS/INJURY , the Reason column value would be EMS. *
df['Reason'] = df.title.apply(lambda x: x.split(':')[0]  )

#** What is the most common Reason for a 911 call based off of this new column? **
df.Reason.value_counts()

#** Now use seaborn to create a countplot of 911 calls by Reason. **
import seaborn as sns
sns.countplot(df.Reason)

#** Now let us begin to focus on time information. What is the data type of the objects in the timeStamp column? **
type(df.timeStamp.iloc[0])

#** You should have seen that these timestamps are still strings.
#Use pd.to_datetime to convert the column from strings to DateTime objects. **
df.timeStamp = pd.to_datetime(df.timeStamp)

# use .apply() to create 3 new columns called Hour, Month, and Day of Week. 
# You will create these columns based off of the timeStamp column, reference the solutions if you get stuck on this step.
#** Notice how the Day of Week is an integer 0-6. Use the .map() with this dictionary to map the actual string names to the day of the week: **

#dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}

df['Year'] = df.timeStamp.apply(lambda x: x.year)
df['Hour'] = df.timeStamp.apply(lambda x: x.hour)
df['Month'] = df.timeStamp.apply(lambda x: x.month)
df['Day'] = df.timeStamp.apply(lambda x: x.dayofweek)
dmap = {0:'Mon',1:'Tue',2:'Wed',3:'Thu',4:'Fri',5:'Sat',6:'Sun'}
df['Day_of_Week']= df['Day'].map(dmap)
df.head()

#** Now use seaborn to create a countplot of the Day of Week column with the hue based off of the Reason column. **
sns.countplot(x = "Day_of_Week", data = df, hue = "Reason")
plt.legend(loc='center right',bbox_to_anchor=(1.26, .9))

#** Now use seaborn to create a countplot of the Monthn with the hue based off of the Reason column. **
sns.countplot(x = "Month", data = df, hue = "Reason")
plt.legend(loc='center right',bbox_to_anchor=(1.26, .9))



#Did you notice something strange about the Plot?

#** You should have noticed it was missing some Months, let's see if we can maybe fill in this information by plotting 
# the information in another way, possibly a simple line plot that fills in the missing months, in order to do this, 
# we'll need to do some work with pandas... **

#** Now create a gropuby object called byMonth, where you group the DataFrame by the month column and 
# use the count() method for aggregation. Use the head() method on this returned DataFrame. **

byMonth = df.groupby('Month').count()
byMonth

#** Now create a simple plot off of the dataframe indicating the count of calls per month. **
sns.lineplot(y = 'lat', x = 'Month',data = byMonth)

#* Now see if you can use seaborn's lmplot() to create a linear fit on the number of calls per month. 
#Keep in mind you may need to reset the index to a column. **
byMonth.reset_index(inplace = True)
sns.lmplot(x = 'Month', y = 'twp', data = byMonth)

#*Create a new column called 'Date' that contains the date from the timeStamp column. 
#You'll need to use apply along with the .date() method. *

df["Date"] = df.timeStamp.apply(lambda x: x.date())
df.head()

#** Now groupby this Date column with the count() aggregate and create a plot of counts of 911 calls.**
byDate = df.groupby('Date').count()
byDate.reset_index(inplace = True)

fig = plt.figure(figsize = (8,4))
x1 = byDate.loc[ : ,['Date', 'twp']]
sns.lineplot(x = 'Date', y = 'twp', data = x1)
plt.tight_layout()

#** Now recreate this plot but create 3 separate plots with each plot representing a Reason for the 911 call**
fig = plt.figure(figsize = (8,4))
df.loc[df['Reason'] == 'EMS'].groupby('Date').count()['lat'].plot()
plt.tight_layout()
plt.title('EMS')

fig = plt.figure(figsize = (8,4))
plt.title('Traffic')
df.loc[df['Reason'] == 'Traffic'].groupby('Date').count()['lat'].plot()
plt.tight_layout()

fig = plt.figure(figsize = (8,4))
plt.title('Fire')
df.loc[df['Reason'] == 'Fire'].groupby('Date').count()['lat'].plot()
plt.tight_layout()

#** Now let's move on to creating heatmaps with seaborn and our data.
#We'll first need to restructure the dataframe so that the columns become the Hours and the Index becomes the Day of the Week.
dayhour = df.groupby(['Day_of_Week', 'Hour']).count()['Reason'].unstack()
dayhour

# Creating heatmap
fig = plt.figure(figsize = (12,4))
sns.heatmap(dayhour)

#** Now create a clustermap using this DataFrame. **
fig = plt.figure(figsize = (8,4))
sns.clustermap(dayhour)

#** Now repeat these same plots and operations, for a DataFrame that shows the Month as the column. **
wk_month = df.groupby(['Day_of_Week', 'Month']).count()['twp'].unstack()
wk_month

# Creating heatmap
fig = plt.figure(figsize = (8,4))
sns.heatmap(wk_month)

#** Now create a clustermap using this DataFrame. **
fig = plt.figure(figsize = (6,4))
sns.clustermap(wk_month)

print('Thank you')
print('end')