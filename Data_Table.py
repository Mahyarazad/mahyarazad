import pandas as pd
import dash_table
import dash
import glob
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
path  = "D:/Data/Py_Files/*.xlsx"
save_path = "D:/Data/Py_Files"
filenames = []
for i in glob.iglob(path, recursive=True):
    filenames.append(i)
df = pd.read_excel(filenames[0])


df['index'] = range(1,len(df)+1)


PageSize = 50


app = dash.Dash(__name__, external_stylesheets = [
        'https://codepen.io/chriddyp/pen/bWLwgP.css'
    ])

app.layout = html.Div([
		dash_table.DataTable(
			id = 'table1',
			columns = [{'name':i,'id':i} for i in sorted(df.columns)],
			page_current = 0,
			page_size = PageSize,
			page_action = 'custom'
		),
		html.Br(),
		dcc.Checklist(
			id = 'use-table1',
			options = [{'label':'Use page_count', 'value':'True'}],
			value = ['True']
			),
		dcc.Input(
			id = 'count-table1',
			type = 'number',
			min = 1,
			max = 50,
			value = 20

			)
	]
)

@app.callback(
	Output('table1','data'),
	[Input('table1','page_current'),
	Input('table1','page_size')]
	)
def select_page(page_current,page_size):
	return df.iloc[page_current*page_size:(page_current+1)*page_size].to_dict('records')


@app.callback(
	Output('table1','page_count'),
	[Input('use-table1','value'),
	Input('count-table1','value')]
	)	
def count(use_table1,count_table1):
	if len(use_table1)==0 or count_table1 == None:
		return None
	return count_table1	 
if __name__ == '__main__':
	app.run_server(port = 8088, debug = True )