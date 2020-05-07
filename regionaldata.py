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

url = 'https://github.com/Mahyarazad/mahyarazad/blob/master/Base.xlsx'
df = pd.read_excel(url)


# df.iloc[0:,-2] = df.iloc[0:,-2].apply(lambda x: x.strftime('%d-%m-%Y'))

df[df.columns[2]].replace(to_replace = 'NAZO GENERAL TRADING LLC',value= 'Global',inplace=True)
df[df.columns[2]].replace(to_replace = 'GLOBAL CO.FOR TECHNOLOGY,MOBILE DEVICES&ELECTRONIC APPLIANCES LTD',value= 'Global',inplace=True)
df[df.columns[2]].replace(to_replace = 'Euro Telecom FZE',value= 'Euro',inplace=True)
pd.set_option('display.max_columns',None)

#### Adding Subtotal to the Base dataframe ####

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


##### Second Tab Processing######

df2 = pd.read_excel(url)
pd_list = {'Product':['Mate 30 Pro',
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
                'Y9s']}
all_options_t = {'South':[
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
                'Wāsiţ'],'North' : [
                'As Sulaymānīyah',
                'Altameem',
                'Dahūk',
                'Arbīl',
                'Nīnawá',
                'Şalāḩ ad Dīn']}
#,'All':[]
pd_list2 = ['Mate 30 Pro',
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
def south(df):

    df = df[(df[df.columns[1]].isin(south_list))&(df[df.columns[-4]].isin(pd_list2))]
    df = df.pivot_table(index=df.columns[1],columns=df.columns[-2],values = df.columns[-1],aggfunc=sum).reset_index()
    return df

def north(df):
    df = df[(df[df.columns[1]].isin(north_list))&(df[df.columns[-4]].isin(pd_list2))]
    df = df.pivot_table(index=df.columns[1],columns=df.columns[-2],values = df.columns[-1],aggfunc=sum).reset_index()
    return df


city_data = south(df2)
city_data2 = north(df2)
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

####### Main App ######
server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
app = dash.Dash(__name__,server=server ,external_stylesheets = [
        'https://codepen.io/chriddyp/pen/bWLwgP.css'
    ])
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True
app.title = 'Iraq Sales Status'
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
					    value = 'Baghdād',
					    options=[
					        {'label': i, 'value':i} for i in df[df.columns[0]].unique()]
					    ),
					    html.Br(),
					    dcc.Dropdown(
					    id = 'Product',
					    style={'height': '30px', 'width': '200px'},
					    value = 'All',
					    multi = True,
					    options=[
					        {'label': i, 'value':i} for i in df[df.columns[3]].unique()
					        ] 
					    ),
					    html.Br()
					    ],className = 'three columns'
					),
				    
				    html.Div([
				        dcc.Graph(
				            id='sell_out',
				            )        
				    ],className = 'nine columns'),
                    ],
                    className = "row"),
                    html.Div([
                        html.Div([
                            html.Div(id='output-text2',   style = {
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
                                id = 'Brand2',
                                value = 'HONOR',
                                options=[{'label': k, 'value': k} for k in all_options.keys()],
                                labelStyle={'display': 'inline-block'}
                                ),
                            html.Br(),
                            dcc.Checklist(
                                id = 'Account2',
                                value = ['Euro','Global'],
                                options= [{'label': 'Euro', 'value' : 'Euro'},{'label': 'Global', 'value' : 'Global'}],
                                labelStyle={'display': 'inline-block'}
                                ),
                            html.Br(),
                            dcc.RadioItems(
                                id = 'NS2',
                                value = 'South',
                                options=[{'label': k, 'value': k} for k in north_south.keys()],
                                labelStyle={'display': 'inline-block'}
                                ),
                            html.Br(),
                            dcc.Dropdown(
                            id = 'Province2',
                            multi = True,
                            style={'height': '400px !important', 'width': '200px','font-size': "100%",'border-radius': '6px'},
                            value = 'All',
                            options=[
                                {'label': i, 'value':i} for i in df[df.columns[0]].unique()]
                            ),
                            html.Br(),
                            dcc.Dropdown(
                            id = 'Product2',
                            style={'height': '30px', 'width': '200px'},
                            value = 'Baghdād',
                            multi = True,
                            options=[
                                {'label': i, 'value':i} for i in df[df.columns[3]].unique()
                                ] 
                            ),
                            html.Br()
                            ],className = 'three columns'
                        ),
                        
                        html.Div([
                            dcc.Graph(
                                id='sell_out2',
                                )        
                        ],className = 'nine columns'),
                    ],className = "row"),    
                ]),

		dcc.Tab(label = 'Huawei Sales Trend',style = {
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
        html.Div(
            [
                html.Div(
                    [
                        html.P('Choose Province:'),
                        dcc.Checklist(
                                id = 'Cities',
                                options=[
                                    {'label': 'Al Qādisīyah', 'value': 'Al Qādisīyah'},
                                    {'label': 'Bābil', 'value': 'Bābil'},
                                ],
                                value=['Bābil', 'Al Qādisīyah'],
                                labelStyle={'display': 'inline-block'}
                        ),
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                ),
                html.Div(
                    [
                        html.P('Choose Region:'),
                        dcc.RadioItems(
                                id = 'Country',
                                options=[{'label': k, 'value': k} for k in all_options_t.keys()],
                                value='All',
                                labelStyle={'display': 'inline-block'}
                        ),
                    ],
                    className='six columns',
                    style={'margin-top': '10'}
                ),    
            ], className="row"
        ),

        html.Div(
            [
            html.Div([
                dcc.Graph(
                    id='example-graph'
                        )
                    ], className= 'six columns'
                ),

                html.Div([
                dcc.Graph(
                    id='example-graph-2',

                )
                ], className= 'six columns'
                )
            ], className="row")
		])
	],className = 'ten columns offset-by-one')
])	


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
                color='#7f7f7f'),
                # range = [df[(df[df.columns[0]].isin(province))&(df[df.columns[3]].isin(product))&(df[df.columns[1]].isin(account))].sum().index[4:].min(),df[(df[df.columns[0]].isin(province))&(df[df.columns[3]].isin(product))&(df[df.columns[1]].isin(account))].sum().index[4:].max()]

            ),
            'yaxis' : dict(
                # title='y Axis',
                titlefont=dict(
                family='Helvetica, monospace',
                size=10,
                color='#7f7f7f'),
                # range = [df[df.columns[-2]].min(),df[df.columns[-2]].max()]
                
            ),
            'transition': {
            	'duration' : 500,
            	'easing' : 'cubic-in-out' 	
            	}    
        }
    }

	return figure
