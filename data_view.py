import sqlite3
from sqlite3 import Error
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set(style="ticks", color_codes=True)

### ----------------------------------------------------------------------------------------------------
### SPEED_COMP
### ----------------------------------------------------------------------------------------------------

def sort_by_conference(conn)
    SEC = ["Alabama","Florida","Georgia","Missouri","South Carolina","Tennessee","Vanderbilt","Alabama","Arkansas","Auburn","LSU","Mississippi","Mississippi State","Texas AM"]
    BIGTEN = ["Indiana","Maryland","Michigan","Michigan State","Ohio State","Penn State","Rutgers","Illinois","Iowa","Minnesota","Nebraska","Northwestern","Purdue","Wisconsin"]

def speed_comp(conn):
    sort_by_conference(conn)

### ----------------------------------------------------------------------------------------------------
### PAIRWISE_PLOT
### ----------------------------------------------------------------------------------------------------

def pairwise_plot(conn):
    with conn:
        df = [get_column(conn,"CB_WEIGHT"),get_column(conn,"CB_HEIGHT")]
        df = pd.concat(df, axis=1)
        g = sns.pairplot(df)
        plt.show()

def convert_values(column,col_name):
    if "HEIGHT" in col_name:
        column = [height_conversion(entry[0]) for entry in column]
    elif "WEIGHT" in col_name:
        column = [float(i[0]) for i in column]
    return column

def height_conversion(height_entry):
    ### Need to check why there is a 5.72
    if "." in height_entry:
        return float(height_entry)
    elif len(height_entry) == 4:
        return float(height_entry[0])*12 + float(height_entry[1:3]) + float(height_entry[3])/10
    else:
        return float(height_entry[0])*12 + float(height_entry[1:3])

### ----------------------------------------------------------------------------------------------------
### GENERAL FUNCTIONS
### ----------------------------------------------------------------------------------------------------

def get_column(conn,col_name):
    cur = conn.cursor()
    cur.execute("SELECT " + col_name+ " FROM URL")
    col_values = cur.fetchall()
    col_values = convert_values(col_values,col_name)
    df = pd.DataFrame(col_values,columns=[col_name])
    return df

### ----------------------------------------------------------------------------------------------------
### CREATE_CONNECTION
### ----------------------------------------------------------------------------------------------------

def create_connection(db):
    try:
        conn = sqlite3.connect(db)
        return conn
    except Error as e:
        print(e)

# URL TEXT,NAME TEXT,POSITION TEXT,COLLEGE TEXT,CB_INVITE TEXT,CB_HEIGHT TEXT,CB_WEIGHT TEXT,CB_FORTY TEXT,CB_TWENTY TEXT,CB_TEN TEXT,CB_REPS TEXT,CB_VERT TEXT,CB_BROAD TEXT,CB_SHUTTLE TEXT,CB_DRILL TEXT, PRO_INVITE TEXT, PRO_HEIGHT TEXT,PRO_WEIGHT TEXT,PRO_FORTY TEXT,PRO_TWENTY TEXT,PRO_TEN TEXT,PRO_REPS TEXT,PRO_VERT TEXT,PRO_BROAD TEXT,PRO_SHUTTLE TEXT,PRO_DRILL TEXT

def main():
    db = "/Users/davidta/Desktop/nfl_prospect/nds_data/nfl_players.db"
    conn = create_connection(db)
    pairwise_plot(conn)
    speed_comp(conn)

if __name__ == '__main__':
    main()
