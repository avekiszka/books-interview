from flask import Flask, render_template, request
import mysql.connector
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def polaczenie():
    db_config = {
        'user': '',
        'password': '',
        'host': '',
        'database': ''
    }
    cnx = mysql.connector.connect(**db_config)
    cursor = cnx.cursor()
    return cursor, cnx


app = Flask(__name__)


@app.route("/")
def main():
    cursor, cnx = polaczenie()
    query_table = "SELECT * FROM ksiazki"
    print(query_table)
    cursor.execute(query_table)
    data = cursor.fetchall()
    cursor.close()
    cnx.close()
    return render_template('index.html', data=data)


@app.route("/google", methods=['GET', 'POST'])
def google():
    if request.method == 'POST':
        slowo_kluczowe = request.form['skluczowe']
        cursor, cnx = polaczenie()
        server_query = "https://www.googleapis.com/books/v1/volumes?q=" + slowo_kluczowe
        r = requests.get(server_query)
        slownik = r.json()
        q = slownik.get("items")
        count_items = len(q)
        eq = 0
        for eq in range(count_items):
            tytul = str(q[eq].get("volumeInfo").get("title", "None"))
            autor = str(q[eq].get("volumeInfo").get("authors", "None")[0])
            kategoria = str(q[eq].get("volumeInfo").get("categories", "None")[0])
            opis = str(q[eq].get("volumeInfo").get("description", "None"))
            eq = eq + 1
            add_book = "INSERT INTO ksiazki (tytul, autor, kategoria, opis) VALUES (%s,%s,%s,%s)"
            print(add_book)
            cursor.execute(add_book, (tytul, autor, kategoria, opis))
        print(server_query)
        cnx.commit()
        query_table = "SELECT * FROM ksiazki"
        cursor.execute(query_table)
        data = cursor.fetchall()
        cursor.close()
        cnx.close()
    else:
        data = "dupa"
    return render_template('google.html', data=data)


@app.route("/formatka", methods=['GET', 'POST'])
def formatka():
    if request.method == 'POST':
        tytul_ksiazki = request.form['tytul']
        imie_autora = request.form['autor']
        cursor, cnx = polaczenie()
        query_table = "INSERT INTO ksiazki(tytul,autor) VALUES(%s,%s)"
        print(query_table)
        cursor.execute(query_table, (tytul_ksiazki, imie_autora))
        cnx.commit()
        cursor.close()
        cnx.close()

    return render_template('formatka.html')


if __name__ == "__main__":
    app.run(host='172.31.43.137', port=80)
