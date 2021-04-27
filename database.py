import sqlite3
import datetime
import threading
# TODO database for all programs: MainName/Title - status(on/off) - filterStrings - config: count in background

# TODO #24 (data_times.db + data_config.db + settings.json)

# TODO files in ApplicationTimeTracker/data/...

# TODO config if filter equals or contains

# TODO filepath as var

conn = sqlite3.connect("ApplicationTimeTracker/data.db",
                       check_same_thread=False)
c = conn.cursor()

lock = threading.Lock()

# delete Table:
# with conn:
#     c.execute("DROP TABLE program_state")

# Rename table:
# with conn:
#     c.execute("ALTER TABLE programTimes RENAME TO program_times")

# program_state
try:
    with conn:
        c.execute("SELECT * FROM program_state").fetchone()
except:
    with conn:
        c.execute("""CREATE TABLE program_state(
                        name TEXT,
                        state INTEGER,    
                        bg_tracking INTEGER      
                        )""")       # 0=false - 1=true

# TODO (change state to tracking - 1/0 ?)
# TODO program_state add bg_tracking INTEGER

# program_filter
try:
    with conn:
        c.execute("SELECT * FROM program_filter").fetchone()
except:
    with conn:
        c.execute("""CREATE TABLE program_filter(
                    name TEXT,
                    filter_string TEXT
                    )""")

# program_times
try:
    with conn:
        c.execute("SELECT * FROM program_times").fetchone()
except:
    with conn:
        c.execute("""CREATE TABLE program_times(
                    name TEXT,
                    date TEXT,
                    time INTEGER,
                    bg_time INTEGER
                    )""")


# ---------- program_methodes ----------

# def add_program(name):
#     if get_program_state(name) == None:
#         with conn:
#             c.execute(
#                 "INSERT INTO program_state VALUES (:name,:state,:bg_tracking)", {"name": name, "state": 1, "bg_tracking": 1})
        # new in other tables...


# TODO rename filter ...


# ---------- program_state - database ----------
def get_program_state(name):
    with conn:
        c.execute("SELECT * FROM program_state WHERE name=:name",
                  {"name": name})
        temp = c.fetchone()
    if temp == None:
        return None
    else:
        return temp[1]


def get_program_bg_tracking_state(name):
    with conn:
        c.execute("SELECT * FROM program_state WHERE name=:name",
                  {"name": name})
        temp = c.fetchone()
    if temp == None:
        return None
    else:
        return temp[2]


def add_program_state(name):
    if get_program_state(name) == None:
        with conn:
            c.execute(
                "INSERT INTO program_state VALUES (:name,:state,:bg_tracking)", {"name": name, "state": 1, "bg_tracking": 0})
        add_program_filter(name, name)  # for default value


def delete_program_state(name):
    with conn:
        c.execute("DELETE FROM program_state WHERE name=:name", {"name": name})
    # TODO delete times and filter


def get_all_programs():
    lock.acquire(True)
    with conn:
        programs = []
        c.execute("SELECT * FROM program_state")
        for p in c.fetchall():
            programs.append(p[0])
    lock.release()
    return programs


def get_all_active_programs():
    lock.acquire(True)
    with conn:
        c.execute("SELECT * FROM program_state WHERE state=1")
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
    # if state == True:
    with conn:
        c.execute(
            "UPDATE program_state SET state=:state WHERE name=:name", {"name": name, "state": state}) 
    # elif state == False:
    #     with conn:
    #         c.execute(
    #             "UPDATE program_state SET state=:state WHERE name=:name", {"name": name, "state": state})


def set_program_bg_tracking_state(name, bg_tracking):
    with conn:
        c.execute(
            "UPDATE program_state SET bg_tracking=:bg_tracking WHERE name=:name", {"name": name, "bg_tracking": bg_tracking})


# ---------- program_filter - database ----------           # TODO if exists requests for all!!!

def get_all_program_filter():
    with conn:
        c.execute("SELECT * FROM program_filter")
        return c.fetchall()

# print(get_all_program_filter())


def get_program_filter(name):
    with conn:
        c.execute("SELECT * FROM program_filter WHERE name =:name",
                  {"name": name})
        filterStrings = []
        for s in c.fetchall():
            filterStrings.append(s[1])
        if len(filterStrings) == 0:   # -> no bugs?
            return [name]
    return filterStrings

# print(get_program_filter("Opera"))


