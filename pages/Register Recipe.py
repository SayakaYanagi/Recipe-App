import streamlit as st
import pymongo
from datetime import date

def set_page_config():

    """Set page config."""

    st.set_page_config(
            page_title='Register Recipe',
            page_icon='📖',
            layout='wide',
            menu_items={'Get Help': None, 'Report a bug': None, 'About': None},
        )
set_page_config()


client = pymongo.MongoClient(f'mongodb://saya:mongo2024@localhost:32788/')
# db = client.note_app
# collection = db['notes']

def connect_to_db_collection(client):

    database_name = st.secrets['mongo']['database']
    collection_name = st.secrets['mongo']['collection']

    db = client[database_name]
    collection = db[collection_name]

    return collection

st.title('✏️ Register your recipe!')

if 'steps' not in st.session_state:
    st.session_state.steps = ['']

def add_step():
    st.session_state.steps.append('')

def load_data_db(name, cuisine, category, occasion, steps):

    # Connect to MongoDB collection
    collection = connect_to_db_collection(client)
    
    # Get today's date
    today = date.today().strftime('%Y-%m-%d')

    document = { 'name' : name,
                 'cuisine' : cuisine,
                 'category' : category,
                 'occasion' : occasion,
                 'last_update' : today,
                 'step' : steps
                 }
    
    #Insert date into MongoDB
    result = collection.insert_one(document)
    return result.acknowledged

with st.container(border = True):
                    name = st.text_input(label = 'Input recipe name', max_chars = 50)
                    cuisine = st.selectbox(label = 'Input cuisine', 
                               options = ('African', 'American', 'Asian', 'European', 'Indian', 'Middle Eastern'), 
                               index = None)
                    category = st.selectbox(label = 'Input category', 
                              options = ('Bread', 'Rice', 'Pasta', 'Curry', 'Salad', 'Soup', 'Meat', 'Fish', 'Dessert', 'Others (source etc.)'),
                              index = None)
                    occasion = st.selectbox(label = 'Input occasion', 
                                options = ['Quick & Easy','Spicy', 'Healthy','Party', 'Vegetarian'],
                                index = None)

with st.container(border = True):

    st.session_state.steps[0] = st.text_input(label = f'Step 1', value = st.session_state.steps[0], key = f'step_0')

    for i in range(1, len(st.session_state.steps)):
        st.session_state.steps[i] = st.text_input(label = f'Step {i+1}', value = st.session_state.steps[i], key = f'step_{i}')

    st.button(label = 'Add step', type = 'primary', on_click = add_step)
    if st.button(label = 'Register recipe', type = 'primary', on_click = load_data_db, args = (name, cuisine, category, occasion, st.session_state.steps)):
        st.markdown('Recipe added!')

