import requests
import mysql.connector

db_config = {
    'user': '',
    'password': '',
    'host': '',
    'database': ''
}
cnx = mysql.connector.connect(**db_config)
cursor = cnx.cursor()
user_query = input("slowo kluczowe: ")
server_query = "https://www.googleapis.com/books/v1/volumes?q="+user_query
print(server_query)
r = requests.get(server_query)
slownik = r.json()
q = slownik.get("items")
count_items = len(q)
eq = 0
for eq in range(count_items):
    tytul = str(q[eq].get("volumeInfo").get("title"))
    autor = q[eq].get("volumeInfo").get("authors")[0]
    add_autor = ("INSERT INTO autorzy (imie_nazwisko) VALUES (\""+autor+"\")")
    cursor.execute(add_autor)
    add_book = ("INSERT INTO ksiazki (tytul, autor) VALUES (\""+tytul+"\", \""+autor+"\")")
    print(add_book)
    cursor.execute(add_book)
    eq = eq + 1
cnx.commit()
cursor.close()
cnx.close()
