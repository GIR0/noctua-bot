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
        tblstmt = "CREATE TABLE IF NOT EXISTS foodorders (id serial, orderstarter integer, description varchar, orders varchar, owner integer, name varchar);"
        self.cur.execute(tblstmt)
        self.connection.commit()

    def add_order(self, orderstarter, description, orders, owner, name):
        stmt = "INSERT INTO foodorders (orderstarter, description, orders, owner, name) VALUES (%s, %s, %s, %s, %s);"
        args = (orderstarter, description, orders, owner, name)
        self.cur.execute(stmt, args)
        self.connection.commit()

    def clear_by_orderstarter(self, orderstarter):
        stmt = "DELETE FROM foodorders WHERE orderstarter = %s;"
        args = (orderstarter,)
        self.cur.execute(stmt, args)
        self.connection.commit()

    def clear_order(self, orders, owner):
        stmt = "DELETE FROM foodorders WHERE orders = %s AND owner = %s"
        args = (orders, owner)
        self.cur.execute(stmt, args)
        self.connection.commit()

    def clear_by_description(self, description):
        stmt = "DELETE FROM foodorders WHERE description = %s;"
        args = (description,)
        self.cur.execute(stmt, args)
        self.connection.commit()

    def get_by_order(self, orders, owner):
        stmt = "SELECT * FROM foodorders WHERE orders = %s AND owner = %s"
        try:
            args = (orders, owner)
            self.cur.execute(stmt, args)
            return self.cur
        except:
            print("Failure")
            return []

    def get_by_orderstarter(self, orderstarter):
        stmt = "SELECT * FROM foodorders WHERE orderstarter = %s"
        try:
            args = (orderstarter,)
            self.cur.execute(stmt, args)
            return self.cur
        except:
            print("Failure")
            return []

    def get_by_owner(self, owner):
        stmt = "SELECT * FROM foodorders WHERE owner = %s"
        try:
            args = (owner,)
            self.cur.execute(stmt, args)
            return self.cur
        except:
            print("Failure")
            return []

    def get_by_owner_description(self, owner, description):
        stmt = "SELECT * FROM foodorders WHERE owner = %s AND description = %s"
        try:
            args = (owner, description)
            self.cur.execute(stmt, args)
            return self.cur
        except:
            print("Failure")
            return []

    def get_by_owner_orderstarter(self, owner, orderstarter):
        stmt = "SELECT * FROM foodorders WHERE owner = %s AND orderstarter = %s"
        try:
            args = (owner, orderstarter)
            self.cur.execute(stmt, args)
            return self.cur
        except:
            print("Failure")
            return []

    def get_by_description(self, description):
        stmt = "SELECT * FROM foodorders WHERE description = %s"
        try:
            args = (description,)
            self.cur.execute(stmt, args)
            return self.cur
        except:
            print("Failure")
            return []

    def get_all(self):
        stmt = "SELECT * FROM foodorders"
        try:
            self.cur.execute(stmt)
            return self.cur
        except:
            print("Failure")
            return []

    def get_all_description(self):
        stmt = "SELECT description FROM foodorders"
        try:
            self.cur.execute(stmt)
            return self.cur
        except:
            print("Failure")
            return []

    def lock(self, orderstarter):
        stmt = "UPDATE foodorders SET description = %s WHERE orderstarter = %s"
        args = ("locked", orderstarter)
        self.cur.execute(stmt, args)
        self.connection.commit()

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

    def get_all(self):
        stmt = "SELECT * FROM PollResults"
        try:
            self.cur.execute(stmt)
            return self.cur
        except:
            print("Failure")
            return []


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

class surveydb:
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
        tblstmt = "CREATE TABLE IF NOT EXISTS SurveyEvents (id serial, event varchar, A varchar, B varchar, C varchar, owner integer, name varchar);"
        self.cur.execute(tblstmt)
        self.connection.commit()

    def add_item(self, answer, owner, name):
        event, A, B, C = answer
        stmt = "INSERT INTO SurveyEvents (event, A, B, C, owner, name) VALUES (%s, %s, %s, %s, %s, %s)"
        args = (event, A, B, C, owner, name)
        self.cur.execute(stmt, args)
        self.connection.commit()

    def delete_event(self, event):
        stmt = "DELETE FROM SurveyEvents WHERE event = %s"
        args = (event, )
        self.cur.execute(stmt, args)
        self.connection.commit()

    def get_all_events(self):
        stmt = "SELECT event FROM SurveyEvents"
        self.cur.execute(stmt)
        return self.cur

    def get_by_event(self, event):
        try:
            self.cur.execute("SELECT * FROM SurveyEvents WHERE event = %s", (event,))
            print("get_event executed")
            return self.cur
        except:
            print("Failure")
            return []

    def clear(self):
        stmt = "DELETE FROM SurveyEvents;"
        self.cur.execute(stmt)
        self.connection.commit()

class ratedb:
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
        tblstmt = "CREATE TABLE IF NOT EXISTS RateEvents (id serial, event varchar, answer varchar, owner integer, name varchar, CONSTRAINT owner_name4 UNIQUE (event, owner, name));"
        self.cur.execute(tblstmt)
        self.connection.commit()

    def add_item(self, event, answer, owner, name):
        stmt = "INSERT INTO RateEvents (event, answer, owner, name) VALUES (%s, %s, %s, %s) ON CONFLICT (event,owner,name) DO UPDATE SET answer = EXCLUDED.answer;"
        args = (event, answer, owner, name)
        self.cur.execute(stmt, args)
        self.connection.commit()

    def delete_event(self, event):
        stmt = "DELETE FROM RateEvents WHERE event = %s"
        args = (event, )
        self.cur.execute(stmt, args)
        self.connection.commit()

    def get_all_events(self):
        stmt = "SELECT event FROM RateEvents"
        self.cur.execute(stmt)
        return self.cur

    def get_by_event(self, event):
        try:
            self.cur.execute("SELECT * FROM RateEvents WHERE event = %s", (event,))
            print("get_event executed")
            return self.cur
        except:
            print("Failure")
            return []

    def get_results(self, event, answer):
        stmt = "SELECT * FROM RateEvents WHERE event = %s AND answer = %s"
        try:
            args = (event, answer)
            self.cur.execute(stmt, args)
            return self.cur
        except:
            print("Failure")
            return []

    def get_stats(self, event):
        x = dict()
        try:
            self.cur.execute("SELECT * FROM RateEvents WHERE event = %s", (event,))
            print("get_stats executed")
            for each in self.cur:
                key = each[2]
                if key in x:
                    x[key] += 1
                else:
                    x[key] = 1
            return x
        except:
            print("Failure")
            return x

    def clear(self):
        stmt = "DELETE FROM RateEvents;"
        self.cur.execute(stmt)
        self.connection.commit()
