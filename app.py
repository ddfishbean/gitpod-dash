import dash
from dash import dash_table
from dash import dcc # dash core components
from dash import html
from dash.dependencies import Input, Output

import pandas as pd

df = pd.read_csv('https://bit.ly/elements-periodic-table')

app = dash.Dash(__name__)

# allows the user to select their own index, columns, and values columns
# via a dropdown component
app.layout = html.Div(
    className="main",
    children=[
        html.H2('Pivot tables: element periodic table'),
        html.Label('row index:'),
        html.Div([
            dcc.Dropdown(
                id='df-index',
                options=[{'label': i, 'value': i} for i in df.columns],
                value='Period'
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.Br(),
        html.Label('columns:'),
        html.Div([
            dcc.Dropdown(
                id='df-columns',
                options=[{'label': i, 'value': i} for i in df.columns],
                value='Group'
            )
        ], style={'width': '48%', 'display': 'inline-block'}),
        
        html.Br(),
        html.Label('entries:'),
        html.Div([
            dcc.Dropdown(
                id='df-values',
                options=[{'label': i, 'value': i} for i in df.columns],
                value='Element'
            )
        ], style={'width': '48%', 'display': 'inline-block'}),

        html.Br(),
        dash_table.DataTable(
            id='table',
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict('records'))
            ]
)

# collect input and render the pivot table
@app.callback(
    Output(component_id='table', component_property='columns'),
    Output(component_id='table', component_property='data'),
    Input(component_id='df-index', component_property='value'),
    Input(component_id='df-columns', component_property='value'),
    Input(component_id='df-values', component_property='value')
)

# update and render the pivot table automatically, aggfunc=list
def update_table(updated_index, updated_column, updated_values):
    df_updated = df.pivot_table(
        index=updated_index,
        columns=updated_column, 
        values=updated_values,
        aggfunc=list
    )

    columns=[{"name": i, "id": i} for i in pd.DataFrame(df_updated.to_records()).columns]
    data=df_updated.to_dict('records')
    return columns, data
    
    
app.run_server(debug=True, host="0.0.0.0")