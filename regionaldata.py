
# import Update
import os
from random import randint
import flask
import dash
from dash.dependencies import Input, Output
import dash_bootstrap_components as dbc
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
from datetime import date
import glob 
import numpy as np


# path  = "D:/Data/Py_Files/*.xlsx"
# save_path = "D:/Data/Py_Files"
# filenames = []
# for i in glob.iglob(path, recursive=True):
#     filenames.append(i)

url = 'https://github.com/Mahyarazad/mahyarazad/raw/master/Base.xlsx'
df = pd.read_excel(url)

# df.iloc[0:,-2] = df.iloc[0:,-2].apply(lambda x: x.strftime('%d-%m-%Y'))

df[df.columns[2]].replace(to_replace = 'NAZO GENERAL TRADING LLC',value= 'Global',inplace=True)
df[df.columns[2]].replace(to_replace = 'GLOBAL CO.FOR TECHNOLOGY,MOBILE DEVICES&ELECTRONIC APPLIANCES LTD',value= 'Global',inplace=True)
df[df.columns[2]].replace(to_replace = 'Euro Telecom FZE',value= 'Euro',inplace=True)
pd.set_option('display.max_columns',None)

#### Adding Subtotal to the Base file ####

collist = list(df.columns)
subtotalacc = pd.DataFrame()
subtotalacc = df.pivot_table(index = 
	[df.columns[0],df.columns[1],df.columns[2],df.columns[3],df.columns[-2]],
	values=df.columns[-1],aggfunc=sum).reset_index()
subtotalacc['Product'],subtotalacc['Product Model'],subtotalacc['Product Family'] ='All','All','All'
subtotalacc = subtotalacc[collist]
df = pd.concat([subtotalacc,df])

##########################################


north_list = [
                'As Sulaymānīyah',
                'Altameem',
                'Dahūk',
                'Arbīl',
                'Nīnawá',
                'Şalāḩ ad Dīn']

south_list = [
                'Al Başrah',
                'Al Muthanná'
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
north_south = {'North' : ['As Sulaymānīyah',
                'Altameem',
                'Dahūk',
                'Arbīl',
                'Nīnawá',
                'Şalāḩ ad Dīn'],
                'South' : ['Al Başrah',
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
                'Wāsiţ']}

all_options = {'HUAWEI': ['Euro','Global'],'HONOR' : ['JiBAL Company for General Trading/Ltd']}
all_options_p = {'HUAWEI': ['All',
							'Y9s',
							'Y9 Prime 2019',
							'Y9 2019',
							'Y7p',
							'Y7 Prime 2019',
							'Y6s',
							'Y6 Prime 2019',
							'Y5 Prime 2018',
							'Y5 lite',
							'Y5 2019',
							'WATCH GT 2',
							'P30 Pro',
							'P30 lite',
							'P30',
							'P smart 2019',
							'nova 5T',
							'MediaPad T5 10.1吋',
							'MediaPad T3 7',
							'MediaPad T3 10',
							'MediaPad M5 lite 10.1吋',
							'Mate 30 Pro',
							'HUAWEI WATCH GT',
							'HUAWEI FreeBuds 3',
							'FreeBuds Lite',
							],'HONOR' : [
							'All',
							'HONOR 9X',
							'Honor 8X Max',
							'Honor 8X',
							'HONOR 8S',
							'Honor 8C',
							'Honor 8A',
							'Honor 7S',
							'HONOR 20 PRO',
							'HONOR 20',
							'HONOR 10i',
							'Honor 10 Lite']}

df = df[df[df.columns[0]]=='Iraq']
df = df.sort_values(by = 'Sell Out Date')
df = df.pivot_table(index = [df.columns[1],df.columns[2],df.columns[3],df.columns[5]], columns = df.columns[-2], values = df.columns[-1], aggfunc = sum).reset_index()

##### Test Print ###### 

# print(df[(df[df.columns[0]]=='Dahūk')&(df[df.columns[3]]=='Y9s')&(df[df.columns[1]].isin(all_options['HUAWEI']))].sum().index[4:])


##### Second Tab ######



####### Main App ######
server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
app = dash.Dash(__name__,server=server ,external_stylesheets = [
        'https://codepen.io/chriddyp/pen/bWLwgP.css'
    ])

app.layout = html.Div([
	dcc.Tabs([
		dcc.Tab(label='Provincial Dashboard',style = {
			    'borderBottom': '1px solid #d6d6d6',
			    'padding': '6px',
			    'fontWeight': 'bold'
			},

			selected_style = {
			    'borderTop': '1px solid #d6d6d6',
			    'borderBottom': '1px solid #d6d6d6',
			    'backgroundColor': '#119DFF',
			    'color': 'white',
			    'padding': '6px'
			},children=[
		    html.Div([
		    	html.Br(),
		    	html.Br(),
			    html.Div(id='output-text',   style = {
			    'color' : '#070200',
			    'background-color' : '#EFEEEE',
			    'text-margin':'center',
			    'width':'auto',
			    'font-family': "Lato",
			    'margin-left':'0px',
			    'font-size': '15px'

			    },children = ''),
			    html.Br(),
			    dcc.RadioItems(
			        id = 'Brand',
			        value = 'HUAWEI',
					options=[{'label': k, 'value': k} for k in all_options.keys()],
			        labelStyle={'display': 'inline-block'}
			        ),
			    html.Br(),
			    dcc.Checklist(
			        id = 'Account',
			        value = ['Euro','Global'],
			        options= [{'label': 'Euro', 'value' : 'Euro'},{'label': 'Global', 'value' : 'Global'}],
			        labelStyle={'display': 'inline-block'}
			        ),
			    html.Br(),
			    dcc.RadioItems(
			        id = 'NS',
			        value = 'South',
					options=[{'label': k, 'value': k} for k in north_south.keys()],
			        labelStyle={'display': 'inline-block'}
			        ),
			    html.Br(),
			    dcc.Dropdown(
			    id = 'Province',
			    multi = True,
			    style={'height': '400px !important', 'width': '200px','font-size': "100%",'border-radius': '6px'},
			    value = None,
			    options=[
			        {'label': i, 'value':i} for i in df[df.columns[0]].unique()]
			    ),
			    html.Br(),
			    dcc.Dropdown(
			    id = 'Product',
			    style={'height': '30px', 'width': '200px'},
			    value = None,
			    multi = True,
			    options=[
			        {'label': i, 'value':i} for i in df[df.columns[3]].unique()
			        ] 
			    ),
			    html.Br()
			    ],className = "three columns"
			),
		    
		    html.Div([
		        dcc.Graph(
		            id='sell_out',
		            )        
		    ],className = 'nine columns'),
		],className = 'ten columns offset-by-one'
		),
		dcc.Tab(label = 'Business Analysis',style = {
			    'borderBottom': '1px solid #d6d6d6',
			    'padding': '6px',
			    'fontWeight': 'bold'
			},

			selected_style = {
			    'borderTop': '1px solid #d6d6d6',
			    'borderBottom': '1px solid #d6d6d6',
			    'backgroundColor': '#119DFF',
			    'color': 'white',
			    'padding': '6px'
			}, children = [
			html.Br(),
			html.Br(),
			html.H1(children='Iraq Handest Daily Sales',
	                        className='nine columns'),
	        html.Img(
	            src="data:image/jpeg;base64,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",
	            className='three columns',
	            style={
	                'height': '9%',
	                'width': '9%',
	                'float': 'right',
	                'position': 'relative',
	                'margin-top': 10,
	            },
	        )
		])
	],className = 'ten columns offset-by-one')
],className = 'ten columns offset-by-one')	


@app.callback(
    Output('Product', 'options'),
    [Input('Brand', 'value')])

def set_product_options(selected_brand_for_product):

	return [{'label': i, 'value': i} for i in all_options_p[selected_brand_for_product]]

@app.callback(
    Output('Account', 'options'),
    [Input('Brand', 'value')])

def set_brands_options(selected_brand):

	return [{'label': i, 'value': i} for i in all_options[selected_brand]]

@app.callback(
    Output('Province', 'options'),
    [Input('NS', 'value')])

def set_cities_options(selected_region):

	return [{'label': i, 'value': i} for i in north_south[selected_region]]


@app.callback(
    Output('output-text','children'),
    [Input('Province','value'),
    Input('Account','value'),
    Input('Brand','value'),
    Input('Product','value')])
def update_text(province,account,brand,product):

    return '{} Province,{} account and, {} product has been selected'.format(province,account,product,df[df.columns[1]].isin(all_options[brand]).index[4:])

@app.callback(
    Output('sell_out','figure'),
    [Input('Brand','value'),
    Input('Province','value'),
    Input('Account','value'),
    Input('Product','value')])

def sell_out(brand,province,account,product):
	if brand == "HUAWEI":
		color = 'E94713' 
	else:
		color = '3CBCD6'
	data = [{'x': df[(df[df.columns[0]].isin(province))&(df[df.columns[3]].isin(product))&(df[df.columns[1]].isin(account))].sum().index[4:],
            'y': df[(df[df.columns[0]].isin(province))&(df[df.columns[3]].isin(product))&(df[df.columns[1]].isin(account))].sum().values[4:],
            'type': 'line',
            'marker': {'color': color}}]

	figure = {
        'data': data,
        'layout': {
            'title': province,
            'xaxis' : dict(
                # title='x Axis',
                titlefont=dict(
                family='Courier New, monospace',
                size=10,
                color='#7f7f7f'
            )),
            'yaxis' : dict(
                # title='y Axis',
                titlefont=dict(
                family='Helvetica, monospace',
                size=10,
                color='#7f7f7f'
            ))
        }
    }

	return figure

if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
# (debug=True, port=8054,dev_tools_ui=False, dev_tools_props_check=False)