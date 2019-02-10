#!/usr/bin/python


# # MP Materials WindRose Program
# #### Exponent
# #### Designed by Ankur Singhal (asinghal@exponent.com)

# Licensing:

# *Windrose : https://github.com/python-windrose/windrose/blob/master/LICENCE
#     - CECILL-B: https://github.com/python-windrose/windrose/blob/master/LICENCE_BSD-3-Clause.TXT
#     - BSD-3-Clause: https://github.com/python-windrose/windrose/blob/master/LICENCE_BSD-3-Clause.TXT

from windrose import WindroseAxes
from matplotlib import pyplot as plt
import matplotlib.cm as cm
import pandas as pd
import os
import numpy as np
import tkinter as tk
from tkinter import ttk, messagebox, filedialog
# from tkcalendar import Calendar
from datetime import datetime, time

"""
class Cal_View():
    def __init__(self, root):
        self.top = tk.Toplevel(root)

        self.cal = Calendar(self.top, font="Arial 14", selectmode='day',
                            cursor="hand1", year=2018, month=2, day=5)
        self.cal.pack(fill="both", expand=True)
        ttk.Button(self.top, text="ok", command=self.print_sel).pack()

        self.date = ''

        self.top.grab_set()

    def print_sel(self):
        self.date = self.cal.selection_get()
        self.top.destroy()
"""

class DateTime():
    def __init__(self, df_time):
        self.root = tk.Tk()
        self.frame = tk.Frame(self.root, bd=2, relief='ridge')
        self.frame.grid(row=0, column=0,)
        self.df_time = df_time

        s = ttk.Style(self.root)
        s.theme_use('winnative')
        
        self.root.title('Select start and end dates and times')
         
        ttk.Label(self.frame, text='Enter the starting and ending dates and times between\n\"{0}\" and \"{1}\"\n'.format(self.df_time.min(), self.df_time.max())).grid(row=0, columnspan=3, stick='w')
        ttk.Label(self.frame, text='Note: All fiels are required!\n', foreground='red').grid(row=1, columnspan=3, sticky='w')
        ttk.Label(self.frame, text='Start date (mm-dd-YYYY)').grid(row=2, column=0)
        ttk.Label(self.frame, text='HH').grid(row=2, column=1)
        ttk.Label(self.frame, text='MM').grid(row=2, column=2)
        #ttk.Button(self.root, text='Start Date', command=self.start_date).grid(row=4, column=0, padx=15)
        self.start_date = ttk.Entry(self.frame)
        self.start_hour = ttk.Entry(self.frame)
        self.start_min = ttk.Entry(self.frame)
        
        self.start_date.grid(row=3, column=0, padx=5)
        self.start_hour.grid(row=3, column=1, padx=5)
        self.start_min.grid(row=3, column=2, padx=5)
        
        ttk.Label(self.frame, text='End date (mm-dd-YYYY)').grid(row=4, column=0)
        ttk.Label(self.frame, text='HH').grid(row=4, column=1)
        ttk.Label(self.frame, text='MM').grid(row=4, column=2)
        #ttk.Button(self.root, text='End Date', command=self.end_date).grid(row=7, column=0, padx=15)
        self.end_date = ttk.Entry(self.frame)
        self.end_hour = ttk.Entry(self.frame)
        self.end_min = ttk.Entry(self.frame)
        
        self.end_date.grid(row=5, column=0, padx=5)
        self.end_hour.grid(row=5, column=1, padx=5)
        self.end_min.grid(row=5, column=2, padx=5)
        
        ttk.Button(self.frame, text='Submit', command=self.submit).grid(row=6, column=0, columnspan=3, padx=15, pady=15)

        self.get_start_date = ''
        self.get_end_date = ''
        
        self.root.mainloop()

    """
    def start_date(self):
        cal = Cal_View(self.root)
        self.root.wait_window(cal.top)
        self.get_start_date = cal.date


    def end_date(self):
        cal = Cal_View(self.root)
        self.root.wait_window(cal.top)
        self.get_end_date = cal.date

    """
    def submit(self):
        try:
            self.get_start_date = datetime.strptime(self.start_date.get(), '%m-%d-%Y').date()
            self.get_end_date = datetime.strptime(self.end_date.get(), '%m-%d-%Y').date()
            self.get_start_time = time(int(self.start_hour.get()), int(self.start_min.get()))
            self.get_end_time = time(int(self.end_hour.get()), int(self.end_min.get()))
        except:
            messagebox.showerror('ERROR', 'Date and time entries cannot be blank.\nHours should be between 0-23 and minutes should be between 0-59')
            raise
        
        if self.get_start_date > self.get_end_date:
            messagebox.showerror('ERROR', 'End date cannot precede start date. Either end date or start date needs to be fixed')
        elif self.get_start_date < datetime.strptime(str(self.df_time.min()), '%Y-%m-%d %H:%M:%S').date() or self.get_end_date > datetime.strptime(str(self.df_time.max()), '%Y-%m-%d %H:%M:%S').date():
             messagebox.showerror('ERROR', 'Dates entered are outside the range of the data!')           
        else:
            self.root.destroy()


