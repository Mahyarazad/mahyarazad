import dash
from dash.dependencies import Input, Output
import dash_table
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import matplotlib.pyplot as plt
from datetime import date
import glob 
import numpy as np
### Save PNG ###
import base64
from io import BytesIO

path  = "C:/Users/m84123311/Downloads/*.xlsx"
save_path = "C:/Users/m84123311/Downloads/"
filenames = []
for i in glob.iglob(path, recursive=True):
    filenames.append(i)

df = pd.read_excel(filenames[0])
pd.set_option('display.max_columns',None)

north_list = {'Sell Out Province':[
                'As Sulaymānīyah',
                'Altameem',
                'Dahūk',
                'Arbīl',
                'Nīnawá',
                'Şalāḩ ad Dīn']}

south_list = {'Sell Out Province':[
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
                'Wāsiţ']}   
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



def south(df):
    south = pd.DataFrame(south_list)
    hwpd = pd.DataFrame(pd_list)    
    df = df.merge(south,on='Sell Out Province')
    df = df.merge(hwpd,on='Product')
    df = df[df['Product Brand']=='HUAWEI'].pivot_table(values = 'Qty',index='Sell Out Province',columns='Sell Out Date',aggfunc=sum)
    df = df.dropna()
    df = df.reset_index()
    df = df.sort_values(by=df.columns[1], ascending=True)
    return df


def north(df):
    north= pd.DataFrame(north_list)
    hwpd = pd.DataFrame(pd_list)
    df = df.merge(north,on='Sell Out Province')
    df = df.merge(hwpd,on='Product')    
    df = df[df['Product Brand']=='HUAWEI'].pivot_table(values = 'Qty',index='Sell Out Province',columns='Sell Out Date',aggfunc=sum)
    df = df.dropna()
    df = df.reset_index()
    df = df.sort_values(by=df.columns[1], ascending=True)
    return df

def trans(df):
    df = df[(df['Product Brand']=='HUAWEI')&(df['Sell Out Country/Region']!='Iraq')].pivot_table(values = 'Qty',index='Product',columns='Sell Out Date',aggfunc=sum)
    df = df.dropna()
    df = df.reset_index()
    df = df.sort_values(by=df.columns[1], ascending=True)
    return df
def mergeDict(dict1, dict2):
   ''' Merge dictionaries and keep values of common keys in list'''
   dict3 = {**dict1, **dict2}
   for key, value in dict3.items():
       if key in dict1 and key in dict2:
               dict3[key] = [value , dict1[key]]
 
   return dict3



north = pd.DataFrame(north_list)
south = pd.DataFrame(south_list)
df =df[df['Sell Out Country/Region']=='Iraq']
dfn = df.merge(north,on='Sell Out Province')
dfn['Region'] = 'North'
dfs = df.merge(south,on='Sell Out Province')
dfs['Region'] = 'South'

df = pd.concat([dfn,dfs])

df2 = df.pivot_table(values='Qty', index= ['Region','Sell Out Province','Product Brand'], columns = 'Sell Out Date',aggfunc=sum)
df2.columns = df2.columns.date
df2.reset_index(inplace = True)

# df2.rename(columns={df2.columns[3]:}, inplace=True)
# print(df2[(df2['Sell Out Province']=='Arbīl')&(df2['Product Brand']=='HUAWEI')].iloc[-1,-3:])
df3 = df2[(df2['Sell Out Province']=='Arbīl')&(df2['Product Brand']=='HUAWEI')].iloc[-1,-3:]

# for key, value in dic1.items():
#     print (value)

app = dash.Dash(__name__, external_stylesheets = [
        'https://codepen.io/chriddyp/pen/bWLwgP.css'
    ])


app.layout = html.Div(

    [
    html.Div(id='output-text',   style = {
    'color' : 'white',
    'background-color' : 'rgb(63,63,63)',
    'text-margin':'center',
    'font-family': "Amatic SC",
    'margin-left':'0px',
    'font-size': '20px'

    },children = ''),
    html.P('Choose Province:'),
    dcc.Dropdown(
        id = 'my-dropdown-widget',
        value = 'Arbīl',

        options=[
            {'label': i, 'value':i} for i in df2[df2.columns[1]].unique()
            ]
            
        ),
    html.P('Choose Brand:'),
    dcc.Dropdown(
        id = 'my-dropdown-widget2',
        value = 'HUAWEI',

        options=[
            {'label': i, 'value':i} for i in df2[df2.columns[2]].unique()
            ]
        
        ),
    html.Br(),

    html.Div([
        dcc.Graph(
            id='sell_out',
            )  
        
    ]),
])

@app.callback(
    Output('output-text','children'),
    [Input('my-dropdown-widget','value'),
    Input('my-dropdown-widget2','value')])
def update_text(province, brand):
    # dic = df2[(df2[df2.columns[1]]==province)&(df2[df2.columns[2]]==brand)].iloc[0,3:]
    return '    You have selected "{}" prvoince for "{}"'.format(province,brand)

@app.callback(
    Output('sell_out','figure'),
    [Input('my-dropdown-widget','value'),
    Input('my-dropdown-widget2','value')])

def sell_out(province, brand):
    if brand =='HUAWEI':
        color = '#F7431C'
    else:
        color = '3CBCD6'    
    data = [{'x': (df2[(df2[df2.columns[1]]==province)&(df2[df2.columns[2]]==brand)].iloc[0,3:]).index,
            'y': (df2[(df2[df2.columns[1]]==province)&(df2[df2.columns[2]]==brand)].iloc[0,3:]).values,
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
    app.run_server(debug=True, port=8054)