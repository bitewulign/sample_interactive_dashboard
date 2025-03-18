# importing the required libraries
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Load the dataset 
df = pd.read_csv('data/Cleaned_ObesityDataSet_raw_and_data_sinthetic.csv')

# Selecting relevant features
features = list(df.columns) 
df = df[features]

# Initialize the Dash app
app = dash.Dash(__name__)
server = app.server  # For deployment

# Define categorical features
categorical_features = ['Gender', 'family_history_with_overweight', 'FAVC', 'CAEC', 'SMOKE', 'SCC', 'CALC', 'MTRANS']

# Create an app layout
app.layout = html.Div(children=[
    html.H1("Obesity Levels Dashboard", style={'textAlign': 'center', 'fontWeight': 'bold', 'fontSize': 30}),
    
    # Dropdown for selecting categorical feature
    html.Label("Select a Feature:", style={'fontWeight': 'bold'}),
    dcc.Dropdown(
        id='feature-dropdown',
        options=[{'label': col, 'value': col} for col in categorical_features],
        value='Gender',
        placeholder="Select a categorical feature",
        searchable=True
    ),
    html.Br(),
    
    # Dropdown for selecting category within feature
    html.Label("Select a Category:", style={'fontWeight': 'bold'}),
    dcc.Dropdown(id='category-dropdown', placeholder="Select a category", searchable=True),
    html.Br(),
    
    # Graph output
    html.Div([dcc.Graph(id='piechart-output')]),
    html.Br(),
])

@app.callback(
    Output('category-dropdown', 'options'),
    Input('feature-dropdown', 'value')
)
def update_category_options(selected_feature):
    unique_values = df[selected_feature].unique()
    return [{'label': 'All', 'value': 'All'}] + [{'label': val, 'value': val} for val in unique_values]

@app.callback(
    Output('piechart-output', 'figure'),
    [Input('feature-dropdown', 'value'), Input('category-dropdown', 'value')]
)
def update_pie_chart(selected_feature, selected_category):
    if not selected_category or selected_category == 'All':
        fig = px.pie(df, names='NObeyesdad', title=f'Obesity Level Distribution Across All {selected_feature}')
    else:
        filtered_df = df[df[selected_feature] == selected_category]
        fig = px.pie(filtered_df, names='NObeyesdad', title=f'Obesity Level Distribution for {selected_category} in {selected_feature}')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True, port=8053)