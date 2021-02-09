#!/usr/bin/env python
# coding: utf-8

# In[1]:


#importing some libraries

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from datetime import datetime


# In[3]:


data = pd.read_csv("D:\Data science\SCMS_Delivery_History_Dataset.csv",encoding = "latin1")


# In[4]:


data.head()


# In[5]:


data.shape


# In[6]:


data.columns


# In[7]:


print("Total number of rows: " ,data.shape[0] )
print("Total number of columns: " ,data.shape[1] )


# In[8]:


data = data.drop(["Item Description","Molecule/Test Type"],axis=1) 


# In[10]:


data = data[data["Weight (Kilograms)"]!="Weight Captured Separately"] 


# In[11]:


data = data[data["Freight Cost (USD)"]!="Freight Included in Commodity Cost"] 


# In[12]:


data = data[data["Freight Cost (USD)"]!="Invoiced Separately"] 


# In[13]:


data.shape


# In[14]:


data.dtypes


# In[15]:


data["Weight (Kilograms)"] =pd.to_numeric(data["Weight (Kilograms)"])


# In[16]:


data["Freight Cost (USD)"] =pd.to_numeric(data["Freight Cost (USD)"])


# In[17]:


data["Scheduled Delivery Date"] = pd.to_datetime(data["Scheduled Delivery Date"])


# In[21]:


order=data["PO / SO #"].nunique() #5572 orders


# In[22]:


order=data["PO / SO #"].count() #6175 orders


# In[24]:


total_projects = data["ï»¿Project Code"].nunique() #130


# In[28]:


total_Freight_Cost= data["Freight Cost (USD)"].sum() #68687760.27


# In[29]:


avg_Freight_Cost= total_Freight_Cost/order #12327.308016870064


# In[30]:


country_summary = data.groupby("Country").sum().reset_index()


# In[31]:


data.head()


# In[32]:


country_summary.columns


# In[33]:


country_summary = country_summary[["Country","Freight Cost (USD)"]]


# In[36]:


country_summary = data.groupby(["Country","Shipment Mode"]).sum().reset_index()


# In[37]:


country_summary = country_summary[["Country","Shipment Mode","Freight Cost (USD)"]]


# In[38]:


country_summary = data.groupby(["Country","Shipment Mode"]).agg({"PO / SO #":"count","Freight Cost (USD)":"sum"}).reset_index()


# In[39]:


country_summary["frt_cst_shipment_per_country_usd_order"] = country_summary["Freight Cost (USD)"]/country_summary["PO / SO #"]


# In[40]:


country_summary.head()


# In[79]:


plt.figure(figsize = (30,7))


# In[82]:


sns.set(font_scale=0.8, palette = "dark")


# In[83]:


ax = sns.barplot(data=country_summary, x = "Country", y="frt_cst_shipment_per_country_usd_order" , ci = None, estimator = sum )
plt.title("Frieght cost by shipment by country order", fontsize = 20)
for p in ax.patches:
    height = p.get_height()
    ax.text(x=p.get_x()+(p.get_width()/2),
    y=height+10, ha="center", s="{:.0f}".format(height))
    plt.xticks(rotation ="vertical")
    plt.show()


# In[86]:


plt.figure(figsize = (30,7))
sns.set(font_scale=2, palette = "dark")
ax = sns.barplot(data=country_summary, x = "Shipment Mode", y="frt_cst_shipment_per_country_usd_order" , ci = None, estimator = sum )
plt.title("Frieght cost by shipment by country order", fontsize = 20)
for p in ax.patches:
    height = p.get_height()
    ax.text(x=p.get_x()+(p.get_width()/2),
    y=height+10, ha="center", s="{:.0f}".format(height))
    plt.xticks(rotation ="vertical")
    plt.show()


# In[87]:


#total freight cost for top 10 country
totalfreight= data.groupby(["Country"])["Freight Cost (USD)"].sum().nlargest(10)


# In[88]:


totalfreight.head()


# In[101]:


plt.figure(figsize = (10,3))
ax_1=data.groupby(["Country"])["Freight Cost (USD)"].sum().nlargest(10).reset_index()
ax = sns.barplot(data=ax_1, x = "Country", y="Freight Cost (USD)" , ci = None, estimator = sum )
plt.ylabel("TFC")

for p in ax.patches:
    height = p.get_height()
    ax.text(x=p.get_x()+(p.get_width()/2),
    y=height+10, ha="center", s="{:.0f}".format(height))
    plt.xticks(rotation ="vertical")
    plt.show()


# In[92]:


# mf is manufacturing
mf_summary = data.groupby("Manufacturing Site").count().reset_index()
mf_summary.head()


# In[93]:


mf_summary = data.groupby(["Manufacturing Site"]).agg({"PO / SO #":"count","Freight Cost (USD)":"sum"}).reset_index()
mf_summary.head()


# In[95]:


plt.figure(figsize = (40,10))
sns.set(font_scale=1.5, palette = "dark")

ax = sns.barplot(data=mf_summary, x = "Manufacturing Site", y="Freight Cost (USD)" , ci = None, estimator = sum )
plt.title("Frieght cost by Manufacturing Site", fontsize = 20)
for p in ax.patches:
    height = p.get_height()
    ax.text(x=p.get_x()+(p.get_width()/2),
    y=height+10, ha="center", s="{:.0f}".format(height))
    plt.xticks(rotation ="vertical")
    plt.show()


# In[98]:


#total freight cost for top 10 country
total_freight= data.groupby(["Manufacturing Site"])["Freight Cost (USD)"].sum().nlargest(10)
total_freight.head()

