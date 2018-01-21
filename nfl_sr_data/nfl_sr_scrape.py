

def attempt_connection(start,end):
    try:
        con = lite.connect('sr_players_database_' + start + '_' + end + '.db')
        return con
    except Error as e:
        print(e)

def main():
	con = attempt_connection(start,end)

if __name__ == "__main__":
    main()