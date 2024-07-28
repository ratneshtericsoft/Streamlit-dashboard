
import pymongo
import streamlit as st

@st.cache_resource
def init_connection():
    connection_string = st.secrets["mongo"]["uri"]
    return pymongo.MongoClient(connection_string)

client = init_connection()
db = client["kinergy-admin"]
