import sqlite3

class Model:
    tabela = 'ime_tabele'
    povezava = None

    @classmethod
    def posodobi(cls, pogoji, vrednosti):
        if not cls.povezava:
            cls.dobi_povezavo()
        sql = "UPDATE " +cls.tabela + " SET "
        vrednosti_sql = [ vrednost + '=' + str(vrednosti[vrednost]) for vrednost in vrednosti]
        sql += ", ".join(vrednosti_sql)
        sql += " WHERE "
        pogoji_sql = [ kolona+'=?' for kolona in pogoji ]
        sql += " AND ".join(pogoji_sql)
        cursor = cls.povezava.cursor()
        pogoji_vrednosti = list(pogoji.values())
        cursor.execute(sql, pogoji_vrednosti)
        cls.povezava.commit()
        
    @classmethod
    def odstrani(cls, pogoji):
        if not cls.povezava:
            cls.dobi_povezavo()
        sql = "DELETE FROM " +cls.tabela + " WHERE "
        pogoji_sql = [ kolona+'=?' for kolona in pogoji ]
        sql += " AND ".join(pogoji_sql)
        cursor = cls.povezava.cursor()
        pogoji_vrednosti = list(pogoji.values())
        cursor.execute(sql, pogoji_vrednosti)
        cls.povezava.commit()

    @classmethod
    def dobi_povezavo(cls):
        if not cls.povezava:
            cls.povezava = sqlite3.connect("BlackJack.db")
    
    @classmethod
    def dobi(cls, pogoji):
        if not cls.povezava:
            cls.dobi_povezavo()
        sql = "SELECT * FROM "+cls.tabela
        sql += " WHERE "
        pogoji_sql = [ kolona+'=?' for kolona in pogoji ]
        sql += " AND ".join(pogoji_sql)
        cursor = cls.povezava.cursor()
        vrednosti = list(pogoji.values())
        cursor.execute(sql, vrednosti)
        cls.povezava.commit()
        return cursor.fetchone()
    
    @classmethod
    def ustvari(cls, podatki):
        if not cls.povezava:
            cls.dobi_povezavo()
        kljuci = list(podatki.keys())
        sql = "INSERT INTO "+cls.tabela+" ("
        sql += ",".join(kljuci)
        sql += ") VALUES ( "
        vprasaji = ['?' for i in range(0, len(kljuci))]
        sql += ",".join(vprasaji)
        sql += " )"
        cursor = cls.povezava.cursor()
        vrednosti = list(podatki.values())
        cursor.execute(sql, vrednosti)
        cls.povezava.commit()
        
class Uporabnik(Model):
    tabela = 'uporabnik'

class Igra(Model):
    tabela = "igra" 
    
    @classmethod
    def dobi_aktivno(cls, uporabnik_id):
        if not cls.povezava:
            cls.dobi_povezavo()
        sql = "SELECT * FROM "+cls.tabela
        sql += " WHERE uporabnik_id=? AND status < 3 "
        cursor = cls.povezava.cursor()
        cursor.execute(sql,(uporabnik_id,))
        cls.povezava.commit()
        return cursor.fetchone()

    

    
    


