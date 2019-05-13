from flask import Flask, render_template, request
import mysql.connector
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf8')


def polaczenie():
    db_config = {
        'user': 'root',
        'password': '',
        'host': '172.31.43.137',
        'database': 'pythonflask'
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
            tytul = str(q[eq].get("volumeInfo").get("title"))
            autor = str(q[eq].get("volumeInfo").get("authors")[0])
            eq = eq + 1
            #add_autor = ("INSERT INTO autorzy (imie_nazwisko) VALUES (\"" + autor + "\")")
            #cursor.execute(add_autor)
            add_book = ("INSERT INTO ksiazki (tytul, autor) VALUES (\"" + tytul + "\", \"" + autor + "\")")
            print(add_book)
            cursor.execute(add_book)
        #query_table = ""
        print(server_query)
        #cursor.execute(query_table)
        cnx.commit()
        cursor.close()
        cnx.close()
    return render_template('google.html')


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
