# wasdasgehtnicht

Sometimes my ISP sucks bad.
Let's track this splendid performance!

## Getting Started

### Prerequisites

* Python3 (tested on 3.4, 3.5 and 3.6)
* MySQL with an existing DB and user with write-access
* PyMySQL-Python module

### Installing

#### Clone this repo
```
$ git clone https://github.com/heysl/wasdasgehtnicht/ && cd wasdasgehtnicht
```

#### Install PyMySQL
```
$ pip install pymysql
```

#### Create settings.ini
The settings.ini can be created by a short little script.
```
$ python createConfig.py
```
Edit the values according to your needs. You usually only need to change the [mysql]-section.
```
[db-schema]
schema = schema.sql

[sqlite]
file = wasdasgehtnicht.db

[mysql]
host = your_mysql_server
user = my_user
password = my_password
db = my_db

[online_check]
timeout = 3
host_ip4 = 8.8.8.8
port_ip4 = 53
host_ip6 = 2001:4860:4860::8888
port_ip6 = 53
host_dns = www.google.com
```
#### Create DB-Schema
Actually there is only one table to create... Once again, there is a script for this tedious work.
It will create the sqlite-file and the table for your mySQL-DB.
```
$ python createSchema.py
```

Ready to go!

## Usage
### Manually
Just execute wasdasgehtnicht.py
```
$ python wasdasgehtnicht.py
```
### Automation
```
$ crontab -e
```
#### Example

```
*/2 * * * * cd /home/osmc/wasdasgehtnicht && /home/osmc/wasdasgehtnicht/env/bin/python /home/osmc/wasdasgehtnicht/wasdasgehtnicht.py
```
* Executes the script every two minutes.
* As the script needs to have the settings.ini in the same path, cron needs to cd into the working directory first.
* As I run the script in a python-venv, cron needs to know the desired python interpreter.  

## OK, now what does it do?
1. Check internet connection by trying to establish
    - an IPv4-socket
    - an IPv6-socket
    - a socket by hostname (=check DNS)

2. Write the results to a Database.  
    I use MySQL-Server on a NAS-System for this purpose. However, this system is not online 24/7.
    - For the NAS' offline-times, the results are cached in a local sqlite-db-file.
    - Once the NAS is online again, the cached results are written to the mysql-DB and the local cache is cleared.

