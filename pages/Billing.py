import streamlit as st
from db_utils import db
import pandas as pd
import plotly.express as px
import numpy as np


def get_bills(bill_type):
    data = db[bill_type].find({})
    return pd.DataFrame(data)

invoices = get_bills("invoices")
receipts = get_bills("receipts")


bills = pd.concat([invoices, receipts], ignore_index=True)


bills['status'] = bills.apply(lambda x: 'paid' if 'payment_mode' in x and pd.notna(x['payment_mode']) else 'unpaid', axis=1)


# Streamlit app
st.title("Bills Analysis")


payment_for = st.selectbox("Select Payment For", options=["appointment", "products"])


if payment_for == "appointment":
    record_type = st.selectbox("Select Record Type", options=["medical_record", "performance_record"])

filtered_bills = bills[bills['payment_for'] == payment_for]

if payment_for == "appointment":
    filtered_bills = filtered_bills[filtered_bills['record_type'] == record_type]


status_counts = filtered_bills['status'].value_counts().reset_index()
status_counts.columns = ['status', 'count']

status_amounts = filtered_bills.groupby('status')['payable_amount'].sum().reset_index()
status_amounts.columns = ['status', 'payable_amount']

# Merge counts and amounts
status_data = pd.merge(status_counts, status_amounts, on='status')


fig = px.pie(status_data, values='payable_amount', names='status', hole=0.5,
             title=f'Payable Amount and Count of {payment_for.capitalize()} Bills (Paid vs Unpaid)',
             custom_data=['count'],
             labels={'payable_amount': 'Total Payable Amount', 'count': 'Count'})

fig.update_traces(hovertemplate='<b>%{label}</b><br>Payable Amount: %{value}$<br>Count: %{customdata[0]}')

# Display the chart
st.plotly_chart(fig)


