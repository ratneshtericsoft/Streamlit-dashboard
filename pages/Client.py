import streamlit as st
from db_utils import db
import pandas as pd
import plotly.express as px
from datetime import date
import datetime


gender_mapping = {
    '': "Others",
    'female': "Female",
    'male': "Male",
    'gender_fluid': 'Gender Fluid',
    'androgyne': 'Androgyne',
    'agender': 'Agender'
}

def get_clients():
    data = db["clients"].find({})
    return pd.DataFrame(data)


clients = get_clients()

# Map the gender values
clients['gender'] = clients['gender'].map(gender_mapping)

st.write(clients)


# Count the number of each gender
gender_counts = clients['gender'].value_counts().reset_index()
gender_counts.columns = ['gender', 'count']

# Create a bar chart with Plotly
fig = px.bar(gender_counts, x='gender', y='count', title='Gender Distribution',
             labels={'gender': 'Gender', 'count': 'Count'}, text='count')

# Update the layout to display the count on hover
fig.update_traces(texttemplate='%{text}', textposition='outside')
fig.update_layout(hovermode='x unified')

# Display the bar chart in Streamlit
st.title('Gender Distribution')
st.plotly_chart(fig)


def get_age(dob, unit='years'):
    today = datetime.date.today()
    if unit == 'years':
        age = today.year - dob.year
        if today.month < dob.month or (today.month == dob.month and today.day < dob.day):
            age -= 1
    elif unit == 'months':
        age = (today.year - dob.year) * 12 + today.month - dob.month
        if today.day < dob.day:
            age -= 1
    elif unit == 'days':
        age = (today - dob).days
    return age

clients_dob_list = list(clients["dob"])
clients_dob_list = [item.rsplit('T')[0] for item in clients_dob_list if item]

# print(clients_dob_list)

clients_dob_list = list(clients["dob"])
clients_dob_list = [item.rsplit('T')[0] for item in clients_dob_list if item]

# Create a select box for the unit of age
unit = st.selectbox("Select age unit", ['years', 'months', 'days'], index=0)

# Calculate age for each client
ages = [get_age(date.fromisoformat(dob), unit) for dob in clients_dob_list]

# Create a DataFrame with the ages
age_df = pd.DataFrame(ages, columns=['age'])

# Plot the bar graph
fig = px.histogram(age_df, x='age', nbins=20, title=f'Age Distribution in {unit.capitalize()}')
st.plotly_chart(fig)