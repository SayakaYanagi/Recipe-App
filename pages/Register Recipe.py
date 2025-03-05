import streamlit as st
import pymongo
from datetime import date
import utils




def add_step():
    st.session_state.steps.append('')

def load_data_db(client, name, cuisine, category, occasion, ingredients, steps):
    
    """Load the input (recipe data) into MongoDB."""

    # Connect to MongoDB collection
    collection = utils.connect_to_db_collection(client)
    
    # Get today's date
    today = date.today().strftime('%Y-%m-%d')

    # Dictionary of inputs
    document = { 'name' : name,
                 'cuisine' : cuisine,
                 'category' : category,
                 'occasion' : occasion,
                 'last_update' : today,
                 'ingredients' : ingredients,
                 'step' : steps
                 }
    
    # Insert date into MongoDB
    result = collection.insert_one(document)
    return result.acknowledged


def main():

    # Set the page config
    utils.set_page_config('Register Recipe')
    # Page title
    st.title('✏️ Register your recipe!')

    # Connect to Mongo DB
    client = utils.init_connection()

    if 'steps' not in st.session_state:
        st.session_state.steps = ['']

    # Filter search
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
                        
    # Ingredients section
    with st.container(border = True):
        ingredients = st.text_area(label = 'Ingredients', height = 100, placeholder = '・1 Onion \n・1Tbs Sugar')

    # Steps section
    with st.container(border = True):

        # Create two columns for the input box and delete button
        col1, col2 = st.columns(spec = [0.9, 0.1])

        # The first row (step 1) is always displayed, and it doesn't have delete button
        with col1 :
            st.session_state.steps[0] = st.text_area(label = f'Step 1', 
                                                    value = st.session_state.steps[0], 
                                                    key = f'step_0',
                                                    height = 70)

        # The second row onwards are created when the button is pressed
        for i in range(1, len(st.session_state.steps)):

            col1, col2 = st.columns(spec = [0.9, 0.1], 
                                    gap = 'small',
                                    vertical_alignment = 'bottom')
            with col1: # Input box
                st.session_state.steps[i] = st.text_area(label = f'Step {i+1}', 
                                                        value = st.session_state.steps[i], 
                                                        key = f'step_{i}',
                                                        height = 70)
            with col2: #Delete button
                if i == len(st.session_state.steps) - 1:
                    if st.button(label = 'Delete', key=f'delete_step_{i}', use_container_width=True):
                        st.session_state.steps.pop()  # Remove the last step
                        st.rerun() 

        # button to add a step
        st.button(label = ':material/add:', on_click = add_step)

        # button to load the input data to MongoDB
        if st.button(label = 'Register recipe', type = 'primary'):
            if not name.strip():
                st.error('⚠️ Recipe name is required!')
            if not ingredients.strip():
                st.error('⚠️ Ingredients are required!')
            else:
                success = load_data_db(client, name, cuisine, category, occasion, ingredients, st.session_state.steps)
                if success:
                    st.success('Recipe added!')
                    # st.balloons()
                    st.snow()
                    
                    
                else:
                    st.error('⚠️ Failed to add recipe.')
             


if __name__ == '__main__':
    main()
             

