# Import python packages
import streamlit as st
from snowflake.snowpark.context import get_active_session
from snowflake.snowpark.functions import col

# Write directly to the app
st.title("Customize Your Smoothie :cup_with_straw:")
st.write(
    """Choose the fruits you want in your custom Smoothie!
    """
)

# Remove the SelectBox
# option = st.selectbox(
#     "What is your favorite fruit?",
#     ("Banana", "Strawberries", "Peaches"))

# st.write("Your favorite fruit is:", option)

# Add a Name Box for Smoothie Orders
name_on_order = st.text_input("Name on Smoothie:")
st.write("The name on your Smoothie will be:", name_on_order)

# Display the Fruit Options List in Your Streamlit in Snowflake (SiS) App. 
# If the line session = get_active_session() appears in your code two times, delete one of the lines.
session = get_active_session()
# Add the New SEARCH_ON Column to the Dataframe that feeds the Multiselect
my_dataframe = session.table("smoothies.public.fruit_options").select(col('FRUIT_NAME'))
# st.dataframe(data=my_dataframe, use_container_width=True)
# st.stop()

# # Add a Multiselect
ingredients_list = st.multiselect(
    'Choose up to 5 ingredients:',
    my_dataframe,
    max_selections = 5
)

# Our ingredients variable is an object or data type called a LIST. So it's a list in the traditional sense of the word, but it is also a datatype or object called a LIST. A LIST is different than a DATAFRAME which is also different from a STRING!
if ingredients_list:
    # st.write(ingredients_list)
    # st.text(ingredients_list)
    
    # Create the INGREDIENTS_STRING Variable
    ingredients_string = ''
    
    # Add the FOR Block
    for fruit_chosen in ingredients_list:
        ingredients_string += fruit_chosen + ' '
        
    # Output the String 
    # st.write(ingredients_string)

    # Build a SQL Insert Statement & Test It
    my_insert_stmt = """ insert into smoothies.public.orders(ingredients, name_on_order)
            values ('""" + ingredients_string + """', '"""+ name_on_order +"""')"""
    st.write(my_insert_stmt)
    # for troubleshooting
    # st.stop()

    # Add a Submit Button
    time_to_insert = st.button('Submit Order')

    if time_to_insert:
        session.sql(my_insert_stmt).collect()
        st.success('Your Smoothie is ordered, '+name_on_order+'!', icon="✅")

