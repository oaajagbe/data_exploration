## 4. Reading in the Data ##

import pandas as pd
data_files = [
    "ap_2010.csv",
    "class_size.csv",
    "demographics.csv",
    "graduation.csv",
    "hs_directory.csv",
    "sat_results.csv"
]
data = {}
for ds in data_files:
    readf = pd.read_csv("schools/{0}".format(ds))
    key_name = ds.replace(".csv", "")
    data[key_name] = readf

## 5. Exploring the SAT Data ##

##Display the first five rows of the SAT scores data.
print(data['sat_results'].head())

## 6. Exploring the Remaining Data ##

for each_key in data:
    print(data[each_key].head())

## 8. Reading in the Survey Data ##

## Read in survey_all.txt and survey_d75.txt datasets
all_survey = pd.read_csv('schools/survey_all.txt', encoding="windows-1252", delimiter="\t")
d75_survey = pd.read_csv('schools/survey_d75.txt', encoding="windows-1252", delimiter="\t")

##Combine the dataframes
survey = pd.concat([all_survey, d75_survey], axis=0)

## read the dataframes
survey.head()

## 9. Cleaning Up the Surveys ##

## copy the data from the dbn column into a new column called DBN. We can copy columns like this:
# survey["new_column"] = survey["old_column"]
survey["DBN"] = survey["dbn"]

## Filter the survey data to contain needed columns
survey = survey.loc[:,["DBN", "rr_s", "rr_t", "rr_p", "N_s", "N_t", "N_p", "saf_p_11", "com_p_11", "eng_p_11", "aca_p_11", "saf_t_11", "com_t_11", "eng_t_11", "aca_t_11", "saf_s_11", "com_s_11", "eng_s_11", "aca_s_11", "saf_tot_11", "com_tot_11", "eng_tot_11", "aca_tot_11"]]

## Add survey data to the dictionary data
data["survey"] = survey

## verify survey data
print(survey.head())

## 11. Inserting DBN Fields ##

data["hs_directory"]["DBN"] = data["hs_directory"]["dbn"]

def pad_csd(num):
    return str(num).zfill(2)
    
data["class_size"]["padded_csd"] = data["class_size"]["CSD"].apply(pad_csd)
data["class_size"]["DBN"] = data["class_size"]["padded_csd"] + data["class_size"]["SCHOOL CODE"]
print(data["class_size"].head())

## 12. Combining the SAT Scores ##

##Uning manual mode calculation
data["sat_results"]["SAT Math Avg. Score"] = pd.to_numeric(data["sat_results"]["SAT Math Avg. Score"], errors="coerce")
data["sat_results"]["SAT Critical Reading Avg. Score"] = pd.to_numeric(data["sat_results"]["SAT Critical Reading Avg. Score"], errors="coerce")
data["sat_results"]["SAT Writing Avg. Score"] = pd.to_numeric(data["sat_results"]["SAT Writing Avg. Score"], errors="coerce")

data["sat_results"]["sat_score"] = data["sat_results"]["SAT Math Avg. Score"] + data["sat_results"]["SAT Critical Reading Avg. Score"] + data["sat_results"]["SAT Writing Avg. Score"]

data["sat_results"]["sat_score"].head()

## Using loop
cols = ["SAT Math Avg. Score", "SAT Critical Reading Avg. Score", "SAT Writing Avg. Score"]
for c in cols:
    pd.to_numeric(data["sat_results"][c], errors="coerce")
    
data["sat_results"]["sat_score"] = data['sat_results'][cols[0]] + data['sat_results'][cols[1]] + data['sat_results'][cols[2]]

data["sat_results"]["sat_score"].head()

## 13. Parsing Geographic Coordinates for Schools ##

import re

def find_lat(loc):
    pattern_coordinates = re.findall("\(.+\)", loc)
    return pattern_coordinates[0].split(",")[0].replace("(", "")


data["hs_directory"]["lat"] = data["hs_directory"]["Location 1"].apply(find_lat)
data["hs_directory"]["lat"].head()

## 14. Extracting the Longitude ##

import re

def find_long(loc):
    pattern_coordinates = re.findall("\(.+\)", loc)
    return pattern_coordinates[0].split(",")[1].replace(")", "").strip()

data["hs_directory"]["lon"] = data["hs_directory"]["Location 1"].apply(find_long)

data["hs_directory"]["lat"] = pd.to_numeric(data["hs_directory"]["lat"], errors="coerce")
data["hs_directory"]["lon"] = pd.to_numeric(data["hs_directory"]["lon"], errors="coerce")

print(data["hs_directory"].head())