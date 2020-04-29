# import dash
# from dash.dependencies import Input, Output
# import dash_table
# import dash_core_components as dcc
# import dash_html_components as html
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import glob 
import numpy as np
### Save PNG ###
import base64
from io import BytesIO
pd.set_option('display.max_columns',None)
path  = "C:/Users/m84123311/Downloads/*.xlsx"
# save_path = "D:/Data/Py_Files"
filenames = []
for i in glob.iglob(path, recursive=True):
    filenames.append(i)
df = pd.read_excel(filenames[0])

# df.iloc[0:,-2] = df.iloc[0:,-2].apply(lambda x: x.strftime('%d-%m-%Y'))

df[df.columns[2]].replace(to_replace = 'NAZO GENERAL TRADING LLC',value= 'Global',inplace=True)
df[df.columns[2]].replace(to_replace = 'GLOBAL CO.FOR TECHNOLOGY,MOBILE DEVICES&ELECTRONIC APPLIANCES LTD',value= 'Global',inplace=True)
df[df.columns[2]].replace(to_replace = 'Euro Telecom FZE',value= 'Euro',inplace=True)
collist = list(df.columns)
subtotalacc = pd.DataFrame()
subtotalacc = df.pivot_table(index = 
	[df.columns[0],df.columns[1],df.columns[2],df.columns[3],df.columns[-2]],
	values=df.columns[-1],aggfunc=sum).reset_index()
subtotalacc['Product'],subtotalacc['Product Model'],subtotalacc['Product Family'] ='All','All','All'
subtotalacc = subtotalacc[collist]
df = pd.concat([subtotalacc,df])


subtotalcity = pd.DataFrame()
subtotalcity = df.pivot_table(index = 
	[df.columns[0],df.columns[1],df.columns[2],df.columns[3],df.columns[-2]],
	values=df.columns[-1],aggfunc=sum).reset_index()