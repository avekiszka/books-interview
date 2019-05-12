import mysql.connector
db_config = {
    'user': '',
    'password': '',
    'host': '',
    'database': ''
}
cnx = mysql.connector.connect(**db_config)
cursor = cnx.cursor()
#user_imie = input("Podaj imie do dodania do bazy: ")
#user_nazwisko = input("Podaj nazwisko do dodania do bazy: ")
#user_plec = input("Podaj plec do dodania do bazy (mezczyzna/kobieta): ")
tytul = input("podaj tytul: ")
autor = input("podaj autora: ")

add_book = ("INSERT INTO ksiazki (tytul, autor) VALUES ('"+tytul+"', '"+autor+"')")
#print(add_user)
cursor.execute(add_book)
query_table = "SELECT * FROM ksiazki"
print(query_table)
cursor.execute(query_table)
for (id, tytul, autor) in cursor:
    print("{}, {}, {}".format(id, tytul, autor))
cnx.commit()
cursor.close()
cnx.close()