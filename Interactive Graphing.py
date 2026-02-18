# "create a python script to read in calculatedVariables.csv and 
# rawData.csv and create interactive graph visualizations"

# for rawData : graph frequency vs real/imag or mag impedance 
# for calculatedVariables : Qf over time, PM over time, & Rf over time 

''' notes: 
    - raw data will always be 51x length of calculated variables
    - packages taken from mikes script, delete unused ones at end of development  

'''
#package managment ---------------

#Import native packages
import subprocess
import sys
import threading
import csv
import asyncio
import struct
import tkinter as tk
from tkinter import ttk, filedialog
from tkinter import messagebox
import tkinter.font as tkFont
from datetime import datetime
import os



#check if required 3rd party packages are installed...install if not
def install_packages(): 
    required = ["matplotlib", "bleak", "numpy", "scipy", "pandas"]
    for package in required:
        try:
            __import__(package)
        except ImportError:
            subprocess.check_call([sys.executable, "-m", "pip", "install", package])

install_packages()

#Import third party packages
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.widgets import Cursor
import matplotlib.ticker as ticker
from bleak import BleakScanner, BleakClient
from scipy.optimize import curve_fit
import subprocess
import sys
import pandas as pd
# from mpl_interactions import ioff, panhandler, zoom_factory - I dont think I need these but will keep for now just in case, delete at end of development if not used




# function definitions -------------

# function that allows user to select raw data files from their file explorer and returns the file path 
def select_raw_file():
    try:
        #open file explorer and allow user to select a file ending with the term 'rawData'
        file_path = filedialog.askopenfilename(
            title="Select a raw data file",
            filetypes=[("CSV Files", "*rawData.csv")]
        )
        if file_path:  # If a file was selected
            print(f"Selected file: {file_path}")
            messagebox.showinfo("File Selected", f"You selected:\n{file_path}")
            return file_path
        else:
            print("No file selected.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")


# function that allows user to select calculated variable files from their file explorer and returns the file path
def select_calc_file():
    try:
        #open file explorer and allow user to select a file ending with the term 'calculatedVariables'
        file_path = filedialog.askopenfilename(
            title="Select a raw data file",
            filetypes=[("CSV Files", "*calculatedVariables.csv")]
        )
        if file_path:  # If a file was selected
            print(f"Selected file: {file_path}")
            messagebox.showinfo("File Selected", f"You selected:\n{file_path}")
            return file_path
        else:
            print("No file selected.")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred: {e}")

#function that reads csv file path into a dataframe and returns that dataframe 
def read_csv_to_df(file_path): 
    try:
        # Read CSV into DataFrame
        df = pd.read_csv(file_path, skiprows=[0,1,2]) # skips first 3 rows that contain model number ect.
        print(f"Successfully loaded CSV: {file_path}")
        print(df.head())  # Show first 5 rows
        return df
    except pd.errors.EmptyDataError:
        messagebox.showerror("Error", "The selected CSV file is empty.")
    except pd.errors.ParserError:
        messagebox.showerror("Error", "The selected file is not a valid CSV.")
    except Exception as e:
        messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

    return None




# main -----------------
# variables 


# Create a hidden root window (so only the file dialog appears)
root = tk.Tk()
root.withdraw()

# Call the file selection function
raw_filepath = select_raw_file()
calc_filepath = select_calc_file()

#obtain dataframes for raw and calc files 

df_raw = read_csv_to_df(raw_filepath)
df_calc = read_csv_to_df(calc_filepath)


# plot line graph of calculated variables
plt.plot(df_calc['Time Stamp'], df_calc['Q-Factor'])
plt.xlabel("Index")
plt.ylabel("Quality Factor")
plt.title("Line Chart Example")
plt.grid(which='major',axis='both')
plt.ion() #allows for zooming and panning 
plt.show(block = True) # this is now not working 


#error checking - possibly implement this into read_csv_into_df
print(calc_filepath)
df = read_csv_to_df(calc_filepath)
if df is not None:
        print(f"DataFrame shape: {df.shape}")
