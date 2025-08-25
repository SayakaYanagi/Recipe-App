import streamlit as st
import pymongo
from bson.objectid import ObjectId
import os
import mongomock

def set_page_config(page_title):

    """Set page config."""

    st.set_page_config(
            page_title = page_title,
            page_icon = '🧁',
            layout = 'wide',
            menu_items = {'Get Help': None, 'Report a bug': None,'About': None},
        )
    
@st.cache_resource
def init_connection():

    """Initialise the MongoDB database connection"""

    if os.getenv('MOCK_DB') == '1':
        client = mongomock.Connection()
    else:
        mongo_uri = st.secrets['mongo']['uri']
        client = pymongo.MongoClient(mongo_uri)
    return client

client = init_connection()


def connect_to_db_collection(client):

    """Connect to Mongo DB collection"""

    database_name = st.secrets['mongo']['database']
    collection_name = st.secrets['mongo']['collection']

    db = client[database_name]
    collection = db[collection_name]

    return collection