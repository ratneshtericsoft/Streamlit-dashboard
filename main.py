import streamlit as st
from db_utils import db
import pandas as pd


def get_data(table):
    data = db[table].find({})
    return data

clients = list(get_data("clients"))
appointments = list(get_data("appointments"))
invoices = list(get_data("invoices"))
receipts = list(get_data("receipts"))



def calculate_percentage_change(current, last):
    return ((current - last) / last) * 100

# Calculate changes
changes = {
    'clients': len(clients),
    'appointments': len(appointments),
    'invoices': len(invoices),
    'receipts': len(receipts)
}

# Streamlit app
st.title('Kinergy Dashboard')

# Create cards
for key, value in changes.items():
    color = 'green' if value > 0 else 'red'
    st.markdown(f"""
        <div style="background-color: {color}; padding: 10px; border-radius: 5px; margin-bottom: 10px;">
            <h3>{key.capitalize()}</h3>
            <p style="font-size: 24px;">{value}</p>
        </div>
    """, unsafe_allow_html=True)





