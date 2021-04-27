import json
import os.path

file = "ApplicationTimeTracker/settings.json"

# TODO add settings

# TODO idle-time --- window x y --- (sql-settings) --- filter-queue?    


def save_settings():
    data = {"idleTime": 120, "windowPosition": [100, 100]}

    with open(file, 'w') as outfile:
        json.dump(data, outfile)

if os.path.exists(file) == False:
    save_settings()

# save_settings()


def edit_settings(setting, text):
    with open(file, 'r') as f:
        config = json.load(f)
    config[setting] = text
    with open(file, 'w') as f:
        json.dump(config, f)


def load_settings():
    with open(file) as json_file:
        data = json.load(json_file)
        print(data)
        for e in data:
            print(e, ":", data[e])

# ----- idleTime -----

def load_idleTime():
    with open(file) as json_file:
        data = json.load(json_file)
    return data["idleTime"]


def set_idleTime(time):
    edit_settings("idleTime", time)

# ----- windowPosition -----

def load_windowPosition():
    with open(file) as json_file:
        data = json.load(json_file)
    return data["windowPosition"]


def set_windowPosition(x, y):
    edit_settings("windowPosition", [x, y])


# ----- ----- -----

