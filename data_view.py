import sqlite3
from sqlite3 import Error
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


def get_column(conn,col_name):
    cur = conn.cursor()
    cur.execute("SELECT " + col_name+ " FROM URL")
    col_values = cur.fetchall()
    col_values = [int(i[0]) for i in col_values]
    df = pd.DataFrame(col_values,columns=[col_name])
    return df

def create_connection(db):
    try:
        conn = sqlite3.connect(db)
        return conn
    except Error as e:
        print(e)

# URL TEXT,NAME TEXT,POSITION TEXT,COLLEGE TEXT,CB_INVITE TEXT,CB_HEIGHT TEXT,CB_WEIGHT TEXT,CB_FORTY TEXT,CB_TWENTY TEXT,CB_TEN TEXT,CB_REPS TEXT,CB_VERT TEXT,CB_BROAD TEXT,CB_SHUTTLE TEXT,CB_DRILL TEXT, PRO_INVITE TEXT, PRO_HEIGHT TEXT,PRO_WEIGHT TEXT,PRO_FORTY TEXT,PRO_TWENTY TEXT,PRO_TEN TEXT,PRO_REPS TEXT,PRO_VERT TEXT,PRO_BROAD TEXT,PRO_SHUTTLE TEXT,PRO_DRILL TEXT

def main():
    db = "/Users/davidta/Desktop/nfl_prospect/nfl_players.db"
    conn = create_connection(db)
    with conn:
        df = get_column(conn,"CB_WEIGHT")
if __name__ == '__main__':
    main()
