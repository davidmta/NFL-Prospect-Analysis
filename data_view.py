import sqlite3
from sqlite3 import Error
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns; sns.set(style="ticks", color_codes=True)

PRO_SPEED_CATEGORY_NUM = 13

### ----------------------------------------------------------------------------------------------------
### SPEED_COMP
### ----------------------------------------------------------------------------------------------------

def get_conf_stats(conference, category, conference_dict):
    stats = []
    for college in conference_dict[conference]:
        for player_stats in conference_dict[conference][college]:
            if player_stats[category] != "NULL":
                stats.append(float(player_stats[category]))
    return stats

def plot_speedgraph(SECspeed_df,BIG10speed_df,ACCspeed_df,PAC12speed_df,BIG12speed_df):
    speed_df = [SECspeed_df,BIG10speed_df,ACCspeed_df,PAC12speed_df,BIG12speed_df]
    speed_df = pd.concat(speed_df, axis=1)
    speed_df.plot.box()
    plt.show()

def speed_comp(conn):
    conference_dict = sort_by_conference(conn)
    SECspeed_df = pd.DataFrame(get_conf_stats("SEC",PRO_SPEED_CATEGORY_NUM,conference_dict),columns=["SEC"])
    BIG10speed_df = pd.DataFrame(get_conf_stats("BIG10",PRO_SPEED_CATEGORY_NUM,conference_dict),columns=["BIG10"])
    ACCspeed_df = pd.DataFrame(get_conf_stats("ACC",PRO_SPEED_CATEGORY_NUM,conference_dict),columns=["ACC"])
    PAC12speed_df = pd.DataFrame(get_conf_stats("PAC12",PRO_SPEED_CATEGORY_NUM,conference_dict),columns=["PAC12"])
    BIG12speed_df = pd.DataFrame(get_conf_stats("BIG12",PRO_SPEED_CATEGORY_NUM,conference_dict),columns=["BIG12"])
    plot_speedgraph(SECspeed_df,BIG10speed_df,ACCspeed_df,PAC12speed_df,BIG12speed_df)



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

def sort_conf_players(conn,conference):
    dict = {}
    cur = conn.cursor()
    for college in conference:
        cur.execute("SELECT * FROM URL WHERE COLLEGE = ' " + college + "'")
        dict[college] = cur.fetchall()
    return dict

def sort_by_conference(conn):
    SEC = ["Alabama","Florida","Georgia","Missouri","South Carolina","Tennessee","Vanderbilt","Alabama","Arkansas","Auburn","LSU","Mississippi","Mississippi State","Texas AM"]
    BIG10 = ["Indiana","Maryland","Michigan","Michigan State","Ohio State","Penn State","Rutgers","Illinois","Iowa","Minnesota","Nebraska","Northwestern","Purdue","Wisconsin"]
    ACC = ["Boston College","Clemson","Florida State","Louisville","North Carolina State","Syracuse","Wake Forest","Duke","Georgia Tech","Miami","North Carolina","Pittsburgh","Virginia","Virginia Tech"]
    PAC12 = ["Arizona","Arizona State","California","UCLA","Colorado","Oregon","Oregon State","Southern California","Utah","Washington","Washington State"]
    BIG12 = ["Baylor","Iowa State","Kansas","Kansas State","Oklahoma","Oklahoma State","Texas Christian","Texas","Texas Tech","West Virginia"]
    
    conference_dict = {}
    conference_dict["SEC"] = sort_conf_players(conn,SEC)
    conference_dict["BIG10"] = sort_conf_players(conn,BIG10)
    conference_dict["ACC"] = sort_conf_players(conn,ACC)
    conference_dict["PAC12"] = sort_conf_players(conn,PAC12)
    conference_dict["BIG12"] = sort_conf_players(conn,BIG12)
    
    return conference_dict

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

def main():
    db = "/Users/davidta/Desktop/nfl_prospect/nds_data/nfl_players.db"
    conn = create_connection(db)
    #pairwise_plot(conn)
    speed_comp(conn)

if __name__ == '__main__':
    main()