def add_program_filter(name, filterString):
    # TODO if prog.state exists
    if get_program_state(name) is not None and get_program_filter(name).count(filterString) == 0:
        with conn:
            c.execute(
                "INSERT INTO program_filter VALUES (:name,:string)", {"name": name, "string": filterString})

# add_program_filter("Opera","web")


def delete_program_filter_string(name, filterString):
    with conn:
        c.execute(
            "DELETE FROM program_filter WHERE name =:name AND filter_string=:filter_string", {"name": name, "filter_string": filterString})


def delete_all_program_filter(filterString):
    with conn:
        c.execute("DELETE FROM program_filter WHERE filter_string=:filter_string",
                  {"filter_string": filterString})

# delete_program_filter("Opera","web")


# ---------- program_times - database ----------

def get_all_program_times():
    with conn:
        c.execute("SELECT * FROM program_times")
        return c.fetchall()


# def get_all_programs_from_time():  # get all from program_times      # TODO remove? -> or check wrong on startup?
#     with conn:
#         programs = []
#         c.execute("SELECT * FROM program_times")
#         for p in c.fetchall():
#             if programs.count(p[0]) == 0:
#                 programs.append(p[0])
#     return programs


def add_program_time(name, date=datetime.datetime.now().date(), time=0, bg_time=0):
    with conn:
        c.execute(
            "INSERT INTO program_times VALUES (:name,:date,:time,:bg_time)", {"name": name, "date": date, "time": time, "bg_time": bg_time})


def set_time(name, date, time):
    with conn:
        if not get_program_state(name) == None and get_time_by_program_date(name=name, date=date) == None:
            add_program_time(name, date, time)
        else:
            c.execute(
                "UPDATE program_times SET time=:time WHERE date=:date AND name=:name", {"name": name, "date": date, "time": time})


def add_time(name, date, time):
    with conn:
        if not get_program_state(name) == None and get_time_by_program_date(name=name, date=date) == None:
            add_program_time(name, date, time)
        else:
            c.execute(
                "UPDATE program_times SET time=time + :time WHERE date=:date AND name=:name", {"name": name, "date": date,  "time": time})


def set_bg_time(name, date, bg_time):
    with conn:
        if not get_program_state(name) == None and get_time_by_program_date(name=name, date=date) == None:
            add_program_time(name, date, bg_time=bg_time)
        else:
            c.execute(
                "UPDATE program_times SET bg_time=:bg_time WHERE date=:date AND name=:name", {"name": name, "date": date, "bg_time": bg_time})


def add_bg_time(name, date, bg_time):
    with conn:
        if not get_program_state(name) == None and get_time_by_program_date(name=name, date=date) == None:
            add_program_time(name, date, bg_time=bg_time)
        else:
            c.execute(
                "UPDATE program_times SET bg_time=bg_time + :bg_time WHERE date=:date AND name=:name", {"name": name, "date": date,  "bg_time": bg_time})


# def add_time_if_name_exists(name, date, time):    # replaced by default...
#     with conn:
#         if not get_program_state(name) == None and get_time_by_program_date(name=name, date=date) == None:
#             add_program_time(name, date)
#         c.execute(
#             "UPDATE program_times SET time=time + :time WHERE date=:date AND name=:name", {"name": name, "date": date,  "time": time})


def get_time_by_program_date(name, date):
    with conn:
        c.execute("SELECT * FROM program_times WHERE date=:date AND name=:name",
                  {"date": date, "name": name})
        return c.fetchone()  # [2] if not none


def get_bg_time_by_program_date(name, date):
    with conn:
        c.execute("SELECT * FROM program_times WHERE date=:date AND name=:name",
                  {"date": date, "name": name})
        return c.fetchone()  # [3] if not none


def get_times_by_program(name):
    with conn:
        c.execute("SELECT * FROM program_times WHERE name=:name",
                  {"name": name})
        return c.fetchall()


def get_fulltime_by_program(name):      # TODO + bgTime?
    lock.acquire(True)
    with conn:
        c.execute("SELECT * FROM program_times WHERE name=:name",
                  {"name": name})
        fulltime = 0
        for day in c.fetchall():
            fulltime += day[2]
        lock.release()
        return fulltime


def delete_program_time_by_name(name):
    with conn:
        c.execute("DELETE FROM program_times WHERE name=:name",
                  {"name": name})


def delete_program_time_by_name_and_date(name, date):
    with conn:
        c.execute("DELETE FROM program_times WHERE name=:name AND date=:date",
                  {"name": name, "date": date})
