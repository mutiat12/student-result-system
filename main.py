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
        print("3. Search student")
        print("4. Delete student")
        print("5. Record / update scores")
        print("6. Show report card")
        print("0. Exit")
        choice = input("Choose: ").strip()
        if choice == "1":
            add_students(students)
        elif choice == "2":
             view_all(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            delete_student(students)
        elif choice == "5":
            record_scores(students)
        elif choice == "6":
            report_card(students)
        elif choice == "0":
             print("Goodbye!")
             break
        else:
            print("Invalid choice.")

def record_scores(students):
    s = find_student(students, input("Student ID: ").strip())
    if s is None:
        print("Not found. Choose 2 to see the exact IDs.")
        return
    scores = {}
    while True:
        print(f"Subjects so far: {len(scores)}")
        subject = input("Subject (type done, or press Enter, to finish): ").strip().title()
        if subject in ("", "Done"):
            if len(scores) >= 5:
                break
            print("You need at least 5 different subjects.")
            continue
        try:
            score = float(input(f"Score for {subject} (0-100): "))
        except ValueError:
            print("Enter a number.")
            continue
        if not 0 <= score <= 100:
            print("Score must be between 0 and 100.")
            continue
        scores[subject] = score
    s["scores"] = scores
    s["date_entered"] = datetime.now().strftime("%Y-%m-%d %H:%M")
    save_students(students)
    print("Scores saved.")

def report_card(students):
    s = find_student(students, input("Student ID: ").strip())
    if s is None or not s.get("scores"):
       print("Student not found or has no scores.")
       return
    print(f"\nREPORT CARD: {s['name']} ({s['student_id']}) {s.get('form', '-')}")
    for subject, score in s["scores"].items():
       print(f" {subject:<15}{score}")
    avg = calculate_average(s["scores"])
    print(f" Total: {calculate_total(s['scores'])} Average: {avg} "
          f"Grade: {assign_grade(avg)}")
    print(f" Results entered: {s.get('date_entered')}")



main()   