import folium
import pandas as pd
import sqlite3


def execute_read_query(connection, query):
    cursor = connection.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"The error '{e}' occurred")


conn = sqlite3.connect('sqlite.db')

michelin1 = pd.read_csv('one-star-michelin-restaurants.csv')
michelin2 = pd.read_csv('two-stars-michelin-restaurants.csv')
michelin3 = pd.read_csv('three-stars-michelin-restaurants.csv')

michelin1['stars'] = 1
michelin2['stars'] = 2
michelin3['stars'] = 3

michelin = pd.concat([michelin1, michelin2, michelin3])
michelin.reset_index(drop=True, inplace=True)
m = folium.Map(location=[0, 0], zoom_start=3)

for _, r in michelin.iterrows():
    folium.Marker(
        [r['latitude'], r['longitude']], tooltip=r['name']
    ).add_to(m)

m.save('index.html')

michelin.to_excel('michelin.xlsx')

# michelin.to_sql(name='michelin', con=conn)

select_all = "SELECT * FROM michelin WHERE stars = 3"
data = execute_read_query(conn, select_all)

for r in data:
    print(r)
