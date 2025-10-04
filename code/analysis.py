import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# load data
df = pd.read_excel("data.xlsx")

# Function to calculate midpoint of cycle length
def midpoint(x):
    if pd.isnull(x):  # handle missing
        return np.nan
    x = str(x).replace("days", "").strip()  # remove stray 'days' if any
    if "-" in x:
        low, high = x.split("-")
        return (int(low.strip()) + int(high.strip())) / 2
    else:
        return int(x)  # single number

# Apply midpoint function
df["Cycle_len"] = df["Average Cycle length"].apply(midpoint)

# Function to classify cycle type
def classify_cycle(length):
    if pd.isnull(length):
        return np.nan
    if 25 <= length <= 35:
        return "Regular"
    else:
        return "Irregular"

# Apply classification
df["cycle_type"] = df["Cycle_len"].apply(classify_cycle)

# Check results
#print(df[["Average Cycle length", "Cycle_len", "cycle_type"]].head())

#summary stats
mean_len = df["Cycle_len"].mean()
median_len = df["Cycle_len"].median()
mode_len = df["Cycle_len"].mode()

print("Average Cycle length", mean_len)
print("Spread of data", median_len)
print("Frequent occuring data", mode_len)

#visualising with boxplot 
# Data to plot
regular = df[df["cycle_type"] == "Regular"]["Cycle_len"]
irregular = df[df["cycle_type"] == "Irregular"]["Cycle_len"]

# Plot
plt.boxplot([regular, irregular], labels=["Regular", "Irregular"])
plt.title("Cycle Length by Regular vs Irregular Cycles")
plt.ylabel("Cycle Length (days)")
plt.show()

#period duration

period_mean = df["Average period duration"].mean()
print("Average Period duration", period_mean)
period_median = df["Average period duration"].median()
print("Spread of period duration", period_median)
period_mode = df["Average Cycle length"].mode()
print("Most common duration", period_mode)

#visualizing with histogram 
regular = df[df["Cycle_len"] == "Regular"]["Average period duration"]
irregular = df[df["Cycle_len"] == "Irregular"]["Average period duration"]

# Count frequencies of each period duration
duration_counts = df["Average period duration"].value_counts().sort_index()

# Bar plot
plt.bar(duration_counts.index, duration_counts.values, color="skyblue", edgecolor="black")
plt.xlabel("Period Duration (days)")
plt.ylabel("Number of Participants")
plt.title("Distribution of Period Duration")
plt.show()

#counter plot
sns.countplot(data=df, x="Average period duration", hue="cycle_type", palette="Set2")
plt.xlabel("Period Duration (days)")
plt.ylabel("Number of Participants")
plt.title("Period Duration by Cycle Type")
plt.show()


#Symptoms and lifestyles

#importing libraries to rectify the symptoms in a cleaner manner
from collections import Counter

symptom_lists = df["symptoms"].dropna().apply(lambda x: [s.strip() for s in x.split(";")])
all_symptoms = [symptom for sublist in symptom_lists for symptom in sublist]
symptom_counts = Counter(all_symptoms)
print(symptom_counts)

#visualizing the symptoms frequency
symptoms = pd.Series(symptom_counts).sort_values(ascending=False)
plt.figure(figsize=(10,10))
sns.barplot(x=symptoms.values,y=symptoms.index,palette="flare")
plt.title("Common Symptoms Experienced")
plt.xlabel("Number of participants")
plt.ylabel("Symptoms")
#plt.show()

#visualising Co-occurance 
from sklearn.preprocessing import MultiLabelBinarizer

mlb = MultiLabelBinarizer()
symptom_matrix = pd.DataFrame(mlb.fit_transform(symptom_lists),columns=mlb.classes_,index=df.index)

#correlation matrix
symptom_corr = symptom_matrix.corr()

plt.figure(figsize=(8,6))
sns.heatmap(symptom_corr, annot=False, cmap="coolwarm", vmin=0, vmax=1)
plt.title("Symptom Co-occurrence Heatmap")
plt.show()`
#productivity and mental health

df["Productivity"] = df["Productivity"].fillna("No")
print("filled NaN with No")

#visualising productivity 
sns.countplot(data=df, x="Productivity", order=["Yes","No","Maybe","Average"],palette="pastel")
plt.title("Productivity During Menstruation")
plt.ylabel("No. of participants")
#plt.show()

#productivity and mental health - crosss analysis
plt.figure(figsize=(5,5))
sns.countplot(data=df, x="Productivity", hue="Emotional Symptoms", order=["Yes","No","Maybe","Average"], palette="muted")
plt.title("Productivity and Mental Health")
plt.ylabel("No. of Participants")
plt.show()
