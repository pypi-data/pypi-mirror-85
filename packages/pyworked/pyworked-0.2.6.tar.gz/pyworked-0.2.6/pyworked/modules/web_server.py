from http.server import HTTPServer, CGIHTTPRequestHandler
import cgi
import html
import http.cookies
import os
import sqlite3 as sql

class Web:

    def __init__(self):
        pass

    def start(self, adr):
        httpd = HTTPServer(adr, CGIHTTPRequestHandler)
        httpd.serve_forever()

    def heading(self):
        return("Content-type: text/html")

    def parse(self, file, htm):
        css = open(file, 'r').read()
        htm = open(htm, 'r').read()
        msg = '<style>' + css + '</style>' + htm
        return(msg)
    
    def get_form_value(self, name):
        txt = cgi.FieldStorage().getfirst(name, "undefined")
        txt = html.escape(txt)
        return(txt)

    def is_cookie(self, name):
        cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
        cookie = cookie.get(name)
        if cookie != None:
            return True
        else:
            return True

    def set__cookie(self, name, value, path):
        return("Set-cookie: " + name + '=' + value + '; expires=Wed May 18 03:33:20 2033; path=' + path)

    def get_cookie(self, name):
        cookie = http.cookies.SimpleCookie(os.environ.get("HTTP_COOKIE"))
        cookie = cookie.get(name)
        return(cookie.value)

    def db_connect(self, name):
        self.con = sql.connect(name)

    def db_create(self, name, params):
        cur = self.con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS `" + name + "` " + params)
        self.con.commit()
        cur.close()

    def db_insert(self, name, values):
        cur = self.con.cursor()
        cur.execute("INSERT INTO `" + name + "` " + values)
        self.con.commit()
        cur.close()

    def db_select(self, what, name, params):
        cur = self.con.cursor()
        cur.execute("SELECT " + what + " `" + name + "` WHERE " + params)
        return(cur.fetchall())
        cur.close()

    def db_update(self, name, sets, params):
        cur = self.con.cursor()
        cur.execute("UPDATE " + name + " SET " + sets + " WHERE " + params)
        self.con.commit()
        cur.close()

    def db_delete(self, name, params):
        cur = self.con.cursor()
        cur.execute("DELETE FROM " + name + " WHERE " + params)
        self.con.commit()
        cur.close()