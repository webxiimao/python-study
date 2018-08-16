import mysql.connector


MYSQL_HOSTS = '127.0.0.1'
MYSQL_USER = 'root'
MYSQL_PASSWORD = 'root'
MYSQL_PORT = '3306'
MYSQL_DB = 'spider'


cnx = mysql.connector.connect(user=MYSQL_USER, host=MYSQL_HOSTS, password=MYSQL_PASSWORD, database=MYSQL_DB)

cur = cnx.cursor(buffered=True)

class Sql:
    @classmethod
    def insert_dd_name(cls,xs_name, xs_author, category, name_id):
        sql = 'INSERT INTO dd_name(`xs_name`, `xs_author`, `category`, `name_id`) VALUES(%(xs_name)s, %(xs_author)s, %(category)s, %(name_id)s)'
        value = {
            'xs_name':xs_name,
            'xs_author':xs_author,
            'category':category,
            'name_id':name_id
        }
        cur.execute(sql, value)
        cnx.commit()

    @classmethod
    def select_name(cls,name_id):
        sql = 'SELECT EXISTS(SELECT1 FROM dd_name WHERE name_id = %(name_id)s)'
        value = {
            'name_id':name_id,
        }
        cur.execute(sql, value)
        return cur.fetchall()[0]