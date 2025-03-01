import streamlit as st
import pymongo
from bson.objectid import ObjectId

# Font
font = 'Funnel Display'

def set_page_config():

    """Set page config."""

    st.set_page_config(
            page_title='Home',
            page_icon='📖',
            layout='wide"',
            menu_items={'Get Help': None, 'Report a bug': None,'About': None},
        )

set_page_config()

@st.cache_resource
def init_connection():

    """Initialise the MongoDB database connection"""
    
    mongo_uri = st.secrets['mongo']['uri']

    # try:
    #     client = pymongo.MongoClient(mongo_uri)
    #     return client
    # except Exception as e:
    #     return f"Failed to connect to DB. {type(e)} : {e}"
    client = pymongo.MongoClient(mongo_uri)
    return client

client = init_connection()

# client = pymongo.MongoClient(f"mongodb://saya:mongo2024@localhost:32788/")
# db = client.note_app
# collection = db["notes"]

def connect_to_db_collection(client):

    database_name = st.secrets['mongo']['database']
    collection_name = st.secrets['mongo']['collection']

    db = client[database_name]
    collection = db[collection_name]

    return collection


def fetch_data(name, cuisine, category, occasion):

    
    collection = connect_to_db_collection(client)

    # Fitering query
    query = {}
    if name:
        query['name'] = {'$regex': name, '$options' : 'i' }
    if cuisine:
        query['cuisine'] = cuisine
    if category:
        query['category'] = category
    if occasion:
        query['occasion'] = occasion

    # Fetch data once
    cursor = collection.find(query)
    return list(cursor) 


def move_page(recipe_id):
    st.session_state.selected_recipe = recipe_id





def create_filtering_input():
    """Create filtering input fields."""
    # Adjusted column ratios for better alignment
    col1, col2, col3, col4 = st.columns(4)

    with col1:
        name = st.text_input('🔍 Search by recipe')
    with col2:
        cuisine = st.selectbox(label = '🇬🇧 Search by cuisine', 
                               options = ('African', 'American', 'Asian', 'European', 'Indian', 'Middle Eastern'), 
                               index = None)
    with col3:
        category = st.selectbox(label = '🍚 Search by category', 
                              options = ('Bread', 'Rice', 'Pasta', 'Curry', 'Salad', 'Soup', 'Meat', 'Fish', 'Dessert', 'Others (source etc.)'),
                              index = None)
    with col4:
        occasion = st.selectbox(label = '🎂 Search by occasion', 
                                options = ['Quick & Easy','Spicy', 'Healthy', 'Party', 'Vegetarian'],
                                index = None)

    return name, cuisine, category, occasion

if "selected_recipe" not in st.session_state:
    st.session_state.selected_recipe = None

if st.session_state.selected_recipe is None:
    st.title('👨‍🍳 Home Cookbook 👩‍🍳')

    with st.form('recipe_finder_form'):
        name,cuisine, category, occasion = create_filtering_input()
        submitted = st.form_submit_button('Find Recipes')

        if submitted:
            with st.spinner('🧐 Searching for recipes...'):


                recipes = fetch_data(name, cuisine, category, occasion)

                if recipes:
                    for recipe in recipes:
                        with st.expander(icon = '🍽️', label = f"**{recipe.get('name')}**"):
                            st.markdown(f"**Cuisine :** {recipe.get('cuisine', 'N/A')}")
                            st.markdown(f"**Category :** {recipe.get('category', 'N/A')}")
                            st.markdown(f"**Occasion :** {recipe.get('occasion', 'N/A')}")
                            
                            if st.form_submit_button(label = 'Go to recipe', 
                                                     type = 'primary', 
                                                     on_click = move_page, 
                                                     args=(str(recipe['_id']),)):
                                pass
                else:
                    st.write('No recipe found. Try other filters.')
else:
    collection = connect_to_db_collection(client)
    
    # Fetch the recipe using its ObjectId
    recipe = collection.find_one({'_id': ObjectId(st.session_state.selected_recipe)})

    if recipe:
        st.title(f'🍽️ {recipe['name']}')
        with st.container(border = True):
            st.markdown(f"**Cuisine :** {recipe.get('cuisine', 'N/A')}")
            st.markdown(f"**Category :** {recipe.get('category', 'N/A')}")
            st.markdown(f"**Occasion :** {recipe.get('occasion', 'N/A')}")

        st.subheader("Steps")
        for i, step in enumerate(recipe.get('step', []), start=0):
            with st.container(border = True):
                st.write(f'S**Step {i + 1} :** {step}')

        if st.button(label = 'Back to Search',
                     type = 'primary'):
            st.session_state.selected_recipe = None

    else:
        st.error('Recipe not found!')
        if st.button(label = 'Back to Search',
                     type = 'primary'):
            st.session_state.selected_recipe = None