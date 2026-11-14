from datetime import datetime
from results import calculate_total, calculate_average, assign_grade

def sort_students(students, sort_by="name"):

       if sort_by == "average":
              return sorted(students,
                            key=lambda s: calculate_average(s["scores"]),
                            reverse=True)   
       return sorted(students, key=lambda s: s["name"].lower())


def class_statistics(students):
       averages = []
       for s in students:
              if s["scores"]:
                     averages.append(calculate_average(s["scores"]))


       if not averages:
              return None
       return {
              "highest": max(averages),
               "lowest": min(averages),
               "class_average": round(sum(averages) / len(averages), 2),

       }              
def build_text_report(students):
    lines = ["STUDENTS RESULT REPORTS",
               "Generated: " + datetime.now().strftime("%Y-%m-%d %H:%M"),
               "-" * 50]



    for s in sort_students(students, "average"):
        if s["scores"]:
            total = calculate_total(s["scores"])
            avg = calculate_average(s["scores"])
            grade = assign_grade(avg)
            lines.append(f"{s['student_id']} {s['name']} " 
                             f"Total: {total} Avg: {avg:.2f} Grade: {grade} ")


    stats = class_statistics(students)
    if stats:
           lines.append("-" * 50)
           lines.append(f"Highest average:{stats['highest']:.2f}")
           lines.append(f"Lowest average:{stats['lowest']:.2f}")
           lines.append(f"Class average:{stats['class_average']}")
    return "\n". join(lines)




def save_text_report(students, filename="report.txt"):
       with open(filename, "w") as file:
              file.write(build_text_report(students))
              return file.name


if __name__ == "__main__":
      test = [
            {"student_id": "NH-001", "name": "Ada-obi",
             "scores": {"Maths": 80, "English":70}},
            {"student_id": "NH-002", "name": "bayo",
             "scores": {"Maths": 50, "English":40}},
                         
            
      ]
print(class_statistics(test))
print(build_text_report(test))
        