import pandas as pd
import sqlite3

def connect(table):
    conn = sqlite3.connect("chroma.db")
    cursor = conn.cursor()
    users = cursor.execute(f"SELECT * FROM {table}")
    result = cursor.fetchall()
    cursor.close()
    return result

def check_user(email):
    result = connect(table = 'user')
    df = pd.DataFrame(result,columns =['ID','Email','Password'])
    
    mail = [x for x in df['Email']]
    if email in mail:
       actual_pass = df.loc[df['Email']==email,'Password'].values[0]
       return actual_pass
    else:
        return 0

def find_accountID(email):
    result = connect(table = 'account')
    df = pd.DataFrame(result,columns = ['ID','Email','Password'])
    mail = [x for x in df['Email']]
    account_ID = df.loc[df['Email']==email , 'ID' ].values[0]
    return account_ID
