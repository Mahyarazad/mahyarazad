import pandas as pd
from datetime import datetime as dt
import numpy as np

class reshape:

	south_list = ['Al Başrah',
		            'Al Muthanná',
		            'An Najaf',
		            'Al Qādisīyah',
		            'Al Anbār',
		            'Bābil',
		            'Baghdād',
		            'Diyālá',
		            'Karbalā’',
		            'Maysān',
		            'Dhī Qār',
		            'Wāsiţ']

	pd_list = ['Mate 30 Pro',
	            'nova 5T',
	            'P smart 2019',
	            'P30',
	            'P30 lite',
	            'P30 Pro',
	            'Y5 2019',
	            'Y5 lite',
	            'Y5 Prime 2018',
	            'Y6 Prime 2019',
	            'Y6s',
	            'Y7 Prime 2019',
	            'Y7p',
	            'Y9 2019',
	            'Y9 Prime 2019',
	            'Y9s'] 

	north_list = ['As Sulaymānīyah',
					'Altameem',
					'Dahūk',
					'Arbīl',
					'Nīnawá',
					'Şalāḩ ad Dīn']

	def __init__(self,df):
		self.df = df

	@property
	def south(self):

	    self.df = self.df[(self.df[self.df.columns[1]].isin(self.south_list))&(self.df[self.df.columns[-4]].isin(self.pd_list))]
	    self.df = self.df.pivot_table(index=self.df.columns[1],columns=self.df.columns[-2],values = self.df.columns[-1],aggfunc=sum).reset_index()
	    return self.df

	@property
	def north(self):

	    self.df = self.df[(self.df[self.df.columns[1]].isin(self.north_list))&(self.df[self.df.columns[-4]].isin(self.pd_list))]
	    self.df = self.df.pivot_table(index=self.df.columns[1],columns=self.df.columns[-2],values = self.df.columns[-1],aggfunc=sum).reset_index()
	    return self.df

	@property
	def dict_data_gen(self): 

		city_data = reshape(self.df).south
		city_data2 = reshape(self.df).north
		city_data = pd.concat([city_data,city_data2])
		city_data.set_index(['Sell Out Province'],inplace = True)
		col_list = []
		deleteList = []
		for col in range(0,int(city_data.shape[1])):
		    col_list.append(str(city_data.columns[col])[0:10])
		    deleteList.append(col)
		city_data.columns = col_list
		date_list = city_data.columns.values.tolist()
		md = city_data.reset_index()
		mdr = []
		mdc = []
		for rows in range(0,md.shape[0]):
		    mdr = []
		    for col in range(1,md.shape[1]):
		        mdr.append(md.iloc[rows,col])
		    mdc.append(list(mdr))
		city_data['SO'] = mdc
		city_data['Date'] = [date_list] * len(city_data)
		city_data = city_data.drop(city_data.columns[deleteList], axis=1)
		city_data.unstack()
		city_data = city_data.transpose()
		city_data = city_data.to_dict()
		return city_data

	@property
	def summation(self):
		self.df[self.df.columns[2]].replace(to_replace = 'NAZO GENERAL TRADING LLC',value= 'Global',inplace=True)
		self.df[self.df.columns[2]].replace(to_replace = 'GLOBAL CO.FOR TECHNOLOGY,MOBILE DEVICES&ELECTRONIC APPLIANCES LTD',value= 'Global',inplace=True)
		self.df[self.df.columns[2]].replace(to_replace = 'Euro Telecom FZE',value= 'Euro',inplace=True)
		collist = list(self.df.columns)
		subtotalacc = pd.DataFrame()
		subtotalacc = self.df.pivot_table(index = 
			[self.df.columns[0],self.df.columns[1],self.df.columns[2],self.df.columns[3],self.df.columns[-2]],
			values=self.df.columns[-1],aggfunc=sum).reset_index()
		subtotalacc['Product'],subtotalacc['Product Model'],subtotalacc['Product Family'] ='All','All','All'
		subtotalacc = subtotalacc[collist]
		df = pd.concat([subtotalacc,self.df])
		df = df[df[df.columns[0]]=='Iraq']
		df = df.sort_values(by = 'Sell Out Date')
		df = df.pivot_table(index = [df.columns[1],df.columns[2],df.columns[3],df.columns[5]], columns = df.columns[-2], values = df.columns[-1], aggfunc = sum).reset_index()
		return df

	@property
	def geo(self):

		self.df[self.df.columns[-2]] = self.df[self.df.columns[-2]].dt.strftime('%Y-%m')
		cv = pd.read_excel('https://github.com/Mahyarazad/mahyarazad/raw/master/Iraq_demographic.xlsx')
		self.df = pd.pivot_table(self.df,index = self.df.columns[1],columns=self.df.columns[-2] ,values = self.df.columns[-1],aggfunc = np.sum).reset_index()
		ts = pd.concat([self.df[self.df.iloc[:,0]!='Iraq'],self.df[self.df.iloc[:,0]!='SOURCE IS NULL']],ignore_index = True)
		SIN = pd.concat([self.df[self.df.iloc[:,0]=='Iraq'],self.df[self.df.iloc[:,0]=='SOURCE IS NULL']],ignore_index = True)
		SIN = SIN.sum(axis = 1)
		SIN = pd.DataFrame({self.df.columns[0]:'Activated inside Iraq',self.df.columns[1]:SIN[0],self.df.columns[2]:SIN[1]},index = ['0'])
		df = pd.concat([self.df,SIN])
		cv = pd.merge(cv,df[[df.columns[0],df.columns[1],df.columns[2]]],on = df.columns[0],how = 'left')
		cv = cv.rename(columns = {cv.columns[-1]:'Activation for ' + str(cv.columns[-1]),
								  cv.columns[-2]:'Activation for ' + str(cv.columns[-2])})
		return cv
		
		