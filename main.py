import folium
import pandas as pd
import sqlite3
import matplotlib.pyplot as plt


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

color_dict = {1: 'green', 2: 'blue', 3: 'red'}

for _, r in michelin.iterrows():
    folium.Marker(
        [r['latitude'], r['longitude']],
        tooltip=r['name'],
        icon=folium.Icon(color=color_dict[r['stars']])
    ).add_to(m)

m.save('index.html')

michelin.to_excel('michelin.xlsx')

# michelin.to_sql(name='michelin', con=conn)

# select_all = "SELECT * FROM michelin WHERE stars = 3"
# data = execute_read_query(conn, select_all)

# for r in data:
#     print(r)

# print(michelin['year'].value_counts().sort_index())
# print(michelin['region'].value_counts())
# print(michelin['cuisine'].value_counts())
# print(michelin['price'].value_counts().sort_index())

michelin['price'].dropna().apply(lambda x: '\$'*len(str(x))).value_counts().sort_index().plot(kind='bar')
plt.xticks(rotation='horizontal')
plt.title('Price distribution')
plt.xlabel('Price')
plt.ylabel('Restaurant count')
plt.savefig('prices.png')
plt.show()
