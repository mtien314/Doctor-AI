import mysql.connector
import pandas as pd
import sqlite3
import sqlite3


def connect_sql():
    conn = sqlite3.connect("chroma.db")
    return conn

def update_user(passw):

    conn = connect_sql()
    cursor = conn.cursor()
    sql = "UPDATE user SET Password=  ? WHERE Password = '0';"
    value = (passw,)
    cursor.execute(sql,value)
    conn.commit()
    cursor.close()

def update_user2(ID,use):
    conn = connect_sql()
    cursor = conn.cursor()
    cursor.execute('UPDATE user SET use = ? WHERE ID = ?', (use,ID))
    conn.commit()
    cursor.close()


def update_user_record(user_id,user_email):
    conn = connect_sql()
    cursor = conn.cursor()
    users = cursor.execute("SELECT * FROM user")
    result = cursor.fetchall()
    df = pd.DataFrame(result,columns =['ID','Email','Password','Use'])

    mail = [str(x) for x in df['Email']]
    password = 0
    use = 1
    if user_email not in mail:
        cursor.execute('INSERT INTO user(ID, Email,Password,Use) VALUES (?,?,?,?);',
                   (user_id,user_email,password,use))
        conn.commit()
    
    cursor.close()

def update_account(ID, Name, Age, Email, Phone):

    conn = connect_sql()
    cursor = conn.cursor()
    account = cursor.execute("SELECT * FROM account")
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns = ['ID','Name','Age','Email','Phone'])

    mail = [str(x) for x in df['Email']]
    if Email not in mail:
        cursor.execute('INSERT INTO account(ID, Name, Age, Email, Phone) VALUES (?, ?, ?, ?, ?);',
                       (ID, Name, Age, Email, Phone))
        conn.commit()
    cursor.close()

def update_appointment(PatientID,DoctorID):
    conn = connect_sql()
    cursor = conn.cursor()
    data = cursor.execute("SELECT * FROM appoiment")
    result = cursor.fetchall()
    df = pd.DataFrame(result, columns = ['ID','DoctorID','PatientID','PatientID','Clinic','Time','Description'])


def update_historylogs(ID,Email):
    conn = connect_sql()
    cursor = conn.cursor()
    cursor.execute('INSERT INTO history_logs(ID,Email) VALUES (? ,?);',
                   (ID,Email))
    conn.commit()
    cursor.close()


def update_appoinment2(PatientID,DATE):
    conn = connect_sql()
    cursor = conn.cursor()
    cursor.execute('UPDATE appointment SET DATE = ? WHERE PatientID = ?', (DATE,PatientID))
    conn.commit()
    cursor.close()
   
def cancel_appointment(PatientID, DATE):
    conn = connect_sql()
    cursor = conn.cursor()
    cursor.execute('DELETE FROM appointment WHERE DATE = ? AND PatientID = ?', (DATE,PatientID))
    conn.commit()
    cursor.close()
    
