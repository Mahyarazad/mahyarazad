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
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from reshape import reshape
import base64


url = 'https://github.com/Mahyarazad/mahyarazad/raw/master/Base.xlsx'
df = pd.read_excel(url)

#####  DataFrame Reshaping #####
sd = reshape(df).summation
city_data = reshape(df).dict_data_gen
cv = reshape(df).geo
cvt = cv.drop(columns = [cv.columns[3],cv.columns[4]])
cvt['MOM Ratio'] = ((cvt[cvt.columns[-1]]- cvt[cvt.columns[-2]])/cvt[cvt.columns[-2]]).apply('{:.0%}'.format)
cvt = cvt.sort_values(by=cvt.columns[3],ascending = False)


#################################


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

#### Map and Table


ccs=px.colors.sequential.Plasma_r
fig = go.Figure()
fig.add_trace(go.Scattermapbox(
        lat=cv[cv.columns[3]],
        lon=cv[cv.columns[4]],
        mode='markers',
        marker=go.scattermapbox.Marker(
            size=(cv[cv.columns[6]]/(cv[cv.columns[6]].min()/2.5)),
            color= cv[cv.columns[6]],
            opacity=0.6,
            showscale=True,
            colorscale = px.colors.sequential.Blackbody,
            cmin=min(cv[cv.columns[-1]]),
            cmax=max(cv[cv.columns[-1]])
        ),
        meta = [cv.columns[-1],cv.columns[-2]],
        hoverinfo= 'all',
        text = cv,
        hovertext = cv.iloc[:,1:],
        hovertemplate=
        " System Name: %{text[0]} <br>" +
		"<extra></extra>" +
        "<b> Province Name: %{text[1]}</b><br><br>" +
        "<b>Accumulated %{meta[0]}: %{text[5]:,}</b><br>" +
        "<b>Accumulated %{meta[1]}: %{text[6]:,}</b><br>" +
        "<span style='color: Cornsilk'>Population at 2018: %{text[2]:,} Thousand</span> <br>"

    ))

fig.update_layout(
    autosize=True,
    hovermode='closest',
    showlegend=False,
    mapbox=dict(
        accesstoken='pk.eyJ1IjoibWFoeWFyYXphZCIsImEiOiJjazh3cHk2eWUwY3huM29xb29meXV1bGV2In0.kKV6XDb8gngFsl4EZMeXPg',
        bearing=0,
        center=dict(
            lat=33.67,
            lon=44
        ),
        pitch=0,
        zoom=5,
        style='light'
    ),
    height =800
)



table = go.Figure(data = [go.Table(
	header = dict(
		values = [cvt.columns[0],cvt.columns[-3],cvt.columns[-2],cvt.columns[-1]],
		fill_color = 'royalblue',
		line_color='darkslategray',
		align = 'center',
	    font=dict(color='white', size=13),
    	height=40
		),
	cells = dict(values = 
		[cvt[cvt.columns[0]],cvt[cvt.columns[-3]],cvt[cvt.columns[-2]],cvt[cvt.columns[-1]]],
	fill_color = 'lavender',
	align = ['left','center','center','center'],
	line_color='darkslategray',
	font_size = 12,
	height = 20))
	# uirevision = colorbar_title),


])

table.update_layout(
	height = 800,
	width = 600
	)


####### Main App ######
server = flask.Flask(__name__)
server.secret_key = os.environ.get('secret_key', str(randint(0, 1000000)))
image_filename = 'BarchartRace.gif'
encoded_image = base64.b64encode(open(image_filename, 'rb').read()).decode('ascii')

app = dash.Dash(__name__,server=server,
                external_stylesheets = [
        'https://codepen.io/chriddyp/pen/bWLwgP.css'
    ]
                )

