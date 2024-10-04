import tkinter
#import python ,tkinter, mysql and other libraries
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import mysql.connector
from mysql.connector import Error
from PIL import Image, ImageTk
import re
import tkinter as tk
from tkinter import ttk
import webbrowser

#connecting to the database
voting_systemdb = mysql.connector.connect(
    host="localhost",
    user="root",
    password="Croatia@24",
    database="voting_system"
)

class votingsystem:
        #initializing the class
    def __init__(self, root):
        self.root = root
        self.root.title("Democracy Solutions, Inc")
        self.root.geometry("1200x750")
        self.root.config(bg="white")
        
        self.loginscreen()
    
    #function to destroy all the widgets on the screen
    def loginscreen(self):
        for i in self.root.winfo_children():
            i.destroy()
            
        self.login_frame = Frame(self.root, bg="white")
        self.login_frame.place(x=0, y=0, width=1200, height=750)
        
        self.show_pass_var = tk.IntVar()
        self.password_visible = False
        # adding Logindogpage1 image
        self.bg = Image.open("login screen image.png")
        self.bg = self.bg.resize((1200, 750), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bg_image = Label(self.login_frame, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
        #adding Welcome text on the top
        self.welcome_label = Label(self.login_frame, text="Empower Your Voice. Vote with Ease", font=("calibri", 20,"bold"), bg="white", fg="grey")
        self.welcome_label.place(x=30, y=40)
        self.welcome_label = Label(self.login_frame, text="Anytime, Anywhere.", font=("calibri", 20,"bold"), bg="white", fg="black")
        self.welcome_label.place(x=30, y=80)
        self.welcome_label = Label(self.login_frame, text="With Democracy Solutions, Inc", font=("calibri", 30,"bold"), bg="white", fg="grey")
        self.welcome_label.place(x=30, y=120)
        
        #adding login text to the login page right side
        self.login_label = Label(self.login_frame, text="Login", font=("calibri", 20,"bold"), bg="white", fg="black")
        self.login_label.place(x=900, y=150)
        
        # adding username labels and entry boxes
        self.username_label = Label(self.login_frame, text="Username", font=("calibri", 15,"bold"), bg="white", fg="black")
        self.username_label.place(x=850, y=200)
        self.username_entry = Entry(self.login_frame, font=("calibri", 15), bg="white", fg="black")
        self.username_entry.place(x=850, y=230)
        
        # adding password labels and entry boxes
        self.password_label = Label(self.login_frame, text="Password", font=("calibri", 15,"bold"), bg="white", fg="black")
        self.password_label.place(x=850, y=270)
        self.password_entry = Entry(self.login_frame, font=("calibri", 15), bg="white", fg="black", show="*")
        self.password_entry.place(x=850, y=300)
        
        # adding show password check button
        self.show_pass = Checkbutton(self.login_frame, text="Show Password", variable=self.show_pass_var, onvalue=1, offvalue=0,bg="white", fg="black")#command=self.show_password
        self.show_pass.place(x=850, y=330)
        
        # adding forgot password button
        self.forgot_pass = Button(self.login_frame, text="Forgot Password?", font=("calibri", 10), bg="white", fg="black", bd=0, cursor="hand2") #command=self.forgot_password
        self.forgot_pass.place(x=860, y=360)
        
        # adding login button
        self.login_button = Button(self.login_frame, text="Login", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2", command=self.login_authentication)
        self.login_button.place(x=880, y=390)
        
        # adding register button
        self.register_button = Button(self.login_frame, text="Register", font=("calibri", 15,"bold"), bg="white", fg="black", bd=1, cursor="hand2", command=self.signupscreen)
        self.register_button.place(x=960, y=390)
        
    def signupscreen(self):
        for i in self.root.winfo_children():
            i.destroy()
            
        self.signup_frame = Frame(self.root, bg="white")
        self.signup_frame.place(x=0, y=0, width=1200, height=750)
        
        self.show_pass_var = tk.IntVar()
        self.password_visible = False
        # adding Logindogpage1 image
        self.bg = Image.open("register.png")
        self.bg = self.bg.resize((1200, 750), Image.LANCZOS)
        self.bg = ImageTk.PhotoImage(self.bg)
        self.bg_image = Label(self.signup_frame, image=self.bg).place(x=0, y=0, relwidth=1, relheight=1)
    
        # adding register text to the signup page right side
        self.register_label = Label(self.signup_frame, text="Register to Vote", font=("calibri", 20,"bold"), bg="#fffcf5", fg="black")
        self.register_label.place(x=800, y=100)
        
        # add first name label and entry box a bit left to the register text
        self.first_name_label = Label(self.signup_frame, text="First Name", font=("calibri", 15,"bold"), bg="#fffcf5", fg="black")
        self.first_name_label.place(x=650, y=150)
        self.first_name_entry = Entry(self.signup_frame, font=("calibri", 15), bg="#fffcf5", fg="black")
        self.first_name_entry.place(x=650, y=180)
        
        # add last name label and entry box next to the first name entry box
        self.last_name_label = Label(self.signup_frame, text="Last Name", font=("calibri", 15,"bold"), bg="#fffcf5", fg="black")
        self.last_name_label.place(x=870, y=150)
        self.last_name_entry = Entry(self.signup_frame, font=("calibri", 15), bg="#fffcf5", fg="black")
        self.last_name_entry.place(x=870, y=180)
        
        # add email label and entry box below the first name entry box
        self.email_label = Label(self.signup_frame, text="Email", font=("calibri", 15,"bold"), bg="#fffcf5", fg="black")
        self.email_label.place(x=650, y=210)
        self.email_entry = Entry(self.signup_frame, font=("calibri", 15), bg="#fffcf5", fg="black")
        self.email_entry.place(x=650, y=240)
        
        # add home address label and entry box below rhe email entry box
        self.home_address_label = Label(self.signup_frame, text="Home Address", font=("calibri", 15,"bold"), bg="#fffcf5", fg="black")
        self.home_address_label.place(x=650, y=270)
        self.home_address_entry = Entry(self.signup_frame, font=("calibri", 15), bg="#fffcf5", fg="black")
        self.home_address_entry.place(x=650, y=300)
        
        # add phone number label and entry box below the home address entry box
        self.phone_number_label = Label(self.signup_frame, text="Phone Number", font=("calibri", 15,"bold"), bg="#fffcf5", fg="black")
        self.phone_number_label.place(x=650, y=330)
        self.phone_number_entry = Entry(self.signup_frame, font=("calibri", 15), bg="#fffcf5", fg="black")
        self.phone_number_entry.place(x=650, y=360)
        
        # add password label and entry box below the phone number entry box
        self.password_label = Label(self.signup_frame, text="Password", font=("calibri", 15,"bold"), bg="#fffcf5", fg="black")
        self.password_label.place(x=650, y=390)
        self.password_entry = Entry(self.signup_frame, font=("calibri", 15), bg="#fffcf5", fg="black", show="*")
        self.password_entry.place(x=650, y=420)
        
        # add confirm password label and entry box below the password entry box
        self.confirm_password_label = Label(self.signup_frame, text="Confirm Password", font=("calibri", 15,"bold"), bg="#fffcf5", fg="black")
        self.confirm_password_label.place(x=650, y=450)
        self.confirm_password_entry = Entry(self.signup_frame, font=("calibri", 15), bg="#fffcf5", fg="black", show="*")
        self.confirm_password_entry.place(x=650, y=480)
        
        # add register button
        self.register_button = Button(self.signup_frame, text="Register", font=("calibri", 15,"bold"), bg="#fffcf5", fg="black", bd=1, cursor="hand2", command=self.registration_data)
        self.register_button.place(x=770, y=520)
        
        # add back to login button
        self.login_button = Button(self.signup_frame, text="Back", font=("calibri", 15,"bold"), bg="#fffcf5", fg="black", bd=1, cursor="hand2", command=self.loginscreen)
        self.login_button.place(x=870, y=520)
        
    def registration_data(self):
        # get the data from the entry boxes
        first_name = self.first_name_entry.get()
        last_name = self.last_name_entry.get()
        email = self.email_entry.get()
        address = self.home_address_entry.get()
        mobile = self.phone_number_entry.get()
        password = self.password_entry.get()
        confirm_password = self.confirm_password_entry.get()
        
        # check if the data is empty
        if first_name == "" or last_name == "" or email == "" or mobile == "" or password == "" or confirm_password == "":
            messagebox.showerror("Error", "All fields are required")
            return
        # email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            messagebox.showerror("Error", "Invalid Email")
            return
        # mobile validation
        if not re.fullmatch(r"^[0-9]{10}$", mobile):
            messagebox.showerror("Error", "Invalid Mobile Number")
            return
        # password validation
        if len(password) < 8 or not re.search("[a-z]", password) or not re.search("[A-Z]", password) or not re.search("[0-9]", password):
            messagebox.showerror("Error", "Password must contain at least 8 characters, including letters and numbers")
            return
        # check if the password and confirm password are the same
        if password != confirm_password:
            messagebox.showerror("Error", "Password and Confirm Password should be the same")
            return
        # inserting the data to the database
        cursor = voting_systemdb.cursor()
        insert_data = f"INSERT INTO voter (first_name, last_name, email, address, mobile, password) VALUES ('{first_name}', '{last_name}', '{email}', '{address}', '{mobile}', '{password}')"
        cursor.execute(insert_data)
        voting_systemdb.commit()
        messagebox.showinfo("Success", "You have successfully registered")
        self.loginscreen()
        
    # login page validation with the database
    def login_authentication(self):
        # get the data from the entry boxes
        email = self.username_entry.get()
        password = self.password_entry.get()
        
        # checking the email and password with the database
        cursor = voting_systemdb.cursor()
        select_data = f"SELECT * FROM voter WHERE email = '{email}' AND password = '{password}'"
        cursor.execute(select_data)
        user = cursor.fetchone()

        if user:
            self.voter_id = user[0]
            self.first_name = user[1]
            self.last_name = user[2]
            self.email = user[3]
            self.address = user[4]
            self.mobile = user[5]
            self.current_password = user[6]
        elif email == "admin" and password == "admin":
            self.adminScreen()
        else:
            messagebox.showerror("Error", "Invalid Email or Password")
            return
        
        
        
        
        
        
        
        
        
        
#starter code
if __name__ == "__main__":
    root = Tk()
    app = votingsystem(root)
    root.mainloop()