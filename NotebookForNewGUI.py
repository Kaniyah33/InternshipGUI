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
from ADSsearcherpkg import *

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

endLab = tk.Label(my_gui, text="end year:", width=7, font=18)  #end year label
endLab.grid(row=4, column=1)

endEnt = tk.Entry(my_gui, width=20, bg="light gray", font=18)  # added one Entry box
endEnt.grid(row=4, column=2)

#stopDirLab = tk.Label(my_gui, text="stop directory:", width=15, font=18)  #stop directory label
#stopDirLab.grid(row=4, column=1)

#stopDirEnt = tk.Entry(my_gui, width=35, bg="light gray", font=18)  # stop directory Entry box
#stopDirEnt.grid(row=4, column=2)

#stop_dir = None

#(name=None, institution=None, year= None, refereed= 'property:notrefereed OR property:refereed', \
               #token=None, stop_dir=None):

def my_search():
    if len(authEnt.get()) == 0: #check for author name
        author = None
    else:
        author = authEnt.get()
    if len(instEnt.get()) == 0: #check for institution name
        institute = None
    else:
        institute = instEnt.get()
        
    datf=AP.ads_search(name= author, institution= institute ,
               token=token, stop_dir=stop_dir) #creates dataframe
    print(datf)
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
    
my_gui.mainloop()


# In[ ]:


#datf=AP.ads_search(institution= "Howard University" ,
               #token=token, stop_dir=stop_dir)

