import streamlit as st
import pymongo
from bson.objectid import ObjectId
import utils
import time

# Set the page config
utils.set_page_config('Home')

def fetch_data(client, name, cuisine, category, occasion):

    # Fetch all data
    collection = utils.connect_to_db_collection(client)

    # Fitering query
    query = {}
    if name:
        query['name'] = {'$regex': name, '$options' : 'i' } # Case insensitive
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
                                options = ['Quick & Easy','Spicy', 'Healthy', 'Party', 'Vegetarian', 'Keto'],
                                index = None)

    return name, cuisine, category, occasion

def delete_recipe(client, recipe_id):
    """Delete specified recipe from MongoDB."""

    collection = utils.connect_to_db_collection(client)
    try:
        collection.delete_one({"_id": ObjectId(recipe_id)})
        st.success('Removed the recipe successfully. Back to Home page...')
        time.sleep(2)
        st.session_state.selected_recipe = None
        st.rerun()
        
        
    except Exception as e:
        st.error(f"Error deleting recipe: {e}")


@st.dialog("⚠️ Are you sure?")
def deletion_pop_up(client, recipe_id):

    """Pop-up window to confirm if user wants to delete the recipe."""

    st.write('Do you really want to delete this recipe? This process cannot be undone.')
    if st.button(label = 'Delete', type = 'primary', width = 'stretch'):
        delete_recipe(client, recipe_id)




def main():

    # Connect to MongoDB
    client = utils.init_connection()

    if "selected_recipe" not in st.session_state:
        st.session_state.selected_recipe = None

    if st.session_state.selected_recipe is None:

        # Page title
        st.title('👨‍🍳 Home Cookbook 👩‍🍳')

        # Filter search
        with st.form('recipe_finder_form'):
            name, cuisine, category, occasion = create_filtering_input()
            submitted = st.form_submit_button('Find Recipes')

        if submitted:
            with st.spinner('🧐 Searching for recipes...'):

                # Collect recipe data with filtering
                recipes = fetch_data(client, name, cuisine, category, occasion)

                if recipes:
                    # Shows the search result
                    for recipe in recipes:
                        with st.expander(icon = '🍽️', label = f"**{recipe.get('name')}**"):
                            st.markdown(f"**Cuisine :** {recipe.get('cuisine', 'N/A')}")
                            st.markdown(f"**Category :** {recipe.get('category', 'N/A')}")
                            st.markdown(f"**Occasion :** {recipe.get('occasion', 'N/A')}")
                            
                            # If button pressed, move to recipe detail page
                            if st.button(label = 'Go to recipe', 
                                        type = 'primary', 
                                        on_click = move_page, 
                                        args=(str(recipe['_id']),),
                                        key=f"go_to_recipe_{recipe['_id']}"):
                                        pass
                            
                else:
                    st.info('No recipes found. Try different filters.')
    else:
        collection = utils.connect_to_db_collection(client)
        
        # Fetch the recipe using its ObjectId
        recipe = collection.find_one({'_id': ObjectId(st.session_state.selected_recipe)})

        if recipe:
            st.title(f'🍽️ {recipe['name']}')

            # Display attributes
            with st.container(border = True):
                st.markdown(f"**Cuisine :** {recipe.get('cuisine', 'N/A')}")
                st.markdown(f"**Category :** {recipe.get('category', 'N/A')}")
                st.markdown(f"**Occasion :** {recipe.get('occasion', 'N/A')}")

            # Display ingredients (Render HTML expressions)
            st.subheader('Ingredients')
            with st.container(border=True):
                st.markdown(recipe.get('ingredients', 'N/A').replace("\n", "<br>"), unsafe_allow_html=True)

            # Display steps (Render HTML expressions)
            st.subheader('Steps')
            for i, step in enumerate(recipe.get('step', []), start = 1):
                with st.container(border = True):
                    st.markdown(f'**Step {i} :** {step}'.replace("\n", "<br>"), unsafe_allow_html=True)

            col1, spacer, col2 = st.columns([1, 6, 1])
            with col1:
                if st.button(label = 'Back to Search', type = 'primary'):
                    st.session_state.selected_recipe = None
            with col2:
                if st.button(label = 'Delete this recipe', 
                             type = 'secondary', 
                             key = 'deletion_pop_up'):
                    deletion_pop_up(client, str(recipe['_id']))

        else:
            # If recipe is not found, go back to search 
            st.error('Recipe not found!')
            if st.button(label = 'Back to Search',
                        type = 'primary'):
                st.session_state.selected_recipe = None


if __name__ == '__main__':
    main()