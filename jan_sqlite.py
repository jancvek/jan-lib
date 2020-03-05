import sqlite3
from sqlite3 import Error
  
def create_connection(db_file):
    conn = None
    
    try:
        conn = sqlite3.connect(db_file)
        print('Successfully connect to db')
    except Error as e:
        print(e)

    return conn

def run_query(conn, sql):
    try:
        cur = conn.cursor()
        cur.execute(sql)
        rows = cur.fetchall()
        print('Successfully run query')
        return rows

    except Error as e:
        print(e)
        return ''

# params = "created_by_service,library_user,status,days_to_expire,text"
# values = ('1','MASA',str(cobissMasa.status.name),cobissMasa.minDays,cobissMasa.error)
def insert_data(conn, table, params, values):
    questStr = "?"
    for x in values[1:]:    #[1:] štarta pri 2 elementu in gre do konca
        questStr += ',?'
    
    try:
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


def get_data_all(conn, table):
    cur = conn.cursor()
    cur.execute("SELECT * FROM "+table)
 
    rows = cur.fetchall()
 
    return rows
    # for row in rows:
    #     print(row)
    #     print(row[1])

# todo: ne spada ravno v ta lib
def update_data_daily_situation(conn, table, id, values):
    print("test111")
    try:
        sql =   ''' UPDATE '''+table+''' 
                SET is_complete = 1, filling = ?, sex = ?, a_init = ?, red_day = ?, additional = ? 
                WHERE id='''+ id

        cur = conn.cursor()
        cur.execute(sql, values)
        print('Successfully insert data')
        print('SQL: '+sql)
        print('values: '+str(values))
    except Error as e:
        print(e)

    if cur:
        return cur.lastrowid
    else:
        return ''

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