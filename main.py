import re
from datetime import datetime

from student import Student 
from storage import load_students, save_students
from results import calculate_total, calculate_average, assign_grade



def find_student(students, student_id):
    for s in students:
        if s["student_id"].lower() == student_id.lower():
            return s
        return None

def add_students(students):
    student_id = input("Student_ID: ").strip()
    if not re.match(r"^[A-Za-z0-9/-]{3,20}$", student_id):
        print("Invalid ID. Use 3-20 letters, numbers or hyphens.")
        return
    if find_student(students, student_id):
        print("That ID already exists.")
        return
    name = input("Full name: ").strip()
    form = input("Class/Form: ").strip()
    gender = input("Gender: ").strip()
    dob = input("Date of birth (YYYY-MM-DD): ").strip()
    try:
        datetime.strptime(dob, "%Y-%m-%d")
    except ValueError:
        print("Invalid date.")
        return
    students.append(Student(student_id, name, form, gender, dob).to_dict())
    save_students(students)
    print("Student added.")

def view_all(students):
    if not students:
        print("No students yet.")
    for s in students:
        if s.get("scores"):
            avg = calculate_average(s["scores"])
            print(f"{s['student_id']} | {s['name']} | {s['form']} | "
                  f"Total {calculate_total(s['scores'])} | "
                  f"Avg {avg} | {assign_grade(avg)}")
        else:
            print(f"{s['student_id']} | {s['name']} | {s['form']} | no scores")

def search_student(students):
    text = input("Search by ID or name: ").strip().lower()
    found = [s for s in students
             if text in s["student_id"].lower() or text in s["name"].lower()]
    view_all(found)


def delete_student(students):
    s = find_student(students, input("Student ID: ").strip())
    if s is None:
       print("Not found.")
       return
    students.remove(s)
    save_students(students)
    print("Deleted.")            

def main():
    students = load_students()
    while True:
        print("\n=== STUDENT RESULT SYSTEM ===")
        print("1. Add student")
        print("2. View all students")
        print("0. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_students(students)
        elif choice == "2":
            view_all(students)
        elif choice == "0":
            print("Goodbye!")
            break
        else:
            print("Invalid choice.")

main()    