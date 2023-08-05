import sqlite3
import pandas as pd

def create_table():
    with sqlite3.connect("data.db") as conn:
        c = conn.cursor()
        c.execute('CREATE TABLE IF NOT EXISTS foodtable(food TEXT, count INTEGER, exp_date DATE)')

def add_data(food, count, exp_date):
    with sqlite3.connect("data.db") as conn:
        c = conn.cursor()
        c.execute('INSERT INTO foodtable(food, count, exp_date) VALUES (?,?,?)', (food, count, exp_date))

def view_data():
    with sqlite3.connect("data.db") as conn:
        c = conn.cursor()
        c.execute('SELECT * FROM foodtable')
        data = c.fetchall()
        df = pd.DataFrame(data, columns=['Food', 'Count', 'Expiration Date'])
        return df
    
def edit_data(record_number, new_food, new_count, new_exp_date):
    with sqlite3.connect("data.db") as conn:
        c = conn.cursor()
        c.execute('UPDATE foodtable SET food=?, count=?, exp_date=? WHERE rowid=?',
                  (new_food, new_count, new_exp_date, record_number))
        conn.commit()

def del_data(record_number):
    with sqlite3.connect("data.db") as conn:
        c = conn.cursor()
        c.execute('DELETE FROM foodtable WHERE rowid=?', (record_number,))
        conn.commit()
    # Resets the index after deletion
    with sqlite3.connect("data.db") as conn:
        c = conn.cursor()
        c.execute("VACUUM")
        conn.commit()
    return True