class WindroseParams():
    def __init__(self, ws):
        self.root = tk.Tk()
        self.ws = ws
        
        s = ttk.Style(self.root)
        s.theme_use('winnative')
        
        self.root.title('Provide wind rose parameters')

        ttk.Label(self.root, text='Please provide the highest wind speed category for\nyour plot (e.g. "20" for 20+mph)').grid(row=0, columnspan=2, padx=10)
        ttk.Label(self.root, text='Max: ' + str(pd.Series.max(ws)) + ';  Mean: ' + str(round(pd.Series.mean(ws),2)) + ';  Median: ' + str(round(pd.Series.median(ws),2))).grid(row=1, column=0, columnspan=2)
        ttk.Label(self.root, text='Highest windspeed:').grid(row=2, column=0, sticky='e')
        self.windspeed = ttk.Entry(self.root)
        self.windspeed.grid(row=2, column=1, padx=10)
        
        ttk.Label(self.root, text='\nSpecify the number of wind speed categories').grid(row=3, columnspan=2, padx=10)
        ttk.Label(self.root, text='Wind speed cotegories:').grid(row=4, column=0, sticky='e')
        self.windcat = ttk.Entry(self.root)
        self.windcat.grid(row=4, column=1, padx=10)

        ttk.Button(self.root, text='Submit', command=self.submit).grid(row=5, column=0, columnspan=2, padx=10, pady=10)

        self.root.mainloop()
    
    
    def submit(self):
        try:
            self.get_windspeed = float(self.windspeed.get())
            self.get_windcat = int(self.windcat.get())
        except:
            messagebox.showerror('ERROR', 'Entries must be numerical!')
            raise
        
        self.root.destroy()


####
def get_met_file():
    """
    Opens up a dialog box to ask the user to select the appropriate 
    Campbell Scientific meteorological data file.

    Note: User input is required
    """
    root = tk.Tk()

    # Ask the user to select the appropriate D1000 file
    messagebox.showinfo('Choose file', 'Please choose the Campbell Scientific meteorological data file')
    met_file = filedialog.askopenfile(parent=root, mode='rb', title="Choose the Campbell Scientific meteorological data file")
    
    root.destroy()

    print("\nRegistering file. May take a few seconds depending on the size of the file...\n")

    return(met_file)


###############################################################################

# Convert met file to a pandas dataframe
# skip first row, which appears to be extraneous
df_met = pd.read_csv(get_met_file(), skiprows=1)

# Remove first two data rows, which correspond to metadata 
# (store as separate dataframe in case of use later)
nrows_in_df_met = df_met.shape[0]
df_met_meta = df_met.iloc[0:2]
df_met = df_met.iloc[2:nrows_in_df_met]

# reassign object types to datetime and int or float where appropriate
ncols_in_df_met = df_met.shape[1]
df_met.columns = [str.upper(col) for col in df_met.columns]
df_datetimeonly = pd.to_datetime(df_met['TIMESTAMP'])
df_others = df_met.iloc[:,1:ncols_in_df_met].apply(pd.to_numeric)
df_wx = pd.concat([df_datetimeonly, df_others], axis = 1)
df_wx.set_index('TIMESTAMP')

app = DateTime(df_wx['TIMESTAMP'])

start_time = datetime.combine(app.get_start_date, app.get_start_time)
start = start_time.strftime('%Y-%m-%d %H:%M:00')
end_time = datetime.combine(app.get_end_date, app.get_end_time)
end = end_time.strftime('%Y-%m-%d %H:%M:00')

## Isolate and subset wind direction and wind speed data by date
wd = df_wx[(df_wx['TIMESTAMP'] >= start) & (df_wx['TIMESTAMP'] <= end)].WD_MEANUNITVECTOR
ws = df_wx[(df_wx['TIMESTAMP'] >= start) & (df_wx['TIMESTAMP'] <= end)].WS_MEAN

windrose_title = 'MPMO_windrose_' + start_time.strftime('%m%d%y') + '_to_' + end_time.strftime('%m%d%y.pdf')

params = WindroseParams(ws)
cats_to_use = np.arange(0, (params.get_windspeed+1), int(params.get_windspeed/params.get_windcat))


### Create Windrose
# percent below 1 m/s or 2.2 mph
calm_ws = round((len(ws[ws < 2.2]) / len(ws) ) * 100 ,1) 

ax = WindroseAxes.from_ax()
ax.bar(wd, ws, normed = True, opening=0.75, edgecolor = 'white', cmap = cm.jet, alpha = 1, 
       bins = cats_to_use )
ax.legend(#loc = 0, # best location based on data
         title = 'Wind Speed (mph)' + '\ncalm: ' + str(calm_ws) + ' %',
         frameon = 1,
         shadow = 1,
         framealpha = 1,
         bbox_to_anchor=(1, 0)  # helpful in making legend outside of figure
         )

ax.set_xlabel('Radial Units are Percent of Total')
ax.set_title(label = ('Wind Rose' + '\n '+ start + '  through  ' + end), fontsize=15)

root = tk.Tk()
messagebox.showinfo("Choose folder", "Please choose the folder to store the windrose in")
os.chdir(filedialog.askdirectory(parent=root, title="Choose the folder to store the windrose in"))
messagebox.showinfo("", "Output file {} being stored in {}".format(windrose_title, os.getcwd()))
root.destroy()

plt.savefig(windrose_title, bbox_inches='tight')
plt.show()

