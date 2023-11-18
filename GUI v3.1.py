import tkinter as tk
import tkinter.messagebox as mb
import os
import sys
import pickle
import random

# Model

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

class Student:
    def __init__(self, id, name, email, password, subjects):
        self.id = id
        self.name = name
        self.email = email
        self.password = password
        self.subjects = subjects

    def match(self, email, password):
        return self.email == email and self.password == password

    def subject_count(self):
        return len(self.subjects)

    def enrol(self, subject):
        if len(self.subjects) < 4:
            self.subjects.append(subject)

class Database:
    def __init__(self):
        self.users = self.load_users_from_file()

    def save_users_to_file(self):
        Controller.save(self.users)

    def load_users_from_file(self):
        try:
            return Controller.read()
        except (FileNotFoundError, EOFError):
            return []
        

    def match(self, email, password):
        for user in self.users:
            if user.match(email, password):
                return user
        return None

# Controller

class Controller:
    @staticmethod
    def filepath():
        scriptpath = os.path.abspath(sys.argv[0])
        scriptdir = os.path.dirname(scriptpath)
        return os.path.join(scriptdir, "students.data")

    @staticmethod
    def save(users):
        with open(Controller.filepath(), 'wb') as file:
            pickle.dump(users, file)

    @staticmethod
    def read():
        with open(Controller.filepath(), 'rb') as file:
            users = pickle.load(file)
        return users

#Frame view

class ConfirmationView(tk.Toplevel):
    def __init__(self, master, user):
        super().__init__(master=master)
        self.title("University GUI Enrollment Module")
        self.geometry("300x200")
        self.configure(bg='#607b8d')
        self.resizable(False, False)
        self.user = user
        label = tk.Label(self, text=f"Welcome {user.name}", fg='#ffc107',
                         font='Helvetica 12 bold', bg='#607b8d')
        label.pack(pady=(30, 10))
        subject_count_btn = tk.Button(self, text="View Enrolled Subjects",
                                      bg='#252525', fg='#ffc107',
                                      font='Helvetica 10 bold',
                                      command=self.view_subjects)
        subject_count_btn.pack(pady=10)

        enroll_btn = tk.Button(self, text="Enroll in Subjects",
                               bg='#252525', fg='#ffc107',
                               font='Helvetica 10 bold',
                               command=self.enroll_subject)
        enroll_btn.pacentr(pady=10)

    def view_subjects(self):
        view_subjects_window = tk.Toplevel(self)
        view_subjects_window.title("University GUI Enrollment Module")
        view_subjects_window.geometry("300x200")
        view_subjects_window.configure(bg='#607b8d')
        subject_list = tk.Label(view_subjects_window, text="Enrolled Subjects", bg='#607b8d', fg='#ffc107', font='Helvetica 12 bold')
        subject_list.pack(pady=(30, 10))
        if self.user.subjects:
            for subject in self.user.subjects:
                subject_info = f"Subject ID: {subject.id}, Mark: {subject.mark}, Grade: {subject.grade}"
                subject_label = tk.Label(view_subjects_window, text=subject_info, bg='#607b8d', fg='white', font='Helvetica 10')
                subject_label.pack()
        else:
            no_subject_label = tk.Label(view_subjects_window, text="No subjects enrolled", bg='#607b8d', fg='white', font='Helvetica 10')
            no_subject_label.pack()

    def enroll_subject(self):
        if self.user.subject_count() >= 4:
            info_message = "Already enrolled in 4 subjects"
            mb.showerror("Enrollment Error", info_message)
        else:
            enroll_subject_window = tk.Toplevel(self)
            enroll_subject_window.title("University GUI Enrollment Module")
            enroll_subject_window.geometry("300x200")
            enroll_subject_window.configure(bg='#607b8d')
            subject_list = tk.Label(enroll_subject_window, text="Enroll in New Subject", bg='#607b8d', fg='#ffc107', font='Helvetica 12 bold')
            subject_list.pack(pady=(60, 10))
            new_subject = Subject()
            self.user.enrol(new_subject)
            enrollment_message = f"Subject ID: {new_subject.id}, Mark: {new_subject.mark}, Grade: {new_subject.grade}"
            success_label = tk.Label(enroll_subject_window, text=enrollment_message, bg='#607b8d', fg='white', font='Helvetica 10')
            success_label.pack()
            database.save_users_to_file()

class LoginFrame(tk.LabelFrame):
    def clear(self):
        self.emailField.delete(0, tk.END)
        self.passwordField.delete(0, tk.END)

    def login(self, master, model):
        user = model.match(self.emailText.get(), self.passwordTxt.get())
        if user is not None:
            ConfirmationView(master, user)
            self.clear()
        else:
            info = "Incorrect email or password"
            mb.showerror(title="Login Error", message=info)
            self.clear()

    def __init__(self, master, model) -> None:
        super().__init__(master)
        box = tk.LabelFrame(master, text='Sign In', bg='#607b8d', fg='white',
                            padx=20, pady=20, font='Helvetica 10 bold')
        box.columnconfigure(0, weight=1)
        box.columnconfigure(1, weight=3)
        box.pack(pady=(30, 0))

        self.emailLbl = tk.Label(box, text="Email:", justify='left', fg='#ffc107',
                                 font='Helvetica 12 bold', bg='#607b8d')
        self.emailLbl.grid(column=0, row=0, padx=5, pady=5, sticky=tk.W)

        passwordLbl = tk.Label(box, text="Password:", fg='#ffc107',
                               font='Helvetica 12 bold', bg='#607b8d')
        passwordLbl.grid(column=0, row=1, padx=5, pady=5, sticky=tk.W)

        self.emailText = tk.StringVar()
        self.emailField = tk.Entry(box, textvariable=self.emailText)
        self.emailField.grid(column=1, row=0, padx=5, pady=5)
        self.emailField.focus()

        self.passwordTxt = tk.StringVar()
        self.passwordField = tk.Entry(
            box, textvariable=self.passwordTxt, show="*")
        self.passwordField.grid(column=1, row=1, padx=5, pady=5)

        self.loginBtn = tk.Button(box, text="Login",
                                  bg='#252525', fg='#ffc107',
                                  font='Helvetica 10 bold',
                                  command=lambda: self.login(master, model))
        self.loginBtn.grid(column=1, row=3, sticky=tk.E, padx=5, pady=5)

        self.cancelBtn = tk.Button(box,
                                   bg='#252525', fg='#ffc107',
                                   font='Helvetica 10 bold',
                                   text="Cancel", command=lambda: master.quit())
        self.cancelBtn.grid(column=1, row=3, sticky=tk.W, padx=5, pady=5)

# Main View

root = tk.Tk()
root.geometry("300x200")
root.title("University GUI Login Module")
root.configure(bg='#607b8d')
root.resizable(False, False)

database = Database()

box = LoginFrame(root, database)
root.mainloop()
