import streamlit as st
from db_utils import db
import pandas as pd
import plotly.express as px
import numpy as np


col1, col2, col3 = st.columns([1, 2, 1])
status_mapping = {
    'scheduled': "Scheduled",
    'no_show': "No Show",
    'cancelled': "Canceled",
    'no_provider': 'No Provider',
    'upcoming': 'Up Coming',
    'engaged': 'Engaged',
    'completed': "Completed"
}

def get_appointments():
    data = db["appointments"].find({})
    return pd.DataFrame(data)

appointments = get_appointments()

appointments["status"] = appointments["status"].map(status_mapping)


unique_record_types = list(appointments['record_type'].unique())
# Remove NaN and any other falsy values
cleaned_list = [item for item in unique_record_types if item and not (isinstance(item, float) and np.isnan(item))]


appointment_type = st.selectbox('Select Appointment type', ['All'] + list(appointments['appointment_type'].unique()))
record_type = st.selectbox('Slect Record type', ['All'] + cleaned_list)

if appointment_type !='All' and record_type !='All':
    filteredAppointments = appointments[
        (appointments['appointment_type'] == appointment_type) &
        (appointments['record_type'] == record_type)
    ]
elif appointment_type !='All':
    filteredAppointments = appointments[appointments['appointment_type'] == appointment_type]
elif record_type !='All':
    filteredAppointments = appointments[appointments['record_type'] == record_type]
else:
    filteredAppointments = appointments

filteredAppointmentsCount = filteredAppointments['status'].value_counts().reset_index()
filteredAppointmentsCount.columns = ['status', 'count']


fig = px.pie(filteredAppointmentsCount, names = "status", values = "count", title="Appointment status Distribution")

with col2: 
    st.plotly_chart(fig, use_container_width=True)
