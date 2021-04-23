import sqlite3
import datetime
import threading
# TODO database for all programs: MainName/Title - status(on/off) - filterStrings - config: count in background

# TODO rename programs to programTimes...

# TODO settings database

conn = sqlite3.connect("ApplicationTimeTracker/data.db",
                       check_same_thread=False)
c = conn.cursor()

lock = threading.Lock()


# TODO config if filter equals or contains

# delete Table:
# with conn:
#     c.execute("DROP TABLE program_state")

try:
    with conn:
        c.execute("SELECT * FROM program_state").fetchone()
except:  # with conn: ?
    with conn:
        c.execute("""CREATE TABLE program_state(    
                        name text,
                        state integer
                        )""")

# with conn:        # for later     # background state per filter?
#     c.execute("""CREATE TABLE program_filter(
#                 name text,
#                 filter text
#                 )""")


# with conn:
#     c.execute("""CREATE TABLE program_config(
#                 name text,
#                 state text,
#                 background integer,   #1=true
#                 filter_string text
#                 )""")

try:
    with conn:
        c.execute("SELECT * FROM program_times").fetchone()
except:
    with conn:
        c.execute("""CREATE TABLE program_times(
                    name text,
                    date text,
                    time integer
                    )""")

# Rename table:
# with conn:
#     c.execute("ALTER TABLE programTimes RENAME TO program_times")

# with conn:
#     c.execute("SELECT * FROM program_times")
#     print(c.fetchall())

# ---------- program_state - database ----------


def get_program_state(name):
    with conn:
        c.execute("SELECT * FROM program_state WHERE name=:name",
                  {"name": name})
    print(c.fetchall())
    # if len(c.fetchone()) == 2:
    #     return c.fetchone()[1]
    # else:
    #     return None


def add_program_state(name):
    if get_program_state(name) == None:
        with conn:
            c.execute(
                "INSERT INTO program_state VALUES (:name,:state)", {"name": name, "state": 1})


# add_program_state("Opera")

def delete_program_state(name):
    with conn:
        c.execute("DELETE FROM program_state WHERE name=:name", {"name": name})


def get_all_programs_from_state():
    with conn:
        programs = []
        c.execute("SELECT * FROM program_state")
        for p in c.fetchall():
            programs.append(p[0])
    return programs


def get_all_active_programs():
    lock.acquire(True)
    with conn:
        c.execute("SELECT * FROM program_state  WHERE state=1")
        programs = []
        for e in c.fetchall():
            programs.append(e[0])
    lock.release()
    return programs


def get_all_inactive_programs():
    with conn:
        c.execute("SELEKT * FROM program_state WHERE state=0")
    return c.fetchall()


def set_program_state(name, state):
    if state == True:
        with conn:
            c.execute(
                "UPDATE program_state SET state=:state WHERE name=:name", {"name": name, "state": state})
    elif state == False:
        with conn:
            c.execute(
                "UPDATE program_state SET state=:state WHERE name=:name", {"name": name, "state": state})


# ---------- program_times - database ----------

def get_all():
    with conn:
        c.execute("SELECT * FROM program_times")
        return c.fetchall()


def get_all_programs():  # get all from program_times      # TODO remove
    with conn:
        programs = []
        c.execute("SELECT * FROM program_times")
        for p in c.fetchall():
            if programs.count(p[0]) == 0:
                programs.append(p[0])
    return programs


def add_program(name, date=datetime.datetime.now().date(), time=0):
    with conn:
        c.execute(
            "INSERT INTO program_times VALUES (:name,:date,:time)", {"name": name, "date": date, "time": time})


def set_time(name, date, time):
    with conn:
        c.execute(
            "UPDATE program_times SET time=:time WHERE date=:date AND name=:name", {"name": name, "date": date, "time": time})


def add_time(name, date, time):
    with conn:
        c.execute(
            "UPDATE program_times SET time=time + :time WHERE date=:date AND name=:name", {"name": name, "date": date,  "time": time})


def add_time_if_name_exists(name, date, time):
    with conn:
        # TODO replace get times durch program/config database
        if len(get_times_by_program(name)) >= 1 and get_time_by_program_date(name=name, date=date) == None:
            add_program(name, date)
        c.execute(
            "UPDATE program_times SET time=time + :time WHERE date=:date AND name=:name", {"name": name, "date": date,  "time": time})


def get_time_by_program_date(name, date):
    with conn:
        c.execute("SELECT * FROM program_times WHERE date=:date AND name=:name",
                  {"date": date, "name": name})
        return c.fetchone()


def get_times_by_program(name):
    with conn:
        c.execute("SELECT * FROM program_times WHERE name=:name",
                  {"name": name})
        return c.fetchall()


def get_fulltime_by_program(name):
    lock.acquire(True)
    with conn:
        c.execute("SELECT * FROM program_times WHERE name=:name",
                  {"name": name})
        fulltime = 0
        for day in c.fetchall():
            fulltime += day[2]
        lock.release()
        return fulltime


def delete_by_name(name):
    with conn:
        c.execute("DELETE FROM program_times WHERE name=:name",
                  {"name": name})


def delete_by_name_and_date(name, date):
    with conn:
        c.execute("DELETE FROM program_times WHERE name=:name AND date=:date",
                  {"name": name, "date": date})
