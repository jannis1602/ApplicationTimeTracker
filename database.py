import sqlite3

conn = sqlite3.connect("ApplicationTimeTracker/data.db")
c = conn.cursor()
try:
    c.execute("SELECT * FROM programs").fetchall()
except:
    c.execute("""CREATE TABLE programs(
                name text,
                date text,
                time integer
                )""")


def add_program(name, date, time=0):
    with conn:
        c.execute(
            "INSERT INTO programs VALUES (:name,:date,:time)", {"name": name, "date": date, "time": time})


def set_time(name, date, time):
    with conn:
        c.execute(
            "UPDATE programs SET time=:time WHERE date=:date AND name=:name", {"name": name, "date": date, "time": time})


def add_time(name, date, time):
    with conn:
        c.execute(
            "UPDATE programs SET time=time + :time WHERE date=:date AND name=:name", {"name": name, "date": date,  "time": time})


def get_time_by_program_date(name, date):
    with conn:
        c.execute("SELECT * FROM programs WHERE date=:date AND name=:name",
                  {"date": date, "name": name})
        return c.fetchone()


def get_times_by_program(name):
    with conn:
        c.execute("SELECT * FROM programs WHERE name=:name",
                  {"name": name})
        return c.fetchall()


def get_fulltime_by_program(name):
    with conn:
        c.execute("SELECT * FROM programs WHERE name=:name",
                  {"name": name})
        fulltime = 0
        for day in c.fetchall():
            fulltime += day[2]
        return fulltime


def delete_by_name(name):
    with conn:
        c.execute("DELETE FROM programs WHERE name=:name",
                  {"name": name})


def delete_by_name_and_date(name, date):
    with conn:
        c.execute("DELETE FROM programs WHERE name=:name AND date=:date",
                  {"name": name, "date": date})
