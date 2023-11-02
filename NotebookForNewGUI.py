#!/usr/bin/env python
# coding: utf-8

# In[34]:


import requests
from urllib.parse import urlencode, quote_plus
import numpy as np
import sys

import nltk
nltk.download('punkt')
nltk.download('wordnet')


# In[35]:


#We designed the code to work with Pandas 1.5.3
import pandas as pd
print(pd. __version__)

#If the Pandas version differs from 1.5.3, run the following:
#pip install pandas==1.5.3 --user


# In[36]:


#edit the following string pointing to the directory where the stopwords.txt file is
path_stop= '/Users/kaniyah/Downloads/NewGUI/'
stop_file='stopwords.txt'
stop_dir=path_stop+stop_file
sys.path.append(path_stop)


# In[37]:


#For the TextAnalysis File, please refer to M. Volze et al. 2023
import TextAnalysis as TA
import ADSsearcherpkg as AP


# In[38]:


#token = 'Your own token from ADS API page ' #Insert your API token
token = 'SmKbSYgQSklEPJpRpsbE03Uhcj3txilVpHoPr0AD' #Kaniyah's API token


# In[ ]:


import tkinter as tk
from tkinter import ttk  # for treeview
from tkinter import filedialog as fd # for opening files
from tkinter.messagebox import showinfo # for showing filepath
from tkinter import messagebox
from ADSsearcherpkg import *
import csv

my_gui = tk.Tk()
my_gui.geometry("1600x350")  # width x height
my_gui.title("ADSsearch.com")  # Adding a title

searchButton = tk.Button(my_gui, text="Search", width=7, font=18, command=lambda: my_search()) # search button
searchButton.grid(row=1, column=3)

authLab = tk.Label(my_gui, text="Author name:", width=15, font=18)  #author name label
authLab.grid(row=1, column=1)

authEnt = tk.Entry(my_gui, width=20, bg="light gray", font=18)  #author name entry box
authEnt.grid(row=1, column=2)

instLab = tk.Label(my_gui, text="Institution name:", width=15, font=18)  #institution name label
instLab.grid(row=2, column=1)

instEnt = tk.Entry(my_gui, width=20, bg="light gray", font=18)  #institution name entry box
instEnt.grid(row=2, column=2)

startLab = tk.Label(my_gui, text="start year:", width=7, font=18)  #start year label
startLab.grid(row=3, column=1)

startEnt = tk.Entry(my_gui, width=20, bg="light gray", font=18)  # added one Entry box
startEnt.grid(row=3, column=2)

#(name=None, institution=None, year= None, refereed= 'property:notrefereed OR property:refereed', \
               #token=None, stop_dir=None):

def my_search():
    value = 0
    if len(authEnt.get()) == 0: #check for author name
        author = None
    else:
        value += 1
        author = authEnt.get()
    if len(instEnt.get()) == 0: #check for institution name
        institute = None
    else:
        value += 2
        institute = instEnt.get()
    if len(startEnt.get()) == 0: # or (len(endEnt.get()) != 4): #check for start and end year
        yr = None
    elif startEnt.get().isdigit() == False:
        yr = None
    else: 
        value += 4
        if len(startEnt.get()) == 4:
            yr = startEnt.get()
        else:
            yr = "[2000 to 2023]"
        
        # if the len == 4: 
            #yr = startEnt.get()
            
        #if the len is 4
        #if int
        #if empty
        #if longer than 4
        
        #print(type(startEnt.get())) #type string, get it to type int
        
    # if value == 1:
    # mirror mallory's code, for 2,3, 5, 6,7 and well
    #access just the function and the value
    
    print("value: ", value)
    if value == 1:
        datf = AP.ads_search(name = author, token = token, stop_dir = stop_dir)
    elif value == 2:
        datf = AP.ads_search(institution= institute, token = token, stop_dir = stop_dir)
    elif value == 3:
        datf=AP.ads_search(name= author, institution= institute ,
               token=token, stop_dir=stop_dir) #creates dataframe
    elif value == 4:
        #datf = datf = AP.ads_search(year = yr, token = token, stop_dir = stop_dir)
        showinfo(
        title='Error',
        message='You did not give me enough to search on, please try again.'
    )
    elif value == 5:
        datf=AP.ads_search(name= author, year = yr ,
               token=token, stop_dir=stop_dir)
    elif value == 6:
        datf=AP.ads_search(institution= institute, year = yr ,
               token=token, stop_dir=stop_dir)
    elif value == 7:
        datf=AP.ads_search(name= author, institution= institute, year = yr ,
               token=token, stop_dir=stop_dir)
    else:
        return 0
    global df2
    datf['Bibcode'] = datf['Bibcode'].str.wrap(30)
    datf["Title"] = datf["Title"].str.wrap(70)
    datf['Affiliations'] = datf['Affiliations'].str.wrap(30)
    df2 = datf
    #print(type(datf), datf.head())
    l1 = list(datf) # List of column names as headers
    r_set = datf.to_numpy().tolist()  # Create list of list using rows
    trv = ttk.Treeview(my_gui, selectmode="browse")  # selectmode="browse" or "extended"
    trv.grid(row=5, column=1, columnspan=4, padx=10, pady=20)  #
    trv["height"] = 15  # Number of rows to display, default is 10
    trv["show"] = "headings"
    # column identifiers
    trv["columns"] = l1
    
    for i in l1:
        trv.column(i, width=110, anchor="c")
        # Headings of respective columns
        trv.heading(i, text=i)
    for dt in r_set:
        v = [r for r in dt]  # creating a list from each row
        #print(v[0])
        try:
            trv.insert("", "end", iid=v[0], values=v)  # adding row
        except:
            continue
        #if id value already in chart, find a way to bypass it
    
    saveButton = tk.Button(my_gui, text="Save CSV", bg="blue", width=10, font=18, command=lambda:save_to_csv())
    saveButton.grid(row=2, column=3)

def save_to_csv():
    global df2
    if df2 is not None:
        file_path = fd.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

        if file_path:
            df2.to_csv(file_path, index=False)
            print(f"Data saved to {file_path}")
    else:
        print("DataFrame is not available, you must create it first.")
      
my_gui.mainloop()


# In[ ]:


#datf=AP.ads_search(institution= "Howard University" ,
               #token=token, stop_dir=stop_dir)

