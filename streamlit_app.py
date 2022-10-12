import streamlit
import pandas
import requests
import snowflake.connector
from urllib.error import URLError

streamlit.title('My parents healthy diner')
streamlit.header('Breakfasr Menu')
streamlit.text('🥣 Idli')
streamlit.text('🥗 Dosa')
streamlit.text('🍞 puri')
streamlit.header('🍌🥭 Build Your Own Fruit Smoothie 🥝🍇')

my_fruit_list = pandas.read_csv("https://uni-lab-files.s3.us-west-2.amazonaws.com/dabw/fruit_macros.txt")
my_fruit_list = my_fruit_list.set_index('Fruit')
fruits_selected = streamlit.multiselect("Pick some fruits:", list(my_fruit_list.index),['Avocado','Strawberries'])
fruits_to_show = my_fruit_list.loc[fruits_selected]
streamlit.dataframe(fruits_to_show)

def getfruitvicedata(fruitname):
    fruityvice_response = requests.get("https://fruityvice.com/api/fruit/"+str(fruitname))
    fruityvice_normalized = pandas.json_normalize(fruityvice_response.json())
    return fruityvice_normalized

streamlit.header('Fruityvice Fruit Advice')
try:
  fruit_choice = streamlit.text_input('What fruit would you like information about?')
  if not fruit_choice:
    streamlit.error("Please select fruit to get information")
  else:
    back_from_function = getfruitvicedata(fruit_choice)
    streamlit.dataframe(back_from_function)

except Exception as e:
    streamlit.error()


#snowflake connection
streamlit.header("The fruit load list contains:")
def get_fruit_load_list():
    with my_cnx.cursor() as my_cur:
        my_cur.execute("SELECT * from fruit_load_list")
        return my_cur.fetchall()

#add button
if streamlit.button("Get fruit load list"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    my_data_rows = get_fruit_load_list()
    streamlit.dataframe(my_data_rows)

#Allow end user to add fruits
def insert_row_snowflake(new_fruit):
    with my_cnx.cursor() as my_cur:
        my_cur.execute("insert into fruit_load_list values('from streamlit');")
        return "Thanks for adding new fruit "+str(new_fruit)

add_my_fruit = streamlit.text_input('What fruit would you like to add?')
if streamlit.button("Add fruit to the list"):
    my_cnx = snowflake.connector.connect(**streamlit.secrets["snowflake"])
    back_from_func = insert_row_snowflake(add_my_fruit)
    streamlit.text(back_from_func)

# my_cur.execute("insert into fruit_load_list values('from streamlit');")
