from datetime import datetime 

class Student:
    def __init__(self, student_id, name, form, gender, dob):
       self.student_id = student_id
       self.name = name 
       self.form = form
       self.gender = gender
       self.dob = dob
       self.scores = {}
       self.date_entered = None 

    def set_scores(self, scores):
        self.scores = scores
        self.date_entered = datetime.now().strftime("%Y-%m-%d %H: %M")

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "name": self.name,
            "form": self.form,
            "gender": self.gender,
            "dob": self.dob,
            "scores": self.scores,
            "date_entered": self.date_entered,
        }



if __name__ == "__main__":
    s1 = Student("NH-001", "Ada-obi", "SS2 A", "Female", "2009-04-12")
    s1.set_scores({"Maths": 70, "English": 80})
    print(s1.name)
    print(s1.to_dict())
