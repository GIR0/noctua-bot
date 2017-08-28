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
        tblstmt = "CREATE TABLE IF NOT EXISTS foodorders (id serial, orderstarter integer, description varchar, orders varchar, owner integer, name varchar, status varchar);"
        self.cur.execute(tblstmt)
        self.connection.commit()

    def add_order(self, orderstarter, description, orders, owner, name):
        stmt = "INSERT INTO foodorders (orderstarter, description, orders, owner, name, status) VALUES (%s, %s, %s, %s, %s, %s);"
        args = (orderstarter, description, orders, owner, name, "")
        self.cur.execute(stmt, args)
        self.connection.commit()

    def clear(self):
        stmt = "DELETE FROM foodorders"
        print ("food cleared")
        self.cur.execute(stmt)
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
        stmt = "SELECT * FROM foodorders"
        try:
            self.cur.execute(stmt)
            hold = []
            for x in self.cur:
                hold.append((x[2],x[6]))
            return hold
        except:
            print("Failure")
            return []

    def lock(self, orderstarter):
        stmt = "UPDATE foodorders SET status = %s WHERE orderstarter = %s"
        args = ("(locked)", orderstarter)
        self.cur.execute(stmt, args)
        self.connection.commit()

    def unlock(self, orderstarter):
        stmt = "UPDATE foodorders SET status = %s WHERE orderstarter = %s"
        args = ("", orderstarter)
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

    def get_Bot(self):
        try:
            self.cur.execute("SELECT * FROM Feedbacks WHERE kind = %s", (("Bot Suggestions"),))
            print("get_Bot executed")
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

    def get_House(self):
        try:
            self.cur.execute("SELECT * FROM Feedbacks WHERE kind = %s", (("About House Events"),))
            print("get_House executed")
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
        tblstmt = "CREATE TABLE IF NOT EXISTS SurveyEvents (id serial, event varchar, A varchar, B varchar, C varchar, D varchar, owner integer, name varchar);"
        self.cur.execute(tblstmt)
        self.connection.commit()

    def add_item(self, answer, owner, name):
        event, A, B, C , D = answer
        stmt = "INSERT INTO SurveyEvents (event, A, B, C, D, owner, name) VALUES (%s, %s, %s, %s ,%s, %s, %s)"
        args = (event, A, B, C, D, owner, name)
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

class sampledb:
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
        tblstmt = "CREATE TABLE IF NOT EXISTS Sample (id serial, title varchar, option varchar, owner integer, name varchar, CONSTRAINT owner_name5 UNIQUE (option, owner, name));"
        self.cur.execute(tblstmt)
        self.connection.commit()

    def action(self, title, option, owner, name):
        stmt = "INSERT INTO Sample (title, option, owner, name) VALUES (%s, %s, %s, %s) ON CONFLICT (option,owner,name) DO NOTHING;"
        args = (title, option, owner, name)
        self.cur.execute(stmt, args)
        self.connection.commit()

    def delete_title(self, title):
        stmt = "DELETE FROM Sample WHERE title = %s"
        args = (title, )
        self.cur.execute(stmt, args)
        self.connection.commit()

    def get_all_titles(self):
        stmt = "SELECT title FROM Sample"
        self.cur.execute(stmt)
        return self.cur

    def get_by_title(self, title):
        try:
            self.cur.execute("SELECT * FROM Sample WHERE title = %s", (title,))
            print("get_by_title executed")
            return self.cur
        except:
            print("Failure")
            return []

    def get_results(self, title, option):
        stmt = "SELECT * FROM Sample WHERE title = %s AND option = %s"
        try:
            args = (title, option)
            self.cur.execute(stmt, args)
            return self.cur
        except:
            print("Failure")
            return []

    def get_stats(self, title):
        x = dict()
        try:
            self.cur.execute("SELECT * FROM Sample WHERE title = %s", (title,))
            for each in self.cur:
                key = each[2]
                if key in x:
                    if each[3] != 0:
                        x[key] += 1
                else:
                    if each[3] != 0:
                        x[key] = 1
            return x
        except:
            print("Failure")
            return x

    def clear(self):
        stmt = "DELETE FROM Sample;"
        self.cur.execute(stmt)
        self.connection.commit()

class samplerecord:
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
        tblstmt = "CREATE TABLE IF NOT EXISTS SampleRecord (id serial, title varchar, inline_message_id integer);"
        self.cur.execute(tblstmt)
        self.connection.commit()

    def add_id(self, title, inline_message_id):
        stmt = "INSERT INTO SampleRecord (title, inline_message_id) VALUES (%s, %s);"
        args = (title, inline_message_id)
        self.cur.execute(stmt, args)
        self.connection.commit()

    def get_by_id(self, inline_message_id):
        try:
            self.cur.execute("SELECT * FROM SampleRecord WHERE inline_message_id = %s", (inline_message_id,))
            return self.cur
        except:
            print("Failure")
            return []

    def clear(self):
        stmt = "DELETE FROM SampleRecord;"
        self.cur.execute(stmt)
        self.connection.commit()

class onodb:
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
        tblstmt = "CREATE TABLE IF NOT EXISTS ONO (id serial, four varchar, owner integer, name varchar, registered varchar);"
        self.cur.execute(tblstmt)
        self.connection.commit()

    def start(self, four):
        stmt = "INSERT INTO ONO (four, owner, name, registered) VALUES (%s, %s, %s, %s)"
        args = (four, 0, "-", "no")
        self.cur.execute(stmt, args)
        self.connection.commit()

    def register(self, four, owner, name):
        stmt = "DELETE FROM ONO WHERE four = %s"
        args = (four, )
        self.cur.execute(stmt, args)
        self.connection.commit()
        stmt = "INSERT INTO ONO (four, owner, name, registered) VALUES (%s, %s, %s, %s)"
        args = (four, owner, name, "yes")
        self.cur.execute(stmt, args)
        self.connection.commit()

    def reset(self, four):
        stmt = "DELETE FROM ONO WHERE four = %s"
        args = (four, )
        self.cur.execute(stmt, args)
        self.connection.commit()
        stmt = "INSERT INTO ONO (four, owner, name, registered) VALUES (%s, %s, %s, %s)"
        args = (four, 0, "-", "no")
        self.cur.execute(stmt, args)
        self.connection.commit()

    def get_four(self):
        stmt = "SELECT * FROM ONO"
        try:
            self.cur.execute(stmt)
            return self.cur
        except:
            print("Failure")
            return []

    def get_four_from_owner(self, owner):
        stmt = "SELECT * FROM ONO WHERE owner = %s"
        args = (owner, )
        try:
            self.cur.execute(stmt, args)
            return self.cur
        except:
            print("Failure")
            return []

    def get_owner_from_four(self, four):
        stmt = "SELECT * FROM ONO WHERE four = %s"
        args = (four, )
        try:
            self.cur.execute(stmt, args)
            return self.cur
        except:
            print("Failure")
            return []

    def clear(self):
        stmt = "DELETE FROM ONO;"
        self.cur.execute(stmt)
        self.connection.commit()
