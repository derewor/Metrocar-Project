#!/usr/bin/env python
# coding: utf-8

# In[1]:


get_ipython().system('pip install dash')
get_ipython().system('pip install jupyter-dash')
get_ipython().system('pip install plotly')


# In[3]:


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


# In[5]:


transactions = pd.read_sql("SELECT * FROM transactions",connection)
signups = pd.read_sql("SELECT * FROM signups",connection)
ride_requests = pd.read_sql("SELECT * FROM ride_requests",connection)
reviews = pd.read_sql("SELECT * FROM reviews",connection)
app_downloads = pd.read_sql("SELECT * FROM app_downloads",connection)


# In[6]:


two_tables = ride_requests.merge(transactions, how='left', on='ride_id')
three_tables = two_tables.merge(reviews, how='left', on='ride_id')
four_tables = three_tables.merge(signups, how='outer', left_on='user_id_x', right_on='user_id')
all_in_one = four_tables.join(app_downloads, how='outer')
all_in_one['month'] = all_in_one['request_ts'].dt.month.fillna(0).astype(int)
all_in_one['hour'] = all_in_one['request_ts'].dt.hour.fillna(99).astype(int)


# In[9]:


def month_number_to_name(month):
    return calendar.month_name[month]
all_in_one['month_name'] = all_in_one['month'].apply(month_number_to_name)


# In[11]:


all_in_one['has_request'] = all_in_one['request_ts'].notnull()
all_in_one['has_accept'] = all_in_one['accept_ts'].notnull()
all_in_one['has_dropoff'] = all_in_one['dropoff_ts'].notnull()
all_in_one['has_review'] = all_in_one['review'].notnull()


# In[13]:


user_ride = {
    'download': all_in_one.groupby('age_range')['app_download_key'].nunique(),
    'signups': all_in_one.groupby('age_range')['session_id'].nunique(),
    'ride_request': all_in_one[all_in_one['has_request']].groupby('age_range')['user_id'].nunique(),
    'ride_accepted': all_in_one[all_in_one['has_accept']].groupby('age_range')['user_id'].nunique(),
    'ride_completed': all_in_one[all_in_one['has_dropoff']].groupby('age_range')['user_id'].nunique(),
    'reviewed': all_in_one[all_in_one['has_review']].groupby('age_range')['user_id'].nunique()
}
user_ride_df = pd.DataFrame(user_ride)
user_ride_df.columns = ['downloaded', 'signed_up', 'ride_requested','ride_accepted','ride_completed','reviewed']


# In[21]:


df_user = user_ride_df.reset_index()
df_user


# In[ ]:





# In[45]:


app = dash.Dash()
app.layout = html.Div(children=[
        html.H1(children="Ride users dashboard!"),
        dcc.Dropdown(id='age_dropdown',
                     options=[{'label':age, 'value':age}
                              for age in df_user['age_range']],
                     value='18-24'),
    dcc.Graph(id='user_ride_graph')])

# # Define the callback to update the output
@app.callback(
Output(component_id='user_ride_graph', component_property='figure'),
        Input('age_dropdown', 'value'))
def update_graph(selected_age):
    filtered_data = df_user[df_user['age_range']==selected_age]
    if not filtered_data.empty:
        funnel_data = {
            'Stage': ['Downloaded', 'Signed Up', 'Ride Requested', 'Ride Accepted', 'Ride Completed', 'Reviewed'],
            'Count': [
                filtered_data['downloaded'].values[0],
                filtered_data['signed_up'].values[0],
                filtered_data['ride_requested'].values[0],
                filtered_data['ride_accepted'].values[0],
                filtered_data['ride_completed'].values[0],
                filtered_data['reviewed'].values[0]
            ]
        }
        funnel_df = pd.DataFrame(funnel_data)
        funnel_fig = px.funnel(funnel_df, x='Count', y='Stage', title=f'Funnel for {selected_age} Age Range')
    else:
        funnel_fig = px.funnel([], x='Count', y='Stage', title='No Data Available')
    return funnel_fig
if __name__ == '__main__':
    app.run_server(debug=True)


# In[25]:


user_rate = df_user.copy() #not to destort the original data
user_rate = pd.DataFrame(user_rate)


# In[27]:


for value in user_rate.columns[1:]:
    user_rate[f'{value}_rate'] = round(user_rate[value] / user_rate['downloaded'] * 100, 2)
print(user_rate)


# In[29]:


user_rate


# In[31]:


user_rate_selected = user_rate[user_rate.columns[[0,7,8,9,10,11,12]]]


# In[33]:


user_rate_selected


# In[43]:


# app = dash.Dash()
# app.layout = html.Div(children=[
#         html.H1(children="Ride request per day dashboard!"),
#         dcc.Dropdown(id='age_dropdown',
#                      options=[{'label':age, 'value':age}
#                               for age in user_rate_selected['age_range']],
#                      value='18-24'),
#     dcc.Graph(id='user_ride_graph')])

# # # Define the callback to update the output
# @app.callback(
# Output(component_id='user_ride_graph', component_property='figure'),
#         Input('age_dropdown', 'value'))
# def update_graph(selected_age):
#     filtered_data = user_rate_selected[user_rate_selected['age_range']==selected_age]
#     if not filtered_data.empty:
#         funnel_data = {
#             'Stage': ['Downloaded', 'Signed Up', 'Ride Requested', 'Ride Accepted', 'Ride Completed', 'Reviewed'],
#             'Count': [
#                 filtered_data['downloaded'].values[0],
#                 filtered_data['signed_up'].values[0],
#                 filtered_data['ride_requested'].values[0],
#                 filtered_data['ride_accepted'].values[0],
#                 filtered_data['ride_completed'].values[0],
#                 filtered_data['reviewed'].values[0]
#             ]
#         }
#         funnel_df = pd.DataFrame(funnel_data)
#         funnel_fig = px.funnel(funnel_df, x='Count', y='Stage', title=f'Funnel for {selected_age} Age Range')
#     else:
#         funnel_fig = px.funnel([], x='Count', y='Stage', title='No Data Available')
#     return funnel_fig
# if __name__ == '__main__':
#     app.run_server(debug=True)


# In[ ]:




