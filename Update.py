import pandas as pd
import matplotlib.pyplot as plt
import datetime as dt
import glob 
import numpy as np
import time
from pandas import ExcelWriter
import openpyxl

pd.set_option('display.max_columns',None)
filename = []
path = 'C:/Users/m84123311/Downloads/*.xlsx'
for i in glob.iglob(path, recursive = True):
 	filename.append(i)
df = pd.read_excel(filename[0])
df.iloc[0:,-2] = df.iloc[0:,-2].apply(lambda x: x.strftime('%Y-%m-%d'))
today = (dt.datetime.today()-dt.timedelta(1)).strftime('%Y-%m-%d')
df = df[df.iloc[0:,-2] ==today]
df.iloc[0:,-2] = df.iloc[0:,-2].apply(lambda x: dt.datetime.strptime(x,'%Y-%m-%d'))
# df.iloc[0:,-2] = df.iloc[0:,-2].apply(lambda x: format(x, '%Y-%m-%d %H:%M:%S'))

###### Finish the Preparation Phase #####

BaseLocation = 'D:/Data/Py_Files/Base.xlsx'

df2 = pd.read_excel(BaseLocation)

if df2.iloc[-1,-2].__str__() == df.iloc[1,-2].__str__():
	print("True")
	pass
else:
	print("False")
	df = pd.concat([df2,df])
	with ExcelWriter(BaseLocation) as writer:
		df.to_excel(writer,sheet_name = 'Report',index = False)
		writer.save()