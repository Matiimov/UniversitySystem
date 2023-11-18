import os
import random
import pickle
import re

class Database:
    @staticmethod
    def file_exists():
        return os.path.exists("students.data")

    @staticmethod
    def create_file():
        open("students.data", "wb").close()

    @staticmethod
    def write_objects(data):
        with open("students.data", "wb") as f:
            pickle.dump(data, f)

    @staticmethod
    def read_objects():
        with open("students.data", "rb") as f:
            try:
                # Check if file is empty
                if os.path.getsize("students.data") == 0:
                    return []
                return pickle.load(f)
            except Exception as e:
                print(f"Error loading data: {e}")
                return []

    @staticmethod
    def clear_data():
        open("students.data", "wb").close()


class Subject:
    def __init__(self):
        self.id = f"{random.randint(1, 999):03d}"
        self.mark = random.randint(25, 100)
        self.grade = self.calculate_grade()

    def calculate_grade(self):
        if self.mark >= 85:
            return "HD"
        elif self.mark >= 70:
            return "D"
        elif self.mark >= 55:
            return "C"
        elif self.mark >= 50:
            return "P"
        else:
            return "F"


class Utils:
    EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@university\.com$")
    PASSWORD_REGEX = re.compile(r"^[A-Z][a-zA-Z]{5,}\d{3,}$")


class Student:
    def __init__(self, name, email, password):
        self.id = f"{random.randint(1, 999999):06d}"
        self.name = name
        self.email = email
        self.password = password
        self.subjects = []

    @staticmethod
    def menu():
        while True:
            print("\n\033[34m--- STUDENT MENU ---\033[0m")
            print("\033[32m(L) Login\033[0m")
            print("\033[32m(R) Register\033[0m")
            print("\033[32m(X) Exit\033[0m")
            choice = input("Enter your choice: ").lower()
            if choice == 'l':
                student = Student.login()
                if student:
                    Student.course_menu(student)
            elif choice == 'r':
                UniSystem.register_student()
            elif choice == 'x':
                break
            else:
                print("\033[31mInvalid choice!\033[0m")

    @staticmethod
    def student_exists(email):
        students = []
        if Database.file_exists():
            students = Database.read_objects()
        for student in students:
            if student.email == email:
                return True
        return False

    @staticmethod
    def login():
        email = input("Enter email: ")
        password = input("Enter password: ")
        students = Database.read_objects()

        # Check if the student exists
        student = next((student for student in students if student.email == email), None)
        if not student:
            print("\033[31mStudent does not exist.\033[0m")
            return None
        if student.password != password:
            print("\033[31mInvalid email or password!\033[0m")
            return None
        print("\033[33mEmail and password formats acceptable\033[0m")
        return student

    def enrol(self, subject):
        if len(self.subjects) < 4:
            self.subjects.append(subject)

    def drop(self, subject_id):
        if any(subject.id == subject_id for subject in self.subjects):
            self.subjects = [subject for subject in self.subjects if subject.id != subject_id]
            return True
        return False

    def average_mark(self):
        if not self.subjects:
            return 0
        return sum(subject.mark for subject in self.subjects) / len(self.subjects)

    def pass_or_fail(self):
        return "Pass" if self.average_mark() >= 50 else "Fail"
    
    def change_student_password(self):
        while True:
            current_password = input("Enter current password: ")
            if self.password != current_password:
                print("\033[31mInvalid choice!\033[0m")
                continue

            new_password = input("Enter new password: ")
            confirm_new_password = input("Confirm new password: ")

            # Validate new password format
            if not Utils.PASSWORD_REGEX.match(new_password):
                print("\033[31mIncorrect password format!\033[0m")
                continue
            if new_password != confirm_new_password:
                print("\033[31mPassword does not match - try again!\033[0m")
                continue

            # Change the password
            self.password = new_password
            students = Database.read_objects()
            for s in students:
                if s.id == self.id:
                    s.password = self.password
            Database.write_objects(students)
            print("\033[33mUpdating Password\033[0m")
            break

    def course_menu(student):
        while True:
            print("\n\033[34mStudent Course Menu:\033[0m")
            print("\033[34m(C) Change Password\033[0m")
            print("\033[34m(E) Enroll in a new subject\033[0m")
            print("\033[34m(R) Remove a subject\033[0m")
            print("\033[34m(S) Show all subjects\033[0m")
            print("\033[34m(X) Exit\033[0m")

            choice = input("Enter your choice: ").lower()
            if choice == 'c':
                print("\n")
                student.change_student_password()
            elif choice == 'e':
                print("\n")
                if len(student.subjects) < 4:
                    new_subject = Subject()
                    student.enrol(new_subject)
                    print(f"\033[33mEnrolling in Subject-{new_subject.id}\033[0m")
                    print(f"\033[33mYou are now enrolled in {len(student.subjects)} out of 4 subjects\033[0m")
                    students = Database.read_objects()
                    for s in students:
                        if s.id == student.id:
                            s.subjects = student.subjects
                    Database.write_objects(students)
                else:
                    print("\033[31mStudents are allowed to enroll in 4 subjects only\033[0m")
            elif choice == 'r':
                subject_id = input("\nEnter subject ID to drop: ")
                if student.drop(subject_id):
                    print(f"\033[33mSubject-{subject_id} dropped!\033[0m")
                    students = Database.read_objects()
                    for s in students:
                        if s.id == student.id:
                            s.subjects = student.subjects
                    Database.write_objects(students)
                else:
                    print(f"\033[31mSubject-{subject_id} not found!\033[0m")
            elif choice == 's':
                print(f"\033[33mShowing {len(student.subjects)} subjects\033[0m")
                for subject in student.subjects:
                    print(f"[ Subject:: {subject.id} - - mark = {subject.mark} - - grade = {subject.grade} ]")
            elif choice == 'x':
                break
            else:
                print("\033[31mInvalid choice!\033[0m")


class UniSystem:
    @staticmethod
    def menu():
        while True:
            print("\n\033[34m--- UNIVERSITY SYSTEM ---\033[0m")
            print("\033[34m(A) Admin\033[0m")
            print("\033[34m(S) Student\033[0m")
            print("\033[34m(X) Exit\033[0m")
            choice = input("Enter your choice: ").lower()
            if choice == 'a':
                Admin.menu()
            elif choice == 's':
                Student.menu()
            elif choice == 'x':
                print("\n\033[33mThank You\033[0m")
                break
            else:
                print("\033[31mInvalid choice!\033[0m")


    @staticmethod
    def register_student():
        print("\n\033[32mStudent Sign Up\033[0m")
        while True:
            email = input("Email: ")
            password = input("Password: ")

            if not Utils.EMAIL_REGEX.match(email):
                print("\033[31mIncorrect email format\033[0m")
                continue
            if not Utils.PASSWORD_REGEX.match(password):
               print("\033[31mIncorrect password format\033[0m")
               continue
            if Student.student_exists(email):
                print(f"\033[31mStudent with email {email} already exists\033[0m")
                return

            # If validation passed and student doesn't exist, then register the student
            name = input("Name: ")
            new_student = Student(name, email, password)
            students = []
            if Database.file_exists():
                students = Database.read_objects()
            students.append(new_student)
            Database.write_objects(students)
            print(f"\033[33mEnrolling Student {name}\033[0m")
            return


class Admin:
    @staticmethod
    def menu():
        while True:
            print("\n\033[34m--- ADMIN MENU ---\033[0m")
            print("\033[34m(C) Clear database file\033[0m")
            print("\033[34m(G) Group students by grade\033[0m")
            print("\033[34m(P) Partition students by pass/fail\033[0m")
            print("\033[34m(R) Remove student by ID\033[0m")
            print("\033[34m(S) Show all students\033[0m")
            print("\033[34m(X) Exit\033[0m")

            choice = input("Enter your choice: ").lower()

            students = Database.read_objects()

            if choice == 'c':
                Admin.clear_database(students)
            elif choice == 'g':
                Admin.group_students_by_grade(students)
            elif choice == 'p':
                Admin.partition_pass_fail(students)
            elif choice == 'r':
                Admin.remove_student_by_id(students)
            elif choice == 's':
                Admin.show_all_students(students)
            elif choice == 'x':
                break
            else:
               print("\033[31mInvalid choice!\033[0m")


    @staticmethod
    def clear_database(students):
        print("\033[33m\nClearing students database\033[0m")
        print("\033[31mAre you sure you want to clear the database (Y)ES/ (N)O: \033[0m", end="")
        confirm = input().upper()

        if confirm == 'Y':
            Database.clear_data()
            students = []
            print("\033[33mStudents data cleared\033[0m")
        elif confirm == 'N':
            print("\033[33mDatabase not cleared\033[0m")
        else:
            print("\033[31mInvalid choice!\033[0m")


    @staticmethod
    def partition_pass_fail(students):
        print("\033[33m\nPASS/FAIL Partition\033[0m")
        pass_students = [student.name for student in students if student.average_mark() >= 50]
        fail_students = [student.name for student in students if student.average_mark() < 50]
        
        print(f"PASS --> {', '.join(pass_students) if pass_students else 'No students'}")
        print(f"FAIL --> {', '.join(fail_students) if fail_students else 'No students'}")

    @staticmethod
    def group_students_by_grade(students):
        print("\n")
        grade_to_students = {
            "HD": [],
            "D": [],
            "C": [],
            "P": [],
            "F": []
        }

        for student in students:
            if not student.subjects:
                continue
            for subject in student.subjects:
                grade_name = subject.grade
                grade_to_students[grade_name].append(f"{student.name} :: {student.id} --> Grade: {grade_name} - Mark: {subject.mark}")

        print("\033[33mStudents Grouped by Grade:\033[0m")
        for grade_name, student_list in grade_to_students.items():
            print(f"{grade_name} --> {', '.join(student_list) if student_list else '< No students >'}")

    @staticmethod
    def remove_student_by_id(students):
        print("\n")
        student_id = input("Enter the student ID to remove: ")
        initial_len = len(students)
        students = [student for student in students if student.id != student_id]
        if initial_len == len(students):
            print(f"\033[31mNo student found with ID {student_id}\033[0m")
        else:
            Database.write_objects(students)
            print(f"\033[33mRemoving student {student_id} Account\033[0m")

    @staticmethod
    def show_all_students(students):
        print("\n")
        print("\033[33mStudent List\033[0m")
        if not students:
            print("< Nothing to Display >")
        else:
            for student in students:
                print(f"{student.name} :: {student.id} --> Email: {student.email}")


if __name__ == "__main__":
    if not Database.file_exists():
        Database.create_file()
    
    UniSystem.menu()