################## Second Chart #################
@app.callback(
    Output('Product2', 'options'),
    [Input('Brand2', 'value')])

def set_product_options(selected_brand_for_product2):

	return [{'label': i, 'value': i} for i in all_options_p[selected_brand_for_product2]]

@app.callback(
    Output('Account2', 'options'),
    [Input('Brand2', 'value')])

def set_brands_options(selected_brand2):

	return [{'label': i, 'value': i} for i in all_options[selected_brand2]]

@app.callback(
    Output('Province2', 'options'),
    [Input('NS2', 'value')])

def set_cities_options(selected_region2):

	return [{'label': i, 'value': i} for i in north_south[selected_region2]]


@app.callback(
    Output('output-text2','children'),
    [Input('Province2','value'),
    Input('Account2','value'),
    Input('Brand2','value'),
    Input('Product2','value')])
def update_text(province2,account2,brand2,product2):

    return '{} Province,{} account and, {} product has been selected'.format(province2,account2,product2,df[df.columns[1]].isin(all_options[brand2]).index[4:])

@app.callback(
    Output('sell_out2','figure'),
    [Input('Brand2','value'),
    Input('Province2','value'),
    Input('Account2','value'),
    Input('Product2','value')])

def sell_out(brand2,province2,account2,product2):
	if brand2 == "HUAWEI":
		color = 'E94713' 
	else:
		color = '3CBCD6'
	data = [{'x': df[(df[df.columns[0]].isin(province2))&(df[df.columns[3]].isin(product2))&(df[df.columns[1]].isin(account2))].sum().index[4:],
            'y': df[(df[df.columns[0]].isin(province2))&(df[df.columns[3]].isin(product2))&(df[df.columns[1]].isin(account2))].sum().values[4:],
            'type': 'line',
            'marker': {'color': color}}]

	figure = {
        'data': data,
        'layout': {
            'title': province2,
            'xaxis' : dict(
                # title='x Axis',
                titlefont=dict(
                family='Courier New, monospace',
                size=10,
                color='#7f7f7f'),
                # range = [df[(df[df.columns[0]].isin(province))&(df[df.columns[3]].isin(product))&(df[df.columns[1]].isin(account))].sum().index[4:].min(),df[(df[df.columns[0]].isin(province))&(df[df.columns[3]].isin(product))&(df[df.columns[1]].isin(account))].sum().index[4:].max()]

            ),
            'yaxis' : dict(
                # title='y Axis',
                titlefont=dict(
                family='Helvetica, monospace',
                size=10,
                color='#7f7f7f'),
                # range = [df[df.columns[-2]].min(),df[df.columns[-2]].max()]
                
            ),
            'transition': {
            	'duration' : 500,
            	'easing' : 'cubic-in-out' 	
            	}    
        }
    }

	return figure
################## Second Tab ###################

@app.callback(
    dash.dependencies.Output('Cities', 'options'),
    [dash.dependencies.Input('Country', 'value')])

def set_cities_options(selected_region):
    return [{'label': i, 'value': i} for i in all_options_t[selected_region]]

@app.callback(
    dash.dependencies.Output('example-graph', 'figure'),
    [dash.dependencies.Input('Cities', 'value')])
        
def update_image_src(selector):
    data = []
    for city in selector:
        data.append({'x': city_data[city]['Date'], 'y': city_data[city]['SO'],
                    'type': 'bar', 'name': city})
 
    figure = {
        'data': data,
        'layout': {

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
                size=20,
                color='#7f7f7f'
            )),
            'transition': {
                'delay' : 500,
                'easing' : 'cubic-in-out'
            }    
        }
    }
    return figure


@app.callback(
    dash.dependencies.Output('example-graph-2', 'figure'),
    [dash.dependencies.Input('Cities', 'value')])
def update_image_src(selector):
    data = []
    for city in selector:
        data.append({'x': city_data[city]['Date'], 'y': city_data[city]['SO'],
                    'type': 'line', 'name': city})
    figure = {
        'data': data,
        'layout': {

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
            )),
            'transition': {
                'delay' : 500,
                'easing' : 'cubic-in-out'
            }
        }
    }
    return figure



if __name__ == '__main__':
    app.server.run(debug=True, threaded=True)
# (debug=True, port=8054,dev_tools_ui=False, dev_tools_props_check=False)