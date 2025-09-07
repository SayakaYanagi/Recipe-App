import os
import pytest
from recipe_book.Home import fetch_data, move_page
import streamlit as st
from streamlit.testing.v1 import AppTest
from unittest.mock import patch
import mongomock

@pytest.fixture
def mock_client():
    client = mongomock.MongoClient()
    return client

@pytest.fixture(autouse=True)
def mock_streamlit_secrets(monkeypatch):
    """
    Patch streamlit.secrets before any test runs so modules
    that import it at top-level won't fail.
    """
    monkeypatch.setattr(
        'streamlit.secrets',
        {'mongo': {'uri': 'mongodb://localhost:27017'}}
    )

@pytest.fixture
def mock_client():
    client = mongomock.MongoClient()
    db = client['test_db']
    collection = db['test_collection']
    return client, collection

@patch('streamlit.secrets', new={'mongo': {'uri': 'mongodb://localhost:27017'}})
def test_fetch_data(mock_client):

    # from Home import fetch_data

    client, collection = mock_client

    collection.insert_one({'name': 'Sushi', 'cuisine': 'Asian', 'category': 'Fish', 'occasion': 'Healthy'})
    
    res = fetch_data(client, 
                     name = 'Sushi', 
                     cuisine = None, 
                     category = 'Fish', 
                     occasion = None
                    )

    assert len(res) == 1
    assert res[0]['name'] == 'Sushi'

def test_move_page():
    
    # from Home import move_page
    st.session_state.selected_recipe = None
    move_page('abc123')

    assert st.session_state.selected_recipe == 'abc123'

def test_display_UI():
    at = AppTest.from_file('Home.py')
    at.run()
    
    button_key = "FormSubmitter:recipe_finder_form-Find Recipes"

    # Verify button is present
    assert at.button(button_key) is not None
    assert at.button(button_key).label == "Find Recipes"


