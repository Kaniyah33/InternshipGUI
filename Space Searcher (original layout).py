#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
from urllib.parse import urlencode, quote_plus
import numpy as np
import sys

import nltk
nltk.download('punkt')
nltk.download('wordnet')


# In[ ]:


#We designed the code to work with Pandas 1.5.3
import pandas as pd
print(pd. __version__)

#If the Pandas version differs from 1.5.3, run the following:
#pip install pandas==1.5.3 --user


# In[ ]:


#edit the following string pointing to the directory where the stopwords.txt file is
path_stop= '/Users/kaniyah/Downloads/NewGUI/'
stop_file='stopwords.txt'
stop_dir=path_stop+stop_file
sys.path.append(path_stop)


# In[ ]:


#For the TextAnalysis File, please refer to M. Volze et al. 2023
import TextAnalysis as TA
import ADSsearcherpkg as AP


# In[ ]:


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
my_gui.resizable(width = 1600, height = 350)#geometry("1600x350")  # width x height
my_gui.title("Space Searcher")  # Adding a title
style = ttk.Style() #creates a style object

searchButton = tk.Button(my_gui, text="Search", width=7, font=18, command=lambda: my_search()) # search button
searchButton.grid(row=1, column=3)

authLab = tk.Label(my_gui, text="Author name:", width=15, font=18)  #author name label
authLab.grid(row=1, column=1)

authEnt = tk.Entry(my_gui, width=20, bg="light gray", font=18)  #author name entry box
authEnt.insert(0, "ex. Last, First")
authEnt.grid(row=1, column=2)
authEnt.bind("<FocusIn>", lambda event: authEnt.delete(0,"end") if authEnt.get() == "ex. Last, First" else None)
authEnt.bind("<FocusOut>", lambda event: authEnt.insert(0, "ex. Last, First") if authEnt.get() == "" else None)


instLab = tk.Label(my_gui, text="Institution name:", width=15, font=18)  #institution name label
instLab.grid(row=2, column=1)

instEnt = tk.Entry(my_gui, width=20, bg="light gray", font=18)  #institution name entry box
instEnt.insert(0, "ex. Example University")
instEnt.grid(row=2, column=2)
instEnt.bind("<FocusIn>", lambda event: instEnt.delete(0,"end") if instEnt.get() == "ex. Example University" else None)
instEnt.bind("<FocusOut>", lambda event: instEnt.insert(0, "ex. Example University") if instEnt.get() == "" else None)

startLab = tk.Label(my_gui, text="start year:", width=7, font=18)  #start year label
startLab.grid(row=3, column=1)

startEnt = tk.Entry(my_gui, width=20, bg="light gray", font=18)  # added one Entry box
startEnt.insert(0, "ex. XXXX")
startEnt.grid(row=3, column=2)
startEnt.bind("<FocusIn>", lambda event: startEnt.delete(0,"end") if startEnt.get() == "ex. XXXX" else None)
startEnt.bind("<FocusOut>", lambda event: startEnt.insert(0, "ex. XXXX") if startEnt.get() == "" else None)

endLab = tk.Label(my_gui, text="end year:", width=7, font=18)  #start year label
endLab.grid(row=4, column=1)

endEnt = tk.Entry(my_gui, width=20, bg="light gray", font=18)  # added one Entry box
endEnt.insert(0, "ex. XXXX")
endEnt.grid(row=4, column=2)
endEnt.bind("<FocusIn>", lambda event: endEnt.delete(0,"end") if endEnt.get() == "ex. XXXX" else None)
endEnt.bind("<FocusOut>", lambda event: endEnt.insert(0, "ex. XXXX") if endEnt.get() == "" else None)

#(name=None, institution=None, year= None, refereed= 'property:notrefereed OR property:refereed', \
               #token=None, stop_dir=None):
        
        
def my_search():
    value = 0
    if len(authEnt.get()) == 0: #check for author name
        author = None
    elif authEnt.get() == "ex. Last, First": #if name is example
        author = None
    else:
        value += 1
        author = authEnt.get()
        
        
    if len(instEnt.get()) == 0: #check for institution name
        institute = None
    elif instEnt.get() == "ex. Example University": #if institution is example
        institute = None
    else:
        value += 2
        institute = instEnt.get()
        
        
    if len(startEnt.get()) == 0:  #check for start and end year, if 0
        yr = None
        showinfo(
        title='Error',
        message='You must insert numbers.'
    )
    elif (startEnt.get() == "ex. XXXX") and (endEnt.get() == "ex. XXXX"): #if the years are the examples, if empty:
            #value += 4
            yr = "[2000 to 2023]"
    elif ((startEnt.get().isdigit() == False) and (startEnt.get() != "ex. XXXX")) or ((endEnt.get().isdigit() == False) and (endEnt.get() != "ex. XXXX")) : #if a year is not a digit and not the example
        yr = None
        showinfo(
        title='Error',
        message='You must insert numbers.'
    )
    elif ((len(startEnt.get()) != 4) and (startEnt.get() != "ex. XXXX")) or ((len(endEnt.get()) != 4) and (endEnt.get() != "ex. XXXX")): #if year is not 4 numbers and not the example
        yr = None
        showinfo(
        title='Error',
        message='Please check your formatting.'
    )
    else:
        value += 4
        if (len(startEnt.get()) == 4) and (len(endEnt.get()) == 4): #combines if the years are digits and a length of 4
            yr = "[" + startEnt.get() + " TO " + endEnt.get() + "]"
        elif (len(startEnt.get()) == 4) and (endEnt.get() == "ex. XXXX"): #if its just the start year
            yr = startEnt.get()
        elif (len(endEnt.get()) == 4) and (startEnt.get() == "ex. XXXX"): #if its just the end year
            yr = endEnt.get()    
        else: 
            yr = "[2000 to 2023]"
        print(yr)
        
    #if year ==:
        #start: "" end: ""       if empty: 2000 to 2023
        #start: xxxx end: xxxx   if all xxxx: 2000 to 2023
        #start: xxxx end: 2023   if start year is xxxx: yr = endEnt.get()
        #start: 2023 end: xxxx   if end year is xxxx: yr = startEnt.get()
        #start: 2023 end: 2023   if both correct: yr = [startEnt.get() TO endEnt.get()]
        
        #start: xxxx end: 20033  if len(startEnt.get()) != 4 or len(endEnt.get()) != 4: print error
        #start: 203 end: 20033
        #start: 2023 end: 20033
        #start: 20033 end: 20033
        #start: 20033 end: xxxx
        #start: 20033 end: 203
        #start: 20033 end: 2023
        
        #start: "2023" end: xxxx if (startEnt.get().isdigit == False) or (endEnt.get().isdigit == False): print error
        #start: "2023" end: 2023
        #start: "2023" end: 203
        #start: "2023" end: 20033
        
        #start: xxxx end: "2023" 
        #start: 2023 end: "2023"
        #start: 203 end: "2023"
        #start: 20033 end: "2023"
        #start: "2023" end: "2023"
        
    
    print("value: ", value)
    if value == 1:
        datf = AP.ads_search(name = author, token = token, stop_dir = stop_dir)
    elif value == 2:
        datf = AP.ads_search(institution= institute, token = token, stop_dir = stop_dir)
    elif value == 3:
        datf=AP.ads_search(name= author, institution= institute ,
               token=token, stop_dir=stop_dir) #creates dataframe
    elif value == 4:
        #datf = AP.ads_search(year = yr, token = token, stop_dir = stop_dir)
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
    l1 = list(datf)
    print(l1)# List of column names as headers
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
        #print(v)
        try:
            trv.insert("", "end", iid=v[0], values=v)  # adding row
        except:
            continue
        #if id value already in chart, find a way to bypass it
    verscrlbar = ttk.Scrollbar(my_gui, 
                           orient ="vertical", 
                           command = trv.yview)
    verscrlbar.grid(row= 5, column=0, sticky='NS')#(side ='right', fill ='x')
    # Configure the style for the scrollbar
    style.configure("Treeview.Scrollbar",
                background="blue",
                troughcolor="black",
                gripcount=0,
                gripcolor="white",
                gripinset=2,
                gripborderwidth=0,
                thickness=10)
    trv.configure(xscrollcommand = verscrlbar.set)
    saveButton = tk.Button(my_gui, text="Save CSV", bg="blue", width=10, font=18, command= lambda:save_to_csv())
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
