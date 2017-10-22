import sys
sys.path.append('/usr/local/lib/python2.7/dist-packages/')
import sqlite3
from pymongo import MongoClient


class DbConnect(object):

    def __init__(self):
        self.conn = sqlite3.connect('timeSchesuling.db')
        self.cursor = self.conn.cursor()

    def create_table(self):
        self.cursor.execute('''CREATE TABLE yapilacaklar (Liste_Indexi, Ust_Konu,
        Gorev_Ismi, Oncelik, Son_Bitis_Tarihi, Tahmini_Yapis_Suresi, Aciliyet)''')
        self._committing()

    def inserting_new_information(self, ust_konu, ders_adi, oncelik, son_bitis_tarihi, tahmini_yapis_suresi):

        # aciliyet = (int(oncelik)*20 + int(tahmini_yapis_suresi)*20 + (20 - int(son_bitis_tarihi))*10*70)/100
        aciliyet = oncelik
        self.conn.execute("INSERT INTO yapilacaklar VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%d')"
                          % (self.cursor.execute("SELECT COUNT(*) FROM yapilacaklar;"), ust_konu, ders_adi, oncelik, son_bitis_tarihi, tahmini_yapis_suresi, aciliyet))
        self._committing()

    def _committing(self):
        self.conn.commit()

    def fetch_the_data_fromDB(self):
        self.cursor.execute('''SELECT Ust_Konu,
        Gorev_Ismi, Oncelik, Son_Bitis_Tarihi, Tahmini_Yapis_Suresi FROM yapilacaklar ORDER BY Aciliyet ASC''')
        return self.cursor.fetchall()

    def retrieve_a_row(self, index):
        self.cursor.execute("SELECT * FROM yapilacaklar DESC LIMIT '%d', 1" % index)
        # self.cursor.execute("DELETE FROM yapilacaklar WHERE DESC LIMIT '%d', 1" % index)
        eleman = self.cursor.fetchone()
        self._committing()
        return eleman

    def delete_the_clicked_row(self, anahtar):
        # Henuz herhangi bir sey silinmiyor!!!
        self.cursor.execute("DELETE FROM yapilacaklar WHERE Liste_Indexi='%s'" % anahtar)
        # self.cursor.execute("DELETE FROM yapilacaklar WHERE Liste_Indexi='<sqlite3.Cursor object at 0x7f8676c89960>'")
        self._committing()

    def close_db_connection(self):
        self.conn.close()


class DatabaseConnection:

    def __init__(self):
        self.host = 'localhost'
        self.port = 27017
        self.collection_name = 'todos'
        self.database_name = 'todo_database'
        self.client = MongoClient(host=self.host, port=self.port)

        self.database = self.client.get_database(self.database_name)
        self.collection = self.database[self.collection_name]

    def insert_doc(self, name, todo, priority, deadline, estimated_duration):
        query = {
            "name": name,
            "todo": todo,
            "priority": priority,
            "deadline": deadline,
            "estimated_duration": estimated_duration
        }
        id_of_inserted_object = self.collection.insert(query)
        return id_of_inserted_object

    def get_all_docs(self):
        return self.collection.find()

    def remove_item(self, item_name):
        query = {"name": item_name}
        self.collection.remove(query)


'''
Burada neye gore siralayacagimizi belirleyecegiz!!

yapilibilirlik (belirli bir zaman dilimi icerisinde) %20
oncelik %20
son bitim tarihi %60

Aciliyet: (20.yapilabilirlik + 20.oncelik + 60.10/(Son gun - Bugun)) / 100

'''



















