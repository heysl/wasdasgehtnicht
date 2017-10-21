import socket
import sqlite3
import pymysql
import datetime
import time
import configparser

def get_datetime():
    now = datetime.datetime.now()
    now_unix = time.mktime(now.timetuple())
    now_timestamp = now.strftime('%Y-%m-%dT%H:%M')
    return now_unix, now_timestamp

def check_ip4(host, port, timeout):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET, socket.SOCK_STREAM).connect((host, port))
        return (True, None)
    except Exception as ex:
        #print(ex)
        return (False, str(ex))

def check_ip6(host, port, timeout):
    try:
        socket.setdefaulttimeout(timeout)
        socket.socket(socket.AF_INET6, socket.SOCK_STREAM).connect((host, port, 0, 0))
        return (True, None)
    except Exception as ex:
        #print(ex)
        return (False, str(ex))

def check_dns(hostname):
    try:
        socket.gethostbyname(hostname)
        return (True, None)
    except Exception as ex:
        #print(ex)
        return (False, str(ex))

def mysql_write(host, user, password, db, timeout=3, data):
    statement = "INSERT INTO wasdasgehtnicht VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
    try:
        con = pymysql.connect(host=host, user=user, password=password, db=db, timeout=timeout)
        with con:
            c = con.cursor()
            c.executemany(statement, data)
        return True
    except Exception as ex:
        return False

def sqlite_write(db, data):
    statement = "INSERT INTO wasdasgehtnicht VALUES (?, ?, ?, ?, ?, ?, ?, ?)"
    con = sqlite3.connect(db)
    with con:
        c = con.cursor()
        c.executemany(statement, data)

def sqlite_read(db):
    statement = "SELECT dt_unix, dt, status_ip4, error_ip4, status_ip6, error_ip6, status_dns, error_dns FROM wasdasgehtnicht"
    con = sqlite3.connect(db)
    with con:
        c = con.cursor()
        c.execute(statement)
        result = c.fetchall()
    return result

def sqlite_clear_table(db):
    statement = "DELETE FROM wasdasgehtnicht"
    con = sqlite3.connect(db)
    with con:
        c = con.cursor()
        c.execute(statement)


if __name__ == "__main__":
    #read settings.ini
    path = "settings.ini"

    config = configparser.ConfigParser()
    config.read(path)

    timeout = config.get("online_check", "timeout")
    host_ip4 = config.get("online_check", "host_ip4")
    port_ip4 = config.get("online_check", "port_ip4")
    host_ip6 = config.get("online_check", "host_ip6")
    port_ip6 = config.get("online_check", "port_ip6")
    host_dns = config.get("online_check", "host_dns")

    sqlite_db = config.get("sqlite", "file")

    my_host = config.get("mysql", "host")
    my_user = config.get("mysql", "user")
    my_passwd = config.get("mysql", "password")
    my_db = config.get("mysql", "db")
    
    #create list of values for insert
    timestamps = get_datetime()
    ip4 = check_ip4(host_ip4, port_ip4, timeout)
    ip6 = check_ip6(host_ip6, port_ip6, timeout)
    dns = check_dns(host_dns)

    insert = (
        timestamps[0],  #dt_unix real
        timestamps[1],  #dt text
        int(ip4[0]),    #status_ip4 int(1)
        ip4[1],         #error_ip4 text
        int(ip6[0]),    #status_ip6 int(1)
        ip6[1],         #error_ip6 text
        dns[0],         #status_dns int(1)
        dns[1]          #error_dns
    )

    #write action!
    if mysql_write(my_host, my_user, my_passwd, my_db, timeout, insert):
        sqlite_result = sqlite_read(sqlite_db)
        if len(sqlite_result) != 0:
            mysql_write(my_host, my_user, my_passwd, my_db, timeout, sqlite_result)
            sqlite_clear_table(sqlite_db)
    else:
        sqlite_write(sqlite_db, insert)