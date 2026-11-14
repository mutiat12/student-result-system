import json

DATA_FILE = "students.json"

def save_students(students):
    try:
        with open(DATA_FILE, "w") as file:
            json.dump(students, file, indent=2)
    except OSError:
        print("Could not save the data.")
    else:
        print("Data saved.")


def load_students():
    try:
        with open(DATA_FILE, "r") as file:
            data = json.load(file)
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        print("The data is damaged, Starting empty.")
        return []
    else:
        return data
    finally:
        print("Load finished")



