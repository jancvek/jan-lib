import sqlite3
from sqlite3 import Error
  
def create_connection(db_file):
    conn = None
    cur = None
    try:
        conn = sqlite3.connect(db_file)
        print('Successfully connect to db')
    except Error as e:
        print(e)

        sql = ''' INSERT INTO '''+table+''' ('''+params+''')
                VALUES('''+questStr+''') '''
        cur = conn.cursor()
        cur.execute(sql, values)
        print('Successfully insert data')
    except Error as e:
        print(e)

    if cur:
        return cur.lastrowid
    else:
        return ''


def get_data_all(conn):
    cur = conn.cursor()
    cur.execute("SELECT * FROM test_table")
 
    rows = cur.fetchall()
 
    return rows
    # for row in rows:
    #     print(row)
    #     print(row[1])

# tole se zazene ko je to main program ni klican iz druge kode
if __name__ == '__main__':
    conn = create_connection(r"data.db")
    if conn:
        print('dela')
        with conn:
            data = ('Tole je test2',)   #pazi na vejico mora biti tudi ce je samo en vnos ker to pomeni da je truple
            # insert_data(conn, data)
            get_data_all(conn)
    else:
        print('ne dela')