# app.scripts.config.serve_locally = True
# app.css.config.serve_locally = True
app.title = 'Iraq Device Business Summary'
app.layout = html.Div([

	# html.Link(href='regionaldata.css', rel='stylesheet'),
	dcc.Tabs([
		dcc.Tab(label='HUAWEI Distribution and Sales Figure',style = {
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
			html.H2('2019 Sales Overview in Middle east, Africa and, North Africa'),
			html.Br(),
			html.Div(html.Img(src='data:image/gif;base64,{}'.format(encoded_image)),
			className = 'row'),
			html.H2('Iraq Activated Stock Distribution'),
			html.Div(
	            [
	            html.Div([
	                dcc.Graph(
	                    figure=fig
	                        )
	                    ], className= 'seven columns'
	                ),

	                html.Div([
	                dcc.Graph(
	                    figure = table

	                )
	                ], className= 'five columns'
	                )
	            ], className="row"),

			html.Br(),
			html.H2('HUAWEI Handset Activation Trend'),	
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
		]),

		dcc.Tab(label = 'Distribution Trend Dashboard',style = {
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
						html.H3('HUAWEI and HONOR Device Sales Trend'),
						html.P('If you choose "ALL product" in the second dropdown, please unchek the shipping account (Global, Euro or, Jibal) before swtiching to other brand, otherwise it shows the summation over both brands.',
							style = {'color':'red'}),
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
					    value = '',
					    options=[
					        {'label': i, 'value':i} for i in sd[sd.columns[0]].unique()]
					    ),
					    html.Br(),
					    dcc.Dropdown(
					    id = 'Product',
					    style={'height': '30px', 'width': '200px'},
					    value = '',
					    multi = True,
					    options=[
					        {'label': i, 'value':i} for i in sd[sd.columns[3]].unique()
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
                                {'label': i, 'value':i} for i in sd[sd.columns[0]].unique()]
                            ),
                            html.Br(),
                            dcc.Dropdown(
                            id = 'Product2',
                            style={'height': '30px', 'width': '200px'},
                            value = 'Baghdād',
                            multi = True,
                            options=[
                                {'label': i, 'value':i} for i in sd[sd.columns[3]].unique()
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
 	],className = 'ten columns offset-by-one')
],className = 'ten columns offset-by-one')	


									#CALL BACK
########################################################################################
########################################################################################

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

    return '{} Province,{} account and, {} product has been selected'.format(province,account,product,sd[sd.columns[1]].isin(all_options[brand]).index[4:])

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
	data = [{'x': sd[(sd[sd.columns[0]].isin(province))&(sd[sd.columns[3]].isin(product))&(sd[sd.columns[1]].isin(account))].sum().index[4:],
            'y': sd[(sd[sd.columns[0]].isin(province))&(sd[sd.columns[3]].isin(product))&(sd[sd.columns[1]].isin(account))].sum().values[4:],
            'type': 'line',
            'marker': {'color': color}}]

	figure = {
        'data': data,
        'layout': {
            'title': province,
            'xaxis' : dict(

                titlefont=dict(
                family='Courier New, monospace',
                size=10,
                color='#7f7f7f'),
                
            ),
            'yaxis' : dict(

                titlefont=dict(
                family='Helvetica, monospace',
                size=10,
                color='#7f7f7f'),

                
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

    return '{} Province,{} account and, {} product has been selected'.format(province2,account2,product2,sd[sd.columns[1]].isin(all_options[brand2]).index[4:])

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
	data = [{'x': sd[(sd[sd.columns[0]].isin(province2))&(sd[sd.columns[3]].isin(product2))&(sd[sd.columns[1]].isin(account2))].sum().index[4:],
            'y': sd[(sd[sd.columns[0]].isin(province2))&(sd[sd.columns[3]].isin(product2))&(sd[sd.columns[1]].isin(account2))].sum().values[4:],
            'type': 'line',
            'marker': {'color': color}}]

	figure = {
        'data': data,
        'layout': {
            'title': province2,
            'xaxis' : dict(
                titlefont=dict(
                family='Courier New, monospace',
                size=10,
                color='#7f7f7f'),
                

            ),
            'yaxis' : dict(
                titlefont=dict(
                family='Helvetica, monospace',
                size=10,
                color='#7f7f7f'),
                
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

                titlefont=dict(
                family='Courier New, monospace',
                size=10,
                color='#7f7f7f'
            )),
            'yaxis' : dict(

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

                titlefont=dict(
                family='Courier New, monospace',
                size=10,
                color='#7f7f7f'
            )),
            'yaxis' : dict(

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