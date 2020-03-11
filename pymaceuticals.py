#!/usr/bin/env python
# coding: utf-8

# ## Observations and Insights
# Capomulin over-performed the competitors when treating mice with squamous cell carcinoma (SCC). It has shown to be very effective in decreasing tumor volume over a period of 45 days. Ramicane is the only medication that comes close to replicating the effectiveness of Capomulin. 
# ## Dependencies and starter code

# In[1]:


# Dependencies and Setup
import matplotlib.pyplot as plt
import pandas as pd
import scipy.stats as st
import numpy as np
import seaborn as sb

# Study data files
mouse_metadata = "data/Mouse_metadata.csv"
study_results = "data/Study_results.csv"

# Read the mouse data and the study results
mouse_metadata = pd.read_csv(mouse_metadata)
study_results = pd.read_csv(study_results)

# Combine the data into a single dataset
merged_df=pd.merge(study_results, mouse_metadata, on="Mouse ID", how="left")

merged_df.head()


# ## Summary statistics

# In[2]:


# Generate a summary statistics table of mean, median, variance, standard deviation, and SEM of the tumor 
#volume for each regimen
mean_tumor=merged_df.groupby(["Drug Regimen"]).mean()["Tumor Volume (mm3)"]
median_tumor=merged_df.groupby(["Drug Regimen"]).median()["Tumor Volume (mm3)"]
variance_tumor=merged_df.groupby(["Drug Regimen"]).var()["Tumor Volume (mm3)"]
std_tumor=merged_df.groupby(["Drug Regimen"]).std()["Tumor Volume (mm3)"]
sem_tumor=merged_df.groupby(["Drug Regimen"]).sem()["Tumor Volume (mm3)"]
summary_table=pd.DataFrame({"Mean": mean_tumor,
                           "Median": median_tumor,
                           "Variance": variance_tumor,
                           "Standard Deviation": std_tumor,
                           "SEM": sem_tumor})
summary_table


# ## Bar plots

# In[3]:


# Generate a bar plot showing number of data points for each treatment regimen using pandas
# drug_groups=merged_df.groupby("Drug Regimen")

drug_groups=merged_df["Drug Regimen"].value_counts()

drug_groups


drug_chart = drug_groups.plot(kind="bar", title="Data Points Per Drug Regimen", rot=45)
drug_chart.set_xlabel("Drug Regimen")
drug_chart.set_ylabel("Data Points")


plt.show()


# In[4]:


# Generate a bar plot showing number of data points for each treatment regimen using pyplot
x_values= drug_groups.index.values

y_values=drug_groups.values

plt.bar(x_values, y_values, align="center")

plt.xticks(rotation=45)

plt.title("Data Points Per Drug Regimen")
plt.xlabel("Drug Regimen")
plt.ylabel("Data Points")

plt.show()


# ## Pie plots

# In[5]:


# Generate a pie plot showing the distribution of female versus male mice using pandas

# sex_distro=merged_df['Sex'].value_counts().plot(kind="pie",startangle=180)

gender_groups=mouse_metadata["Sex"].value_counts()

gender_groups.head()

colors = ['#ff9999','#66b3ff']

gender_chart= gender_groups.plot(kind="pie", title="Gender Count of Mice in study", colors=colors)
gender_chart.set_ylabel(" ")

plt.show()


# In[6]:


# Generate a pie plot showing the distribution of female versus male mice using pyplot

values=gender_groups.index.values
x_values= gender_groups.values
colors=['#ff9999','#66b3ff']
plt.pie(x_values, labels=values, colors=colors)
plt.title("Gender Count of Mice in Study")
plt.axis("equal")
plt.show()


# ## Quartiles, outliers and boxplots

# In[12]:



change_name=merged_df.rename(columns={"Drug Regimen": "drug_regimen", "Mouse ID": "mouse_id", 
                                      "Weight (g)": "weight_g", "Tumor Volume (mm3)": "tumor_volume"})

drugs= ["Capomulin", "Ramicane", "Infubinol", "Ceftamin" ]

filtered_df=change_name.drug_regimen.isin(drugs)

best_drugs= change_name[change_name.drug_regimen.isin(drugs)]


sb.boxplot(x = 'drug_regimen', y = 'tumor_volume', data = best_drugs).set(
    title="Data Distributin of Final Tumor Volume for Highest Performing Medications",
    xlabel='Medication', 
    ylabel='Final Tumor Volume'
)
plt.show()


# ## Line and scatter plots

# In[8]:


# Generate a line plot of time point versus tumor volume for a mouse treated with Capomulin

capomulin_s185= change_name[(change_name.mouse_id=="s185") & (change_name.drug_regimen=="Capomulin")]

capomulin_s185


x= capomulin_s185["Timepoint"]
y= capomulin_s185["tumor_volume"]

capomulin_df=pd.DataFrame({
    "x": x,
    "y": y
})

fig, ax = plt.subplots()

capomulin_df.plot(x="x", y="y", ax=ax, label="Tumor Volume")


title = "Tumor Volume Over Time using Capomulin - Subject s185  "
ylabel = "Tumor Volume (mm3)"
xlabel = "Time"
ax.set(title=title, xlabel=xlabel, ylabel=ylabel)

ax.legend(loc="upper right")


# In[9]:


# Generate a scatter plot of mouse weight versus average tumor volume for the Capomulin regimen

capomulin= merged_df.loc[merged_df["Drug Regimen"]=="Capomulin"]

average_capomulin= capomulin.groupby(["Mouse ID"]).mean()

plt.scatter(average_capomulin["Weight (g)"], average_capomulin["Tumor Volume (mm3)"], color="red", edgecolor="black");

plt.title("Weight of Mice vs Average Tumor Volume When Using Capomulin")

plt.xlabel("Weight (g)");
plt.ylabel("Average Tumor Volume");


# In[10]:


# Calculate the correlation coefficient and linear regression model for mouse weight and average tumor volume 
#for the Capomulin regimen

correlation = st.pearsonr(average_capomulin["Weight (g)"], average_capomulin["Tumor Volume (mm3)"])
print(f"The correlation between weight and tumor size is {round(correlation[0],2)}")


# In[11]:


#find linear regression between weight and tumor volume

m_slope, m_int, m_r, m_p, m_std_err = st.linregress(average_capomulin["Weight (g)"], average_capomulin["Tumor Volume (mm3)"])
m_fit = m_slope * average_capomulin["Weight (g)"] + m_int
line_eq = "y = " + str(round(m_slope,2)) + "x + " + str(round(m_int,2))
plt.scatter(average_capomulin["Weight (g)"],average_capomulin["Tumor Volume (mm3)"])
plt.plot(average_capomulin["Weight (g)"],m_fit, color="red")
plt.xticks(average_capomulin["Weight (g)"])
plt.annotate(line_eq, (20,36), fontsize=15,color="red")
plt.title("Weight of Mice vs Average Tumor Volume When Using Capomulin")
plt.xlabel("Weight (g)");
plt.ylabel("Average Tumor Volume");
plt.show()


# In[ ]:




