import requests
from bs4 import BeautifulSoup
import sqlite3


def create_table(cursor):
    cursor.execute("CREATE TABLE IF NOT EXISTS Halo_Master_Chief_Collection "
                   "(id INTEGER PRIMARY KEY, Date TEXT, Price TEXT, Gain TEXT, Discount TEXT)")


def collect_data():
    response = requests.get(f"https://steampricehistory.com/app/594570")
    game_page = response.text

    soup = BeautifulSoup(game_page, "html.parser")

    table_body = soup.find_all("tbody", limit=2)
    table_rows = table_body[1].find_all("tr")
    return table_rows


def insert_row_data(cursor, table_rows):
    count = 1
    for item in table_rows[1::1]:
        all_entries = item.find_all("td")
        id_var = count
        date_var = all_entries[0].text
        price_var = all_entries[1].text
        gain_var = all_entries[2].text
        disc_var = all_entries[3].text
        try:
            cursor.execute("INSERT INTO Halo_Master_Chief_Collection (id, Date, Price, Gain, Discount) values (?, ?, ?, ?, ?)",
                           (id_var, date_var, price_var, gain_var, disc_var))
        except:
            pass
            count += 1


def get_high_price():
    price_list = []
    for item in rows:
        price_list.append(float(item[2].strip("$")))
    high_price = 0
    for item in price_list:
        if item > high_price:
            high_price = item
    return high_price


def get_high_discount():
    price_list = []
    for item in rows:
        if item[4] != "-":
            price_list.append(int(item[4].strip("-").strip("%")))
        else:
            price_list.append(0)
    high_disc = 0
    for item in price_list:
        if item > high_disc:
            high_disc = item
    return high_disc


def discount_price(price, discount):
    discounted_price = price*(discount/100)
    return round(discounted_price, 2)


connection = sqlite3.connect("PriceHistory.db")
cursor = connection.cursor()
# insert_row_data(cursor, collect_data())
# connection.commit()

db_entries = connection.execute("select * from Halo_Master_Chief_Collection")
rows = db_entries.fetchall()
connection.close()

high_price = get_high_price()
discount = get_high_discount()

print(f"The latest Entry is: {rows[0][1]} | {rows[0][2]} | {rows[0][3]} | {rows[0][4]} "
      f"\nHighest Price is: ${high_price} "
      f"\nHighest Discount: {discount}% "
      f"\nDiscount Price: ${discount_price(high_price, discount)}")

