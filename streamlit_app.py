# STREAMLIT
import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

# function def #
def get_fruityvice_data(this_fruit_choice): # use REQUESTS lib
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/" + fruit_choice)
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("select * from fruit_load_list")
        return my_cur.fetchall()
    
def insert_row_snowflake (new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values (new_fruit)")
        return "Thanks for adding " + new_fruit
      
        
# section 1
streamlit.title('My new Healthy diner')
streamlit.header('Breakfast Menu')
streamlit.text('🥣 Omega 3 & Blueberry Oatmeal')
streamlit.text('🥗 Kale, Spinach ¬ rocket Smoothie')
streamlit.text('🐔 Hard-Boiled Free-Range Egg')
streamlit.text('🥑🍞 Avocado Toast')

# section 2
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')
# use PANDAS lib 
my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
# put a pick list with some fruit preselected
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

# section 3
streamlit.header('Fruityvice Fruit Advice!')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select a Fruit to get information")
  else:
    back_from_function = get_fruityvice_data(fruit_choice)
    #streamlit.write('The user entered',fruit_choice)
    # streamlit.text(fruityvice_response.json())
    streamlit.dataframe(back_from_function)  
except URLError as e:
  streamlit.error()

# section 4
streamlit.header('View our Fruit List - Add your favorites!!')
# use SNOWFLAKE 
if streamlit.button('Get Fruit list'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    my_cnx-close()
    streamlit.dataframe(my_data_rows)  
    
# section 5
add_my_fruit = streamlit.text_input('What fruit would you like to add?' ,'jackfruit')
if streamlit.button('Add Fruit'):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_function = insert_row_snowflake(add_my_fruit)
    my_cnx-close()
    streamlit.text(back_from_function)
    
# don't run anything past here while we troubleshoot
streamlit.stop()



