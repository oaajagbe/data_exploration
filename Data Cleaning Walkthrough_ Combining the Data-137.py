## 3. Condensing the Class Size Dataset ##

class_size = data["class_size"]
class_size = class_size[class_size["GRADE "] == "09-12"]
class_size = class_size[class_size["PROGRAM TYPE"] == "GEN ED"]
class_size.head()

## 5. Computing Average Class Sizes ##

import numpy as np

# Find the average values for each column associated with each DBN in class_size.
class_size = class_size.groupby("DBN").agg(np.mean)
class_size.reset_index(inplace=True)
data["class_size"] = class_size
data["class_size"].head()

## 7. Condensing the Demographics Dataset ##

# Filter demographics, only selecting rows in data["demographics"] where schoolyear is 20112012.
# schoolyear is actually an integer, so be careful about how you perform your comparison.
data["demographics"] = data["demographics"][data["demographics"]["schoolyear"] == 20112012].head()
# data["demographics"].head()

## 9. Condensing the Graduation Dataset ##

# Filter graduation, only select rows where the Cohort column equals 2006
data["graduation"] = data["graduation"][data["graduation"]["Cohort"] == "2006"]

# Filter graduation, only select rows where the Demographic column equals Total Cohort
data["graduation"] = data["graduation"][data["graduation"]["Demographic"] == "Total Cohort"]
data["graduation"].head()

## 10. Converting AP Test Scores ##

cols = ['AP Test Takers ', 'Total Exams Taken', 'Number of Exams with scores 3 4 or 5']

# Convert each of the following columns in ap_2010 to numeric values using the pandas.to_numeric() function with the keyword argument errors="coerce".

for c in cols:
    data["ap_2010"][c] = pd.to_numeric(data["ap_2010"][c], errors="coerce")
    
data["ap_2010"].dtypes

## 12. Performing the Left Joins ##

combined = data["sat_results"]
combined = combined.merge(data["ap_2010"], on="DBN", how="left")
combined = combined.merge(data["graduation"], on="DBN", how="left")
print(combined.head(5))
print(combined.shape)

## 13. Performing the Inner Joins ##

combined = combined.merge(data["class_size"], on="DBN", how="inner")
combined = combined.merge(data["demographics"], on="DBN", how="inner")
combined = combined.merge(data["survey"], on="DBN", how="inner")
combined = combined.merge(data["hs_directory"], on="DBN", how="inner")
combined.head()
combined.shape

## 15. Filling in Missing Values ##

combined = combined.fillna(combined.mean()) #Fill in any missing values in combined with the means of the respective columns
combined = combined.fillna(0) #Fill in any remaining missing values in combined with 0
print(combined.head(5))

## 16. Adding a School District Column for Mapping ##

def extract2xters(char):
    return char[0:2]

combined["school_dist"] = combined["DBN"].apply(extract2xters)
combined["school_dist"].head()