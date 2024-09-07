#!/usr/bin/env python
# coding: utf-8

# In[ ]:





# In[4]:


get_ipython().system('pip install dash')
get_ipython().system('pip install jupyter-dash')
get_ipython().system('pip install plotly')


# In[5]:


import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd
from jupyter_dash import JupyterDash
import sqlalchemy as sa
import calendar
engine = sa.create_engine('postgresql://Test:bQNxVzJL4g6u@ep-noisy-flower-846766-pooler.us-east-2.aws.neon.tech/Metrocar')
connection = engine.connect().execution_options(isolation_level="AUTOCOMMIT")
inspector = sa.inspect(engine)
inspector.get_table_names()


# In[6]:


transactions = pd.read_sql("SELECT * FROM transactions",connection)
signups = pd.read_sql("SELECT * FROM signups",connection)
ride_requests = pd.read_sql("SELECT * FROM ride_requests",connection)
reviews = pd.read_sql("SELECT * FROM reviews",connection)
app_downloads = pd.read_sql("SELECT * FROM app_downloads",connection)


# In[7]:


# A step by step merging of the files
two_tables = ride_requests.merge(transactions, how='left', on='ride_id')
three_tables = two_tables.merge(reviews, how='left', on='ride_id')
four_tables = three_tables.merge(signups, how='outer', left_on='user_id_x', right_on='user_id')
#to ensure than all rows from both tables are included, we used .join function without a key.
all_in_one = four_tables.join(app_downloads, how='outer')
all_in_one['month'] = all_in_one['request_ts'].dt.month.fillna(0).astype(int)
all_in_one['hour'] = all_in_one['request_ts'].dt.hour.fillna(99).astype(int)


# In[8]:


def month_number_to_name(month):
    return calendar.month_name[month]
all_in_one['month_name'] = all_in_one['month'].apply(month_number_to_name)


# In[9]:


all_in_one['has_request'] = all_in_one['request_ts'].notnull()
all_in_one['has_accept'] = all_in_one['accept_ts'].notnull()
all_in_one['has_dropoff'] = all_in_one['dropoff_ts'].notnull()
all_in_one['transaction_approved'] = all_in_one['charge_status'] == 'Approved'
all_in_one['has_review'] = all_in_one['review'].notnull()


# In[10]:


rides = {
    'ride_request': all_in_one[all_in_one['has_request']].groupby('age_range')['request_ts'].count(),
    'ride_accepted': all_in_one[all_in_one['has_accept']].groupby('age_range')['accept_ts'].count(),
    'ride_completed': all_in_one[all_in_one['has_dropoff']].groupby('age_range')['dropoff_ts'].count(),
    'transaction_completed': all_in_one[all_in_one['transaction_approved']].groupby('age_range')['user_id'].count(),
    'reviewed': all_in_one[all_in_one['has_review']].groupby('age_range')['user_id'].count()
}
rides_df = pd.DataFrame(rides)
rides_dfs = pd.DataFrame(rides_df.reset_index())

#rides_dfs.info()
rides_dfs.columns = ['age_range','ride_requested','ride_accepted','ride_completed','transaction_completed','reviewed']


# In[11]:


rides_dfs.reset_index()


# In[12]:


app = dash.Dash()
app.layout = html.Div(children=[
        html.H1(children="Ride request per age group dashboard!"),
        dcc.Dropdown(id='age_dropdown',
                     options=[{'label':age, 'value':age}
                              for age in rides_dfs['age_range']],
                     value='18-24', style={'color': '#EF553B'}),
    dcc.Graph(id='user_ride_graph')])

# # Define the callback to update the output
@app.callback(
Output(component_id='user_ride_graph', component_property='figure'),
        Input('age_dropdown', 'value'))
def update_graph(selected_age):
    filtered_data = rides_dfs[rides_dfs['age_range']==selected_age]
    if not filtered_data.empty:
        funnel_data = {
            'Stage': ['ride_requested', 'ride_accepted', 'ride_completed','transaction_completed', 'reviewed'],
            'Count': [
                filtered_data['ride_requested'].values[0],
                filtered_data['ride_accepted'].values[0],
                filtered_data['ride_completed'].values[0],
                filtered_data['transaction_completed'].values[0],
                filtered_data['reviewed'].values[0]
            ]
        }
        funnel_df = pd.DataFrame(funnel_data)
        funnel_fig = px.funnel(funnel_df, x='Count', y='Stage', title=f'Funnel for {selected_age} Age Range')
    else:
        funnel_fig = px.funnel([], x='Count', y='Stage', title='No Data Available')
                            
    return funnel_fig
if __name__ == '__main__':
    app.run_server(mode='inline', port=8052)


# In[ ]:




