import os

class Student:
    """Represents a student with marks in multiple subjects."""

    def __init__(self, roll_no, name, marks):
        self.roll_no = roll_no
        self.name = name
        self.marks = marks

    def average(self):
        """Returns average marks."""
        return sum(self.marks.values()) / len(self.marks)

    def grade(self):
        """Returns grade based on average."""
        avg = self.average()

        if avg >= 90:
            return "A"
        elif avg >= 80:
            return "B"
        elif avg >= 70:
            return "C"
        elif avg >= 60:
            return "D"
        else:
            return "F"

    def __str__(self):
        return f"{self.roll_no} | {self.name} | Avg: {self.average():.2f} | Grade: {self.grade()}"

FILE = "records.txt"


def save_all(students):
    """Saves all students to file."""
    with open(FILE, "w") as f:
        for s in students:
            subject_data = ",".join([f"{sub}:{mark}" for sub, mark in s.marks.items()])
            f.write(f"{s.roll_no},{s.name},{subject_data}\n")


def load_all():
    """Loads students from file and returns Student objects."""
    students = []

    if not os.path.exists(FILE):
        return students

    with open(FILE, "r") as f:
        for line in f:
            parts = line.strip().split(",")
            roll_no = parts[0]
            name = parts[1]

            marks = {}
            for item in parts[2:]:
                sub, score = item.split(":")
                marks[sub] = int(score)

            students.append(Student(roll_no, name, marks))

    return students

def find_student(students, roll_no):
    for s in students:
        if s.roll_no == roll_no:
            return s
    return None

def class_statistics(students):
    """Displays class statistics."""

    if not students:
        print("No students available.")
        return

    total_students = len(students)
    averages = [s.average() for s in students]

    highest = max(students, key=lambda s: s.average())
    lowest = min(students, key=lambda s: s.average())

    grade_count = {"A":0, "B":0, "C":0, "D":0, "F":0}
    subject_totals = {}

    for s in students:
        grade_count[s.grade()] += 1

        for sub, mark in s.marks.items():
            if sub not in subject_totals:
                subject_totals[sub] = []
            subject_totals[sub].append(mark)

    subject_avg = {
        sub: sum(marks)/len(marks) for sub, marks in subject_totals.items()
    }

    best_subject = max(subject_avg, key=subject_avg.get)

    print("\n--- CLASS STATISTICS ---")
    print("Total Students:", total_students)
    print("Class Average:", sum(averages)/len(averages))
    print("Highest Performer:", highest.name)
    print("Lowest Performer:", lowest.name)
    print("Grade Distribution:", grade_count)
    print("Top Subject:", best_subject)

def add_student(students):
    """Adds a new student with validation."""

    roll_no = input("Enter roll no: ")

    if find_student(students, roll_no):
        print("Roll number already exists!")
        return

    name = input("Enter name: ")
    if not name.strip():
        print("Invalid name!")
        return

    try:
        num_subjects = int(input("How many subjects? "))
    except:
        print("Invalid number!")
        return

    marks = {}

    for _ in range(num_subjects):
        sub = input("Subject name: ")
        try:
            mark = int(input("Marks (0-100): "))
            if mark < 0 or mark > 100:
                print("Invalid marks skipped.")
                continue
        except:
            print("Invalid input skipped.")
            continue

        marks[sub] = mark

    students.append(Student(roll_no, name, marks))
    save_all(students)
    print("Student added successfully!")


def view_students(students):
    for s in students:
        print(s)


def search_student(students):
    roll_no = input("Enter roll no: ")
    s = find_student(students, roll_no)

    if s:
        print(s)
    else:
        print("Student not found.")


def delete_student(students):
    roll_no = input("Enter roll no: ")
    s = find_student(students, roll_no)

    if s:
        students.remove(s)
        save_all(students)
        print("Deleted successfully.")
    else:
        print("Student not found.")


def top_performer(students):
    if not students:
        print("No data.")
        return

    top = max(students, key=lambda s: s.average())
    print("Top Performer:", top)

def menu():
    students = load_all()

    while True:
        print("\n=== Student Management System ===")
        print("1. Add new student")
        print("2. View all students")
        print("3. Search by roll number")
        print("4. Delete a student")
        print("5. Show top performer")
        print("6. Show class statistics")
        print("0. Exit")

        choice = input("Enter choice: ")

        if choice == "1":
            add_student(students)
        elif choice == "2":
            view_students(students)
        elif choice == "3":
            search_student(students)
        elif choice == "4":
            delete_student(students)
        elif choice == "5":
            top_performer(students)
        elif choice == "6":
            class_statistics(students)
        elif choice == "0":
            save_all(students)
            print("Exiting...")
            break
        else:
            print("Invalid choice!")

menu()