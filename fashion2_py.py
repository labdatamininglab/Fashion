import pandas as pd
import numpy as np
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

df0 = pd.read_csv('frq_items.csv')
df1 = df0.drop(columns=['Unnamed: 0', 'support'], inplace=False)

df1['Item'] = df1['itemsets'].astype(str).str.extract(r"\{(.+?)\}")

unique_items = [item.strip() for sublist in df1['Item'].str.split(',') for item in sublist]

unique_items = list(set(unique_items))

unique_items.sort()

cleaned_items = [item.strip().strip("'") for item in unique_items]

list_one = []
list_two = []
list_three = []

# Iterate over each row in the dataframe
for index, row in df1.iterrows():
    # Split the itemsets by comma and remove the leading and trailing whitespace
    items = [item.strip().strip("'") for item in row['Item'].split(',')]
    # Based on the number of items in the row, append to the respective list
    if len(items) == 1:
        list_one.append(items)
    elif len(items) == 2:
        list_two.append(items)
    elif len(items) == 3:
        list_three.append(items)


combo_list = cleaned_items

df1 = pd.read_csv('df1.csv')
color_counts = df1.groupby('Color').size()
season_counts = df1.groupby('Season').size()
shipping_counts = df1.groupby('Shipping Type').size()
discount_counts = df1.groupby('Discount Applied').size()
payment_counts = df1.groupby('Payment Method').size()
age_counts = df1.groupby('Age').size()
sum_purchase = df1.groupby('Purchased')['Purchase Amount (USD)'].sum()
sum_location = df1.groupby('Location')['Purchase Amount (USD)'].sum()
sum_age = df1.groupby('Age')['Purchase Amount (USD)'].sum()



# Initialize the Dash app
app = dash.Dash(__name__)




app.layout = html.Div(
    children=[
        dcc.Dropdown(
            id='combo-dropdown',
            options=[{'label': item, 'value': item} for item in combo_list],
            placeholder="Select an item"
        ),

        html.Br(),
        html.Div(
            id='output-field',
            style={
                'backgroundColor': 'yellow',
                'fontSize': '24px',
                'textAlign': 'center'
            }
        ),




        html.Div(
            dcc.Graph(
                id='histogram',
                figure=px.histogram(sum_purchase, x=sum_purchase.index, y=sum_purchase.values),
                style={
                    'width': '50%',
                    'display': 'inline-block',
                    'verticalAlign': 'top',
                    'textAlign': 'right'
                }
            ),
            style={'margin-right': '20px'}  
        ),


        html.Div(
            dcc.Graph(
                id='histogram',
                figure=px.histogram(sum_location, x=sum_location.index, y=sum_location.values, nbins=20),
                style={
                    'width': '50%',
                    'display': 'inline-block',
                    'verticalAlign': 'top',
                    'textAlign': 'right'
                }
            ),
            style={'margin-right': '20px'}  
        ),


        html.Div(
            dcc.Graph(
                id='histogram',
                figure=px.histogram(season_counts, x=season_counts.index, y=season_counts.values),
                style={
                    'width': '50%',
                    'display': 'inline-block',
                    'verticalAlign': 'top',
                    'textAlign': 'right'
                }
            ),
            style={'margin-right': '20px'}  
        ),


        html.Div(
            dcc.Graph(
                id='histogram',
                figure=px.histogram(payment_counts, x=payment_counts.index, y=payment_counts.values, nbins=20),
                style={
                    'width': '50%',
                    'display': 'inline-block',
                    'verticalAlign': 'top',
                    'textAlign': 'right'
                }
            ),
            style={'margin-right': '20px'}  
        ),


   


        html.Div(
            dcc.Graph(
                id='histogram',
                figure=px.histogram(shipping_counts, x=shipping_counts.index, y=shipping_counts.values, nbins=20),
                style={
                    'width': '50%',
                    'display': 'inline-block',
                    'verticalAlign': 'top',
                    'textAlign': 'right'
                }
            ),
            style={'margin-right': '20px'}  
        ),


        html.Div(
            dcc.Graph(
                id='histogram',
                figure=px.histogram(discount_counts, x=discount_counts.index, y=discount_counts.values, nbins=20),
                style={
                    'width': '50%',
                    'display': 'inline-block',
                    'verticalAlign': 'top',
                    'textAlign': 'right'
                }
            ),
            style={'margin-right': '20px'}  
        ),


        html.Div(
            dcc.Graph(
                id='line-plot',
                figure=px.line(age_counts, x=age_counts.index, y=age_counts.values),  
                style={
                    'width': '50%',
                    'display': 'inline-block',
                    'verticalAlign': 'top',
                    'textAlign': 'right'
                }
            ),
            style={'margin-right': '20px'}
        ),


        html.Div(
            dcc.Graph(
                id='line-plot',
                figure=px.line(sum_age, x=sum_age.index, y=sum_age.values),  
                style={
                    'width': '50%',
                    'display': 'inline-block',
                    'verticalAlign': 'top',
                    'textAlign': 'right'
                }
            ),
            style={'margin-right': '20px'}
        ),


        html.Div(
            dcc.Graph(
                id='pie-chart',
                figure=px.pie(color_counts, values=color_counts.values, names=color_counts.index),
                style={
                    'width': '50%',
                    'display': 'inline-block',
                    'verticalAlign': 'top',
                    'textAlign': 'left'
                }
            ),
            style={'margin-left': '20px'}  # Adjust margin for spacing
        )
    ]
)


@app.callback(
    Output('output-field', 'children'),
    [Input('combo-dropdown', 'value')]
)


def update_output(selected_item):
    recommendations = []
    for pair in list_two:
        if selected_item in pair:
            recommendations.append(pair[1] if pair[0] == selected_item else pair[0])
    return ', '.join(recommendations) if recommendations else ''

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)