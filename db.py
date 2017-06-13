import os
import psycopg2
import urlparse

urlparse.uses_netloc.append("postgres")
url = urlparse.urlparse(os.environ["DATABASE_URL"])

class orderdb:
    def __init__(self):
        self.connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        self.cur = self.connection.cursor()

    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS foodorders (id serial, orders varchar, owner integer, name varchar, CONSTRAINT owner_name3 UNIQUE (owner, name));"
        self.cur.execute(tblstmt)
        self.connection.commit()

    def add_order(self, orders, owner, name):
        stmt = "INSERT INTO foodorders (orders, owner, name) VALUES (%s, %s, %s) ON CONFLICT (owner,name) DO UPDATE SET orders = EXCLUDED.orders;"
        args = (orders, owner, name)
        self.cur.execute(stmt, args)
        print("order added")
        self.connection.commit()

    def clear(self):
        stmt = "DELETE FROM foodorders;"
        self.cur.execute(stmt)
        self.connection.commit()

    def delete_order(self, owner):
        stmt = "DELETE FROM foodorders WHERE owner = %s"
        args = (owner, )
        self.cur.execute(stmt, args)
        self.connection.commit()

    def get_orders(self):
        stmt = "SELECT * FROM foodorders"
        try:
            self.cur.execute(stmt)
            print("get_orders executed")
            return self.cur
        except:
            print("Failure")
            return []


class polldb:
    def __init__(self):
        self.connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        self.cur = self.connection.cursor()

    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS PollResults (id serial, answer varchar, owner integer, name varchar, CONSTRAINT owner_name2 UNIQUE (owner, name));"
        self.cur.execute(tblstmt)
        self.connection.commit()

    def add_answer(self, answer, owner, name):
        stmt = "INSERT INTO PollResults (answer, owner, name) VALUES (%s, %s, %s) ON CONFLICT (owner,name) DO UPDATE SET answer = EXCLUDED.answer;"
        args = (answer, owner, name)
        self.cur.execute(stmt, args)
        print("answer added")
        self.connection.commit()

    def clear(self):
        stmt = "DELETE FROM PollResults;"
        self.cur.execute(stmt)
        self.connection.commit()

    def get_results(self, answer):
        stmt = "SELECT * FROM PollResults where answer = %s"
        try:
            args = (answer,)
            self.cur.execute(stmt, args)
            return self.cur
        except:
            print("Failure")
            return []

    def get_stats(self):
        stmt = "SELECT * FROM PollResults"
        x = dict()
        try:
            self.cur.execute(stmt)
            print("get_stats executed")
            for each in self.cur:
                key = each[1]
                if key in x:
                    x[key] += 1
                else:
                    x[key] = 1
            return x
        except:
            print("Failure")
            return x


class userdb:
    def __init__(self):
        self.connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        self.cur = self.connection.cursor()

    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS users (id serial, owner integer, name varchar, CONSTRAINT owner_name UNIQUE (owner, name));"
        self.cur.execute(tblstmt)
        self.connection.commit()

    def add_user(self, owner, name):
        stmt = "INSERT INTO users (owner, name) VALUES (%s, %s) ON CONFLICT (owner,name) DO NOTHING"
        args = (owner, name)
        self.cur.execute(stmt, args)
        self.connection.commit()

    def delete_user(self, name):
        stmt = "DELETE FROM users WHERE name = %s"
        args = (name, )
        self.cur.execute(stmt, args)
        self.connection.commit()

    def get_name(self):
        stmt = "SELECT * FROM users"
        try:
            self.cur.execute(stmt)
            print("get_name executed")
            return [x[2] for x in self.cur]
        except:
            print("Failure")
            return []

    def get_id_and_name(self):
        stmt = "SELECT * FROM users"
        self.cur.execute(stmt)
        print("get_id_and_name executed")
        return self.cur


class feedbackdb:
    def __init__(self):
        self.connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        self.cur = self.connection.cursor()

    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS Feedbacks (id serial, feedback varchar, kind varchar, owner integer, name varchar);"
        self.cur.execute(tblstmt)
        self.connection.commit()

    def add_item(self, feedback, kind, owner, name):
        print("Item added")
        stmt = "INSERT INTO Feedbacks (feedback, kind, owner, name) VALUES (%s, %s, %s, %s)"
        args = (feedback, kind, owner, name)
        self.cur.execute(stmt, args)
        self.connection.commit()

    def delete_item(self, feedback,):
        stmt = "DELETE FROM Feedbacks WHERE feedback = %s"
        args = (feedback, )
        self.cur.execute(stmt, args)
        self.connection.commit()

    def get_BOT(self):
        try:
            self.cur.execute("SELECT * FROM Feedbacks WHERE kind = %s", (("BOT Functions"),))
            print("get_BOT executed")
            return self.cur
        except:
            print("Failure")
            return []

    def get_General(self):
        try:
            self.cur.execute("SELECT * FROM Feedbacks WHERE kind = %s", (("General Feedback"),))
            print("get_General executed")
            return self.cur
        except:
            print("Failure")
            return []

    def get_all_from_name(self, name):
        stmt = "SELECT feedback FROM Feedbacks WHERE name = %s"
        args =(name, )
        try:
            self.cur.execute(stmt, args)
            return [x[0] for x in self.cur]
        except:
            print("Failure")
            return []

    def clear(self):
        stmt = "DELETE FROM Feedbacks;"
        self.cur.execute(stmt)
        self.connection.commit()

class eventdb:
    def __init__(self):
        self.connection = psycopg2.connect(
            database=url.path[1:],
            user=url.username,
            password=url.password,
            host=url.hostname,
            port=url.port
        )
        self.cur = self.connection.cursor()

    def setup(self):
        tblstmt = "CREATE TABLE IF NOT EXISTS Events (id serial, event varchar, A varchar, B varchar, C varchar, owner integer, name varchar);"
        self.cur.execute(tblstmt)
        self.connection.commit()

    def add_item(self, answer, owner, name):
        event, A, B, C = answer
        stmt = "INSERT INTO Events (event, A, B, C, owner, name) VALUES (%s, %s, %s, %s, %s, %s)"
        args = (event, A, B, C, owner, name)
        self.cur.execute(stmt, args)
        self.connection.commit()

    def delete_event(self, event):
        stmt = "DELETE FROM Events WHERE event = %s"
        args = (event, )
        self.cur.execute(stmt, args)
        self.connection.commit()

    def get_all_events(self):
        stmt = "SELECT event FROM Events"
        self.cur.execute(stmt)
        return self.cur

    def get_by_event(self, event):
        try:
            self.cur.execute("SELECT * FROM Events WHERE event = %s", (event,))
            print("get_event executed")
            return self.cur
        except:
            print("Failure")
            return []

    def get_all_from_name(self, name):
        stmt = "SELECT * FROM Events WHERE name = %s"
        args =(name, )
        try:
            self.cur.execute(stmt, args)
            return [x[0] for x in self.cur]
        except:
            print("Failure")
            return []

    def clear(self):
        stmt = "DELETE FROM Event;"
        self.cur.execute(stmt)
        self.connection.commit()
