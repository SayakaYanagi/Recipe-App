import os
import pytest
from Home import fetch_data, move_page
import streamlit as st
from streamlit.testing.v1 import AppTest
import mongomock


@pytest.fixture
def mock_client():
    client = mongomock.MongoClient()
    db = client['recipe_app']
    collection = db['recipes']
    return client, collection

def test_fetch_data(mock_client):

    client, collection = mock_client

    collection.insert_one({'name': 'Sushi', 'cuisine': 'Asian', 'category': 'Fish', 'occasion': 'Healthy'})
    
    res = fetch_data(client, name = 'Sushi', cuisine = None, category = 'Fish', occasion = None)

    assert len(res) == 1
    assert res[0]['name'] == 'Sushi'

def test_move_page():
    st.session_state.selected_recipe = None
    move_page('abc123')

    assert st.session_state.selected_recipe == 'abc123'

def test_display_UI():
    at = AppTest.from_file('Home.py')
    at.run()

    assert at.form("recipe_finder_form").button("Find Recipes").exists()

