import configparser

def createConfig(path):
    config = configparser.ConfigParser()
    #db-schema
    config.add_section("db-schema")
    config.set("db-schema", "schema", "create_db.sql")
    #sqlite
    config.add_section("sqlite")
    config.set("sqlite", "file", "wasdasgehtnicht.db")
    #mysql
    config.add_section("mysql")
    config.set("mysql", "host", "hostname")
    config.set("mysql", "user", "mysql_user")
    config.set("mysql", "password", "mysql_password")
    config.set("mysql", "db", "mysql_db")
    #online_check
    config.add_section("online_check")
    config.set("online_check", "timeout", "3")
    config.set("online_check", "host_ip4", "8.8.8.8")
    config.set("online_check", "port_ip4", "53")
    config.set("online_check", "host_ip6", "2001:4860:4860::8888")
    config.set("online_check", "port_ip6", "53")
    config.set("online_check", "host_dns", "www.google.de")

    with open(path, "w+") as config_file:
        config.write(config_file)

if __name__ == "__main__":
    path = "settings.ini"
    createConfig(